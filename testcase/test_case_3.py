import subprocess
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "bus_pass.py"

with tempfile.TemporaryDirectory() as folder:
    workdir = Path(folder)

    inputs = "1\nAman\nRoute 7\nWeekly\nGeneral\n5\n"

    result = subprocess.run(
        [sys.executable, str(APP)],
        input=inputs,
        capture_output=True,
        text=True,
        cwd=workdir,
        timeout=10
    )

    output = result.stdout

    assert result.returncode == 0, result.stderr
    assert "ERROR: Invalid pass type." in output, output
    assert "SUCCESS: Pass issued." not in output, output

    print("TEST CASE 3: PASS")
    print("Expected: Invalid pass type error")
    print("Actual: Invalid pass type error")