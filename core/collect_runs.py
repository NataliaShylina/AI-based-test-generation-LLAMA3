from pathlib import Path
import json


def collect_test_counts(base_dir):
    base = Path(base_dir)
    files = sorted(base.glob("*.json"))

    return [len(json.load(open(f))["tests"]) for f in files]