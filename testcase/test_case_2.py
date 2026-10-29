import subprocess
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "bus_pass.py"

with tempfile.TemporaryDirectory() as folder:
    workdir = Path(folder)
    (workdir / "buspass.txt").write_text("", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(APP)],
        input="4\n5\n",
        capture_output=True,
        text=True,
        cwd=workdir,
        timeout=10
    )

    output = result.stdout

    assert result.returncode == 0, result.stderr
    assert "No passes issued yet." in output, output

    print("TEST CASE 2: PASS")
    print("Expected: No passes issued yet.")
    print("Actual: No passes issued yet.")