import os
import re
from openai import AzureOpenAI # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
  api_version=os.getenv("AZURE_API_VERSION")
)

directory = '../../datasets/cleaned_data/'
output_directory = '../../datasets/gpt_cot_annotated/'

os.makedirs(output_directory, exist_ok=True)

# abbreviations = [
#     'CLA',  # Clarity of Review
#     'JUS',  # Justification of Scores
#     'DEP',  # Depth of Analysis
#     'FAI',  # Fairness and Objectivity
#     'CON',  # Constructiveness of Feedback
#     'ENG',  # Engagement with Related Work
#     'ACC',  # Accuracy in Understanding
#     'CST',  # Consistency of Evaluation
#     'NOV',  # Identification of Novelty
#     'ETH'   # Ethical Considerations and Responsibility
# ]

def generate_annotations(review_text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant tasked with annotating peer reviews based on 10 specific questions. "
                    "Here is the mapping of the questions to abbreviations:\n"
                    "'Clarity of Review' -> 'CLA'\n"
                    "'Justification of Scores' -> 'JUS'\n"
                    "'Depth of Analysis' -> 'DEP'\n"
                    "'Fairness and Objectivity' -> 'FAI'\n"
                    "'Constructiveness of Feedback' -> 'CON'\n"
                    "'Engagement with Related Work' -> 'ENG'\n"
                    "'Accuracy in Understanding' -> 'ACC'\n"
                    "'Consistency of Evaluation' -> 'CST'\n"
                    "'Identification of Novelty' -> 'NOV'\n"
                    "'Ethical Considerations and Responsibility' -> 'ETH'\n"
                    "Please use Chain of Thought reasoning when providing the answers, carefully considering "
                    "the content of the review to decide on each question."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Here is the peer review text:\n\n{review_text}\n\n"
                    "Please provide the annotations in the following format: [[CLA-POS],[JUS-POS],[DEP-NEG],[FAI-NEG],[CON-POS],[ENG-NEG],[ACC-POS],[CST-POS],[NOV-NEG],[ETH-POS]].\n"
                    "Use Chain of Thought reasoning for each question, and decide whether the review is positive or negative for each question."
                )
            }
        ]
    )
    
    gpt_response = response.choices[0].message.content
    return gpt_response


def extract_annotations(text):

    pattern = r'\[\[\s*(.*?)\s*\]\]' 
    matches = re.findall(pattern, text)

    formatted = ''
    
    for match in matches:
        for i in match:
            if i == ' ':
                continue
            else:
                formatted += i

    return f"[[{formatted}]]"

processed_files = 0
max_files = 45

for filename in os.listdir(directory):
    if processed_files >= max_files:
        break
    
    if filename.endswith('.txt'):

        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            review_content = file.read()

        response = generate_annotations(review_content)
        annotations = extract_annotations(response)

        print(annotations)

        new_filename = filename.replace('.txt', '_annotated.txt')
        new_file_path = os.path.join(output_directory, new_filename)

        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(f"{review_content[2:-1]}{annotations}")
        
        processed_files += 1
        print(f"Annotated: {new_filename}")

print(f"Total files annotated: {processed_files}")
