"""
Run the complete BahaPredict data pipeline.
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"

PIPELINE_STEPS = [
    "ingest.py",
    "transform.py",
    "run_queries.py",
    "generate_stakeholder_reports.py",
]


def run_pipeline():
    """Execute all pipeline scripts in sequence."""

    print("=" * 60)
    print("BAHAPREDICT - AUTOMATED DATA PIPELINE")
    print("=" * 60)

    for script in PIPELINE_STEPS:
        script_path = SCRIPTS_DIR / script

        if not script_path.exists():
            raise FileNotFoundError(f"Pipeline script not found: {script_path}")

        print(f"\nRunning: {script}")
        print("-" * 60)

        subprocess.run(
            [sys.executable, str(script_path)],
            cwd=BASE_DIR,
            check=True,
        )

        print(f"Completed: {script}")

    print("\n" + "=" * 60)
    print("BAHAPREDICT PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
