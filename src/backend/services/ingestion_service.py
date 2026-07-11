
from src.backend.parsers import document_parser
from src.backend.repository import  assignment_stub
def save_to_memory(file_path: str, extracted_text: str):
    assignment_stub.save_assignment(file_path, extracted_text)

if __name__ == "__main__":
#     get input from the user.
    file_path = input("Enter file path: ")
    text = document_parser.extract_text(file_path)
    save_to_memory(file_path, text)

