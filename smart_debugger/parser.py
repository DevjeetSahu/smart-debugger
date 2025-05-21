import re
from typing import List, Dict, Tuple

def parse_error_log(log_path: str) -> Tuple[List[Dict], str]:
    with open(log_path, 'r') as f:
        lines = f.readlines()

    stack = []
    error_msg = ""

    # Regex for JS stack frame lines, e.g.
    # at exports.createRoot (react-dom_client.js?v=6ebce59c:17994:17)
    # at main.jsx:6:1
    pattern = re.compile(
        r'^\s*at\s+(?:(?P<func>.*?)\s+\()?((?P<file>.*?):(?P<line>\d+):(?P<col>\d+))\)?$'
    )

    for i, line in enumerate(lines):
        line = line.rstrip('\n')
        if i == 0:
            # First line is usually the error message
            error_msg = line.strip()
            continue

        match = pattern.match(line)
        if match:
            func = match.group('func') or "<anonymous>"
            file_path = match.group('file')
            line_number = int(match.group('line'))
            # You can capture column if needed: col = int(match.group('col'))
            stack.append({
                "file": file_path,
                "line": line_number,
                "function": func
            })
        else:
            # Print debug info for lines that don't match
            print(f"[DEBUG] No match for stack line: {line}")

    if not stack:
        print("[WARN] No stack frames parsed from the log.")

    if not error_msg:
        print("[WARN] No error message found in the log.")

    return stack, error_msg
