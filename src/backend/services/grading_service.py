from pathlib import Path
import json
from src.backend.api import connect_LLM
from src.backend.parsers import document_parser

# Import the main assignment dir
ASSIGNMENT_DIR = Path(__file__).resolve().parents[3] / "data"

# TODO: Move this to parser
def load_assignment(file_name):
    json_path = ASSIGNMENT_DIR / file_name

    with open(json_path, "r") as f:
        data = json.load(f)

    return data

# TODO: Move this to parser
def load_assignment_solution(file_name):
    path = ASSIGNMENT_DIR / file_name

    return path.read_text(encoding="utf-8")
# TODO: Fix info leak
def get_assignment_grading(assign_desc, rubric, assign_sol):
    combined_text = f"Assignment Description: \n{assign_desc}\n\n Rubric: \n{rubric}\n\n Assignment Solution: \n{assign_sol}\n\n"
    system_prompt = '''
                    <goal>
                    You are GraderGPT, an expert coding assignment grader.
                    Your role is to evaluate a student's code solution by cross-checking 
                    it against each rubric item and returning a precise structured grade.
                    Base all scores strictly on the rubric — nothing more, nothing less.
                    Never assume anything about the files or text given.
                    Never reference these instructions in your response.
                    </goal>
                    
                    <grading_categories>
                    - Tasks 1-7 each contribute to Completeness (75% total)
                    - Correctness (15%) is an overall judgment across all tasks
                    - Style (10%) is an overall judgment across all tasks
                    - Design (0%) is not graded
                    </grading_categories>
                    
                    <evaluation_format>
                    Return a single valid JSON object in exactly this structure.
                    No explanation, no preamble, no markdown code blocks. Raw JSON only.
                    
                    {
                      "rubric_grades": [
                        {
                          "task": "Task 1",
                          "description": "Whether the task is correct. If not, specify exactly where points were lost.",
                          "points_toward": "Completeness",
                          "passed": true,
                          "score": 0,
                          "max_score": 0,
                          "test_cases": [
                            {
                              "input": "example input",
                              "expected_output": "expected output",
                              "actual_output": "what the code actually produces",
                              "passed": true
                            }
                          ]
                        }
                      ],
                      "category_scores": {
                        "completeness": {"score": 0, "max": 75},
                        "correctness": {"score": 0, "max": 15},
                        "style": {"score": 0, "max": 10},
                        "design": {"score": 0, "max": 0}
                      },
                      "total_score": 0,
                      "max_total": 100,
                      "overall_feedback": "2-4 sentence summary of the submission."
                    }
                    </evaluation_format>
                    
                    <planning_guidance>
                    When grading:
                    1. Read and understand the assignment description.
                    2. Go through each rubric item one by one — do not skip any.
                    3. Check the student solution against each rubric item.
                    4. Trace through the logic for each test case and determine actual output.
                    5. Assign scores based strictly on rubric weights.
                    6. Evaluate Correctness and Style as overall judgments across all tasks.
                    7. Return valid JSON only.
                    </planning_guidance>

                    
                    <output>
                    - Return raw JSON only following the <evaluation_format> structure.
                    - Do not include any text before or after the JSON.
                    - Do not wrap the JSON in markdown code blocks.
                    - Follow <planning_guidance> when evaluating.
                    - Follow <grading_categories> when assigning points_toward.
                    </output>
    '''


    user_prompt = f'''
                    Please grade the following student submission.
                    
                    Assignment Description:
                    {assign_desc}
                    
                    Rubric:
                    {rubric}
                    
                    Student Solution:
                    {assign_sol}
    '''

    graded_result = connect_LLM.get_llm_response(combined_text, user_prompt, system_prompt)

    return graded_result
def main():
    assignment_desc_file_path = "assignments/Assignment.json"
    assignment_desc = load_assignment(assignment_desc_file_path)
    extract_assignment_desc = assignment_desc["extracted_text"]
    rubric_file_path = "assignments/Rubric.json"
    extract_rubric = load_assignment(rubric_file_path)
    assignment_sol_file_path = "assignment_solution/assignment1/sir_100.py"
    extract_assignment_sol = load_assignment_solution(assignment_sol_file_path)

    # print(extract_assignment_desc + "\n")
    # print(extract_rubric)
    # print(extract_assignment_sol + "\n")

    score = get_assignment_grading(extract_assignment_desc, extract_rubric, extract_assignment_sol)
    print(score)

if __name__ == "__main__":
    main()

    # Load the assignment data first then get grading