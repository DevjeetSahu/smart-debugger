from typing import List, Dict
import os
import re

def find_file_in_codebase(codebase_root: str, file_name: str) -> str:
    """
    Search recursively for the file inside codebase_root.
    Returns full path if found, else empty string.
    """
    # Remove query params or fragments from filename (e.g. "?v=1234")
    base_name = re.split(r'[?#]', file_name)[0]

    # Check direct path first
    direct_path = os.path.normpath(os.path.join(codebase_root, base_name))
    if os.path.isfile(direct_path):
        return direct_path

    # Recursively search for the file
    for root, dirs, files in os.walk(codebase_root):
        if base_name in files:
            return os.path.join(root, base_name)

    return ""  # Not found


def extract_code_context(stack: List[Dict], codebase_root: str, radius: int = 5) -> List[Dict]:
    context = []

    for frame in stack:
        file_path = find_file_in_codebase(codebase_root, frame['file'])

        if not file_path:
            print(f"[WARN] File not found anywhere in codebase: {frame['file']}")
            context.append({
                "file": frame["file"],
                "line": frame["line"],
                "snippet": "[File not found]"
            })
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            error_line = frame["line"]
            start = max(0, error_line - radius - 1)
            end = min(len(lines), error_line + radius)

            snippet = "".join(lines[start:end])
            context.append({
                "file": frame["file"],
                "line": error_line,
                "snippet": snippet
            })
        except Exception as e:
            print(f"[ERROR] Could not read file {file_path}: {e}")
            context.append({
                "file": frame["file"],
                "line": frame["line"],
                "snippet": f"[Error reading file: {e}]"
            })

    return context
