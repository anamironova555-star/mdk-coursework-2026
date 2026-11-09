import argparse
import statistics
import subprocess
import sys
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--jq", default="jq")
args = parser.parse_args()
path = Path(__file__).resolve().parent / "data/users.json"
for name, command in [
    (
        "Python",
        [
            sys.executable,
            "-c",
            'import json,sys; json.load(open(sys.argv[1],encoding="utf-8"))',
            str(path),
        ],
    ),
    ("jq", [args.jq, "empty", str(path)]),
]:
    values = []
    for _ in range(20):
        started = time.perf_counter()
        subprocess.run(command, check=True, capture_output=True)
        values.append((time.perf_counter() - started) * 1000)
    print(f"{name}: median of 20 process starts = {statistics.median(values):.3f} ms")
