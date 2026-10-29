import subprocess
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "bus_pass.py"

with tempfile.TemporaryDirectory() as folder:
    workdir = Path(folder)

    inputs = "1\nRiya\nRoute 5\nMonthly\nGeneral\n5\n"

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
    assert "SUCCESS: Pass issued. ID: BP101" in output, output
    assert "Fee: Rs. 500.00" in output, output

    print("TEST CASE 1: PASS")
    print("Expected Fee: Rs. 500")
    print("Actual: Pass issued successfully")