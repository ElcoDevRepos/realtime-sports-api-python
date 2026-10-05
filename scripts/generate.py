#!/usr/bin/env python3
"""Generate the typed models and operation methods from the Realtime Sports API OpenAPI spec.

    python scripts/generate.py                                 # production spec
    SPEC=/tmp/rsa-spec/openapi.json python scripts/generate.py # local file

Writes src/realtime_sports_api/_types.py and src/realtime_sports_api/_operations.py.
Only the standard library is used.
"""
from __future__ import annotations

import json
import keyword
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "src" / "realtime_sports_api"
DEFAULT_SPEC = "https://www.realtimesportsapi.com/openapi.json"

RENAME = {"Error": "ErrorBody"}

WEBHOOK_ALIASES = {
    "listWebhooks": "list",
    "createWebhook": "create",
    "getWebhook": "get",
    "updateWebhook": "update",
    "deleteWebhook": "delete",
    "getWebhookSecret": "get_secret",
    "rotateWebhookSecret": "rotate_secret",
    "testWebhook": "test",
    "listWebhookDeliveries": "deliveries",
}

# Required query parameters that become positional arguments.
POSITIONAL_QUERY = {("searchAthletes", "query"), ("getAthleteGameLog", "season")}


def load_spec() -> dict:
    src = os.environ.get("SPEC", DEFAULT_SPEC)
    print(f"Reading spec from {src}", file=sys.stderr)
    if re.match(r"^https?://", src):
        with urllib.request.urlopen(src, timeout=30) as r:  # noqa: S310 - fixed https URL or user-provided
            return json.load(r)
    return json.loads(Path(src).read_text())


def snake(name: str) -> str:
    name = name.replace("WebSocket", "Websocket")
    s = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name).lower()
    s = s.replace("-", "_").replace(".", "_")
    if keyword.iskeyword(s):
        s += "_"
    return s


def ref_name(ref: str) -> str:
    n = ref.rsplit("/", 1)[-1]
    return RENAME.get(n, n)


def py_type(schema: dict | None, *, top: bool = True) -> str:
    if not schema:
        return "Any"
    nullable = schema.get("nullable", False)
    t: str
    if "$ref" in schema:
        t = f'"{ref_name(schema["$ref"])}"'
    elif "allOf" in schema:
        refs = [x for x in schema["allOf"] if "$ref" in x]
        t = f'"{ref_name(refs[0]["$ref"])}"' if refs else "Dict[str, Any]"
    elif "enum" in schema:
        vals = ", ".join(json.dumps(v) for v in schema["enum"])
        t = f"Literal[{vals}]"
    else:
        typ = schema.get("type")
        if typ == "string":
            t = "str"
        elif typ == "integer":
            t = "int"
        elif typ == "number":
            t = "float"
        elif typ == "boolean":
            t = "bool"
        elif typ == "array":
            t = f"List[{py_type(schema.get('items'), top=False)}]"
        else:
            t = "Dict[str, Any]"
    return f"Optional[{t}]" if nullable else t


def gen_types(spec: dict) -> str:
    schemas = spec["components"]["schemas"]
    out = [
        '"""Typed models generated from the Realtime Sports API OpenAPI spec. Do not edit by hand.',
        "",
        "Regenerate with `python scripts/generate.py`. Every TypedDict is `total=False`: the API may omit",
        "fields, so read them with `.get()` when in doubt. Nested inline objects are typed as plain dicts.",
        '"""',
        "from __future__ import annotations",
        "",
        "from typing import Any, Dict, List, Literal, Optional, TypedDict",
        "",
        "",
    ]
    names = []
    for raw_name, schema in schemas.items():
        name = RENAME.get(raw_name, raw_name)
        names.append(name)
        desc = schema.get("description")
        if "enum" in schema:
            vals = ", ".join(json.dumps(v) for v in schema["enum"])
            out.append(f"{name} = Literal[{vals}]")
            out.append("")
            continue
        bases = []
        props: dict = {}
        if "allOf" in schema:
            for part in schema["allOf"]:
                if "$ref" in part:
                    bases.append(ref_name(part["$ref"]))
                else:
                    props.update(part.get("properties", {}))
        props.update(schema.get("properties", {}))
        base = ", ".join(bases) if bases else "TypedDict"
        bad = [k for k in props if keyword.iskeyword(k) or not k.isidentifier()]
        if bad:
            fields = ", ".join(f"{json.dumps(k)}: {py_type(v)}" for k, v in props.items())
            out.append(f"{name} = TypedDict({json.dumps(name)}, {{{fields}}}, total=False)")
            out.append("")
            continue
        out.append(f"class {name}({base}, total=False):")
        if desc:
            out.append(f'    """{desc.strip().splitlines()[0]}"""')
            out.append("")
        if not props and not desc:
            out.append("    pass")
        for k, v in props.items():
            out.append(f"    {k}: {py_type(v)}")
        out.append("")
        out.append("")
    out.append("__all__ = [")
    for n in names:
        out.append(f'    "{n}",')
    out.append("]")
    return "\n".join(out).rstrip() + "\n"


def data_schema(op: dict) -> dict | None:
    resp = op["responses"].get("200") or op["responses"].get("201")
    try:
        return resp["content"]["application/json"]["schema"]["properties"]["data"]
    except (KeyError, TypeError):
        return None


def resolve_body(spec: dict, op: dict) -> tuple[dict, list[str]]:
    rb = op.get("requestBody")
    if not rb:
        return {}, []
    schema = rb["content"]["application/json"]["schema"]
    props: dict = {}
    required = list(schema.get("required", []))
    parts = schema.get("allOf", []) + [schema]
    for part in parts:
        if "$ref" in part:
            target = spec["components"]["schemas"][part["$ref"].rsplit("/", 1)[-1]]
            props.update(target.get("properties", {}))
            required += target.get("required", [])
        else:
            props.update(part.get("properties", {}))
    return props, required


def collect_ops(spec: dict) -> list[dict]:
    ops = []
    for path, item in spec["paths"].items():
        for method, op in item.items():
            if not isinstance(op, dict) or "operationId" not in op:
                continue
            params = list(item.get("parameters", [])) + list(op.get("parameters", []))
            path_params = [p for p in params if p["in"] == "path"]
            query_params = [p for p in params if p["in"] == "query"]
            body_props, body_required = resolve_body(spec, op)
            absolute = bool(item.get("servers") or op.get("servers"))
            ops.append(
                dict(
                    id=op["operationId"],
                    method=method.upper(),
                    path=path,
                    summary=(op.get("summary") or "").strip(),
                    path_params=path_params,
                    query_params=query_params,
                    body_props=body_props,
                    body_required=body_required,
                    has_body="requestBody" in op,
                    body_optional=("requestBody" in op and not op["requestBody"].get("required", False)),
                    ret=py_type(data_schema(op)),
                    absolute=absolute,
                )
            )
    return ops


def path_expr(op: dict) -> str:
    if op["absolute"]:
        return "self._websocket_auth_url"
    expr = re.sub(r"\{(\w+)\}", lambda m: "{_p(" + snake(m.group(1)) + ")}", op["path"])
    return f'f"{expr}"' if "{" in expr else f'"{expr}"'


def signature(op: dict) -> tuple[list[str], list[str], list[str], list[str]]:
    """Return (positional args, keyword-only args, query dict lines, body dict lines)."""
    pos, kw, qlines, blines = [], [], [], []
    for p in op["path_params"]:
        pos.append(f"{snake(p['name'])}: Union[str, int]")
    for p in op["query_params"]:
        arg = snake(p["name"])
        typ = py_type(p.get("schema"))
        if (op["id"], p["name"]) in POSITIONAL_QUERY:
            pos.append(f"{arg}: {typ}")
        else:
            kw.append(f"{arg}: Optional[{typ}] = None")
        qlines.append(f'"{p["name"]}": {arg}')
    for name, schema in op["body_props"].items():
        arg = snake(name)
        typ = py_type(schema)
        if name in op["body_required"]:
            pos.append(f"{arg}: {typ}")
        else:
            kw.append(f"{arg}: Union[{typ}, NotGiven] = NOT_GIVEN")
        blines.append(f'"{name}": {arg}')
    return pos, kw, qlines, blines


def gen_method(op: dict, *, name: str, is_async: bool, with_meta: bool, delegate: str | None = None) -> list[str]:
    pos, kw, qlines, blines = signature(op)
    args = ["self", *pos, "*", *kw, "request_options: Optional[RequestOptions] = None"]
    ret = f"ApiResponse[{op['ret']}]" if with_meta else op["ret"]
    d = "async def" if is_async else "def"
    lines = [f"    {d} {name}(", *[f"        {a}," for a in args], f"    ) -> {ret}:"]
    doc = f"`{op['id']}` - {op['method']} {op['path']}"
    if op["summary"]:
        doc += f": {op['summary']}"
    lines.append(f'        """{doc}"""')
    aw = "await " if is_async else ""
    if delegate:
        call_args = [a.split(":")[0] for a in pos] + [f"{a.split(':')[0]}={a.split(':')[0]}" for a in kw]
        call_args.append("request_options=request_options")
        lines.append(f"        return {aw}self._parent.{delegate}({', '.join(call_args)})")
        lines.append("")
        return lines
    q = "{" + ", ".join(qlines) + "}" if qlines else "None"
    if op["has_body"]:
        b = "{" + ", ".join(blines) + "}" if blines else "{}"
    else:
        b = "NOT_GIVEN"
    fn = "_request_with_meta" if with_meta else "_request_data"
    lines.append(
        f'        return {aw}self.{fn}("{op["method"]}", {path_expr(op)}, query={q}, body={b}, request_options=request_options)'
    )
    lines.append("")
    return lines


def gen_operations(spec: dict) -> str:
    ops = collect_ops(spec)
    type_names = sorted({RENAME.get(n, n) for n in spec["components"]["schemas"]})
    out = [
        '"""Operation methods generated from the Realtime Sports API OpenAPI spec. Do not edit by hand.',
        "",
        "Regenerate with `python scripts/generate.py`.",
        '"""',
        "# ruff: noqa: E501",
        "from __future__ import annotations",
        "",
        "from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union",
        "",
        "from ._base import NOT_GIVEN, ApiResponse, NotGiven, RequestOptions, _p",
        "",
        "if TYPE_CHECKING:",
        "    from typing import Literal",
        "",
        "    from ._types import (",
        *[f"        {n}," for n in type_names],
        "    )",
        "",
        "",
    ]
    variants = [
        ("_SyncOperations", False, False, "_SyncWebhooks"),
        ("_SyncOperationsWithMeta", False, True, "_SyncWebhooksWithMeta"),
        ("_AsyncOperations", True, False, "_AsyncWebhooks"),
        ("_AsyncOperationsWithMeta", True, True, "_AsyncWebhooksWithMeta"),
    ]
    for cls, is_async, with_meta, wh_cls in variants:
        # webhooks namespace
        out.append(f"class {wh_cls}:")
        out.append('    """`client.webhooks` namespace (aliases of the `*_webhook*` methods)."""')
        out.append("")
        out.append(f'    def __init__(self, parent: "{cls}") -> None:')
        out.append("        self._parent = parent")
        out.append("")
        for op in ops:
            if op["id"] in WEBHOOK_ALIASES:
                out.extend(gen_method(op, name=WEBHOOK_ALIASES[op["id"]], is_async=is_async, with_meta=with_meta, delegate=snake(op["id"])))
        out.append("")
        out.append(f"class {cls}:")
        out.append('    """Generated API methods. Mixed into the client classes."""')
        out.append("")
        out.append("    _websocket_auth_url: str")
        out.append("")
        if is_async:
            out.append("    async def _request_data(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover")
            out.append("        raise NotImplementedError")
            out.append("")
            out.append("    async def _request_with_meta(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover")
            out.append("        raise NotImplementedError")
        else:
            out.append("    def _request_data(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover")
            out.append("        raise NotImplementedError")
            out.append("")
            out.append("    def _request_with_meta(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover")
            out.append("        raise NotImplementedError")
        out.append("")
        out.append("    @property")
        out.append(f"    def webhooks(self) -> {wh_cls}:")
        out.append('        """Webhook management: list/create/get/update/delete/get_secret/rotate_secret/test/deliveries."""')
        out.append(f"        return {wh_cls}(self)")
        out.append("")
        for op in ops:
            out.extend(gen_method(op, name=snake(op["id"]), is_async=is_async, with_meta=with_meta))
        out.append("")
    out.append(f"OPERATION_IDS = {json.dumps([o['id'] for o in ops])}")
    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    spec = load_spec()
    (PKG / "_types.py").write_text(gen_types(spec))
    (PKG / "_operations.py").write_text(gen_operations(spec))
    print(f"Wrote {PKG / '_types.py'} and {PKG / '_operations.py'}", file=sys.stderr)


if __name__ == "__main__":
    main()
