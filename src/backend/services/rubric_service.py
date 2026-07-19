from pathlib import Path

import json
from src.backend.api import connect_LLM
from src.backend.repository import rubric_stub

# Import the .json file to read and load data
ASSIGNMENT_DIR = Path(__file__).resolve().parents[3] / "data" / "assignments"

def load_assignment(file_name: str):
    json_path = ASSIGNMENT_DIR / file_name

    with open(json_path, "r") as f:
        data = json.load(f)

    return data

# TODO: Move the system and user prompts out of the method. It's taking up a lot of space.
def extract_rubric(file_name: str):
    assignment = load_assignment(file_name)

    extracted_assignment_text = assignment["extracted_text"]

#     write a system prompt & user instruction to send to llm
    system_prompt = '''
                    You are an expert at analyzing academic assignment descriptions and extracting 
                    grading criteria. Your job is to identify ALL rubric information from an 
                    assignment description, even when it is not explicitly labeled as a "rubric."
                    
                    Rubric information can appear as:
                    - Explicit grading weights or percentages
                    - A list of tasks or functions the student must implement
                    - Test cases with expected inputs and outputs
                    - Style or design requirements
                    
                    Always return your response as valid JSON only. No explanation, no preamble, 
                    no markdown code blocks. Just raw JSON.
                    '''
    user_prompt = '''
                    Extract the rubric from the following assignment description.

                    Return a JSON object in exactly this format:
                    {
                      "grading_categories": [
                        {
                          "category": "category name",
                          "weight_percent": 0,
                          "description": "what is being graded"
                        }
                      ],
                      "rubric_items": [
                        {
                          "task": "task name or number",
                          "description": "what the student must implement",
                          "points_toward": "which grading category this falls under",
                          "test_cases": [
                            {
                              "input": "example input",
                              "expected_output": "expected output"
                            }
                          ]
                        }
                      ]
                    }
                    
                    Assignment description:
                    {assignment_text}
    '''

    extracted_rubric = connect_LLM.get_llm_response(extracted_assignment_text, user_prompt, system_prompt)
    return extracted_rubric



if __name__ == "__main__":
    assignment_file_name = "Assignment.json"
    extract_rubric_text = extract_rubric(assignment_file_name)
    rubric_file_name = "Rubric.json"
    print(extract_rubric_text)
    rubric_stub.save_rubric(extract_rubric_text, rubric_file_name)



