import json
from pathlib import Path
from datetime import date

ASSIGNMENTS_DIR = Path(__file__).resolve().parents[3] / "data" / "assignments"


def save_assignment(file_path: str, extracted_text: str):
    ASSIGNMENTS_DIR.mkdir(parents=True, exist_ok=True)

    assignment = {
        "name": Path(file_path).name,
        "saved_at": str(date.today()),
        "file_path": str(file_path),
        "extracted_text": extracted_text
    }

    json_path = ASSIGNMENTS_DIR / (Path(file_path).stem + ".json")
    json_path.write_text(json.dumps(assignment, indent=2))
    print(f"Saved to: {json_path}")