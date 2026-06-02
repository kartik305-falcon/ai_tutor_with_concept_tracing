import subprocess
import tempfile
import os
import re
import shutil
import sys

TIME_LIMIT = 10  # seconds


def _extract_class_name(source_code: str) -> str:
    """Extracts the public class name. Falls back to 'Main'."""
    match = re.search(r'public\s+class\s+(\w+)', source_code)
    return match.group(1) if match else "Main"


def _find_compiler():
    """
    Returns (compile_cmd_list, java_cmd) or (None, java_cmd).
    Works on Windows, macOS, and Linux.
    """
    # shutil.which works cross-platform (Windows, macOS, Linux)
    javac_path = shutil.which("javac")
    java_path = shutil.which("java") or "java"

    if javac_path:
        return [javac_path], java_path

    # No javac binary — try jdk.compiler module embedded in the JRE (OpenJDK 9+)
    try:
        test = subprocess.run(
            [java_path, "--add-modules", "jdk.compiler",
             "com.sun.tools.javac.Main", "--version"],
            capture_output=True, text=True, timeout=10
        )
        if test.returncode == 0:
            return (
                [java_path, "--add-modules", "jdk.compiler",
                 "com.sun.tools.javac.Main"],
                java_path
            )
    except Exception:
        pass

    return None, java_path


JAVAC_CMD, JAVA_CMD = _find_compiler()


def run_java_code(source_code: str, input_data: str = "") -> dict:
    if JAVAC_CMD is None:
        return {
            "status": "compile_error",
            "error": (
                "No Java compiler (javac) found on this system.\n"
                "Please install the JDK:\n"
                "  Windows: https://adoptium.net  or  winget install EclipseAdoptium.Temurin.21.JDK\n"
                "  macOS:   brew install openjdk\n"
                "  Linux:   sudo apt install default-jdk"
            )
        }

    class_name = _extract_class_name(source_code)

    with tempfile.TemporaryDirectory() as tmpdir:
        java_file = os.path.join(tmpdir, f"{class_name}.java")

        with open(java_file, "w", encoding="utf-8") as f:
            f.write(source_code)

        # Compile
        compile_cmd = JAVAC_CMD + [java_file, "-d", tmpdir]
        compile_proc = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            cwd=tmpdir
        )

        if compile_proc.returncode != 0:
            error_msg = compile_proc.stderr.strip()
            error_msg = error_msg.replace(tmpdir + os.sep, "")
            error_msg = error_msg.replace(tmpdir + "/", "")
            return {
                "status": "compile_error",
                "error": error_msg
            }

        # Run
        try:
            run_proc = subprocess.run(
                [JAVA_CMD, "-cp", tmpdir, class_name],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=TIME_LIMIT,
                cwd=tmpdir
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
