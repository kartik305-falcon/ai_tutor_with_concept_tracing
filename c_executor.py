import subprocess
import tempfile
import os

TIME_LIMIT = 2  # seconds


def run_c_code(source_code, input_data=""):
    with tempfile.TemporaryDirectory() as tmpdir:
        c_file = os.path.join(tmpdir, "main.c")
        exe_file = os.path.join(tmpdir, "prog.exe")

        # Write C source
        with open(c_file, "w") as f:
            f.write(source_code)

        # Compile
        compile_cmd = [
            "gcc",
            c_file,
            "-o", exe_file,
            "-std=c11",
            "-Wall",
            "-Wextra",
            "-O0"
        ]

        compile_proc = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True
        )

        if compile_proc.returncode != 0:
            return {
                "status": "compile_error",
                "error": compile_proc.stderr
            }

        # Run with timeout
        try:
            run_proc = subprocess.run(
                [exe_file],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=TIME_LIMIT
            )

            return {
                "status": "success",
                "output": run_proc.stdout.strip(),
                "stderr": run_proc.stderr.strip()
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": "Time limit exceeded"
            }
