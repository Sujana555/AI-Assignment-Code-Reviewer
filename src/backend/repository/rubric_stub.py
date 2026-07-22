import json
from pathlib import Path

ASSIGNMENTS_DIR = Path(__file__).resolve().parents[3] / "data" / "assignments"

def save_rubric(rubric_text, rubric_file_name):
    ASSIGNMENTS_DIR.mkdir(parents=True, exist_ok=True)

    rubric_json_path = ASSIGNMENTS_DIR / (Path(rubric_file_name).stem + ".json")
    rubric_json_data = json.loads(rubric_text)

    with open(rubric_json_path, "w") as f:
        json.dump(rubric_json_data, f, indent=2)
    print(f"Saved to: {rubric_json_path}")