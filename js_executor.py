"""
js_executor.py
--------------
Feature 6: JavaScript Language Support.
Runs JavaScript code via Node.js subprocess.
Requires Node.js installed: https://nodejs.org
"""

import subprocess
import tempfile
import os
import sys

TIMEOUT = 10  # seconds


def run_js_code(source_code: str, stdin_input: str = "") -> dict:
    """
    Run JavaScript code using Node.js.

    Returns:
        {
            "status": "success" | "error" | "timeout",
            "output": str,
            "stderr": str,
            "error": str (only on failure)
        }
    """
    # Write source to a temp file
    tmp_file = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".js", delete=False, encoding="utf-8"
        ) as f:
            # Wrap stdin handling: replace process.argv input with readline simulation
            # Inject a simple stdin-to-readable-input shim
            shim = """
const _lines = `{stdin}`.split('\\n').filter(l => l.trim() !== '');
let _lineIdx = 0;

// Override readline-style input for simple programs
const _readline = () => _lines[_lineIdx++] || '';

// Make process.stdin.read() work via lines
""".format(stdin=stdin_input.replace("`", "\\`").replace("\\", "\\\\"))

            f.write(shim + "\n" + source_code)
            tmp_file = f.name

        # Determine node executable
        node_cmd = "node"
        if sys.platform == "win32":
            node_cmd = "node"  # assumes node is in PATH

        result = subprocess.run(
            [node_cmd, tmp_file],
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            encoding="utf-8",
            errors="replace"
        )

        if result.returncode == 0:
            return {
                "status": "success",
                "output": result.stdout,
                "stderr": result.stderr
            }
        else:
            return {
                "status": "error",
                "output": result.stdout,
                "stderr": result.stderr,
                "error": result.stderr or f"Node exited with code {result.returncode}"
            }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "output": "",
            "stderr": "",
            "error": f"Execution timed out after {TIMEOUT}s"
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "output": "",
            "stderr": "",
            "error": "Node.js not found. Please install Node.js from https://nodejs.org"
        }
    except Exception as e:
        return {
            "status": "error",
            "output": "",
            "stderr": "",
            "error": str(e)
        }
    finally:
        if tmp_file and os.path.exists(tmp_file):
            try:
                os.unlink(tmp_file)
            except Exception:
                pass
