#!/usr/bin/env python3
"""
inline-assets.py · v0.2.2 跨目录加载防御工具

把 verdict HTML 中所有本地图片 / SVG 引用替换为 base64 data URI，
让单文件可移植到任何环境（邮件 / Notion / 用户桌面）而不断图。

用法：
    python3 inline-assets.py <input.html> [output.html]

如果不指定 output，则输出到 <input>-inline.html。

支持识别的引用形式：
    src="file:///abs/path/foo.png"
    src="/abs/path/foo.png"
    src="../relative/path/foo.png"
    src="assets/avatars/01.png"
"""

import base64
import os
import re
import sys
from pathlib import Path

MIME_BY_EXT = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
}


def to_data_uri(path: str) -> str:
    ext = Path(path).suffix.lower()
    mime = MIME_BY_EXT.get(ext)
    if not mime:
        return None
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{data}"


def resolve_path(ref: str, html_dir: str) -> str:
    """Try to resolve a src reference to an absolute filesystem path."""
    if ref.startswith("file://"):
        ref = ref[len("file://"):]
    if ref.startswith("data:"):
        return None
    if os.path.isabs(ref):
        return ref if os.path.exists(ref) else None
    # relative to HTML file
    candidate = os.path.normpath(os.path.join(html_dir, ref))
    return candidate if os.path.exists(candidate) else None


def inline_html(input_path: str, output_path: str) -> tuple[int, int, int]:
    """Returns (replaced, missing, unchanged)."""
    html = open(input_path).read()
    html_dir = os.path.dirname(os.path.abspath(input_path))
    cache: dict[str, str] = {}
    stats = {"replaced": 0, "missing": 0, "unchanged": 0}

    def repl(m: re.Match) -> str:
        full = m.group(0)
        ref = m.group(1)
        abs_path = resolve_path(ref, html_dir)
        if not abs_path:
            print(f"  ⚠️  MISSING: {ref}", file=sys.stderr)
            stats["missing"] += 1
            return full
        if abs_path not in cache:
            uri = to_data_uri(abs_path)
            if not uri:
                stats["unchanged"] += 1
                return full
            cache[abs_path] = uri
        stats["replaced"] += 1
        return f'src="{cache[abs_path]}"'

    new_html = re.sub(r'src="([^"]+)"', repl, html)
    with open(output_path, "w") as f:
        f.write(new_html)
    return stats["replaced"], stats["missing"], stats["unchanged"]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"input not found: {input_path}", file=sys.stderr)
        return 1
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        stem, ext = os.path.splitext(input_path)
        output_path = f"{stem}-inline{ext}"

    replaced, missing, unchanged = inline_html(input_path, output_path)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ inlined: {replaced} refs → {output_path} ({size_kb:.1f} KB)")
    if missing:
        print(f"⚠️  {missing} reference(s) could not be resolved")
    if unchanged:
        print(f"ℹ️  {unchanged} reference(s) had unsupported extensions (left as-is)")
    return 0 if missing == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
