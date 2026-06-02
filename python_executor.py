import subprocess
import tempfile
import os
import shutil

TIME_LIMIT = 5

# Find the correct Python binary cross-platform
# Windows uses "python", Linux/macOS use "python3"
PYTHON_CMD = (
    shutil.which("python3") or
    shutil.which("python") or
    "python"
)


def run_python_code(source_code: str, input_data: str = "") -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        py_file = os.path.join(tmpdir, "main.py")

        with open(py_file, "w", encoding="utf-8") as f:
            f.write(source_code)

        try:
            run_proc = subprocess.run(
                [PYTHON_CMD, py_file],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=TIME_LIMIT
            )

            if run_proc.returncode != 0:
                return {
                    "status": "runtime_error",
                    "error": run_proc.stderr.strip()
                }

            return {
                "status": "success",
                "output": run_proc.stdout.strip(),
                "stderr": run_proc.stderr.strip()
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": f"Time limit exceeded ({TIME_LIMIT}s)"
            }
