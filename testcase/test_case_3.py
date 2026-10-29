import subprocess
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "bus_pass.py"

with tempfile.TemporaryDirectory() as folder:
    workdir = Path(folder)

    old_pass = (
        "BP101 | Riya | Route 5 | Monthly | 500 | General "
        "| 2026-10-01 | 2026-10-31\n"
    )

    (workdir / "buspass.txt").write_text(
        old_pass, encoding="utf-8"
    )

    inputs = (
        "1\n"
        "Aman\n"
        "Route 7\n"
        "Yearly\n"
        "Student\n"
        "3\n"
        "BP101\n"
        "5\n"
    )

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
    assert "BP102" in output, output
    assert "Aman" in output, output
    assert "Rs. 3600" in output, output
    assert "Riya" in output, output
    assert "Route 5" in output, output
    assert "Rs. 500" in output, output

    print("TEST CASE 4: PASS")
    print("Expected: Aman pass issued; Riya pass searched")
    print("Actual: Both operations verified")