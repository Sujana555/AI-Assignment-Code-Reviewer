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
                    You are a professor grading a student's assignment solution. You will be given Assignment Description, Rubric, Assignment
                    Solution.
                    
                    Your job:
                    1. Read and understand the assignment description to understand what is being expected.
                    2. Go through each and every Rubric item one by one.
                    3. Check the student's assignment solution against every rubric item.
                    4. Check whether the logic would produce correct results for the test cases mentioned 
                        in the assignment description
                    5. Assign a score for each rubric item based on its weight
                    
                    
                    Give me a string with the assignment score.
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