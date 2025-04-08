import os
import re
import time
from groq import Groq # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

client = Groq()
model = "mixtral-8x7b-32768"

directory = '../../datasets/cleaned_data/'
output_directory = '../../datasets/mixtral_annotated/'
os.makedirs(output_directory, exist_ok=True)

questions = {
    'CLA': "Is the review clearly articulated, providing a structured and understandable assessment of the paper?",
    'JUS': "Does the review provide sound reasoning or evidence for the given scores (e.g., for clarity, originality, significance)?",
    'DEP': "Does the review engage deeply with the content of the paper, discussing strengths and weaknesses in detail rather than superficially?",
    'FAI': "Is the review impartial and free from bias? Does it avoid making unsubstantiated or overly subjective claims?",
    'CON': "Does the review offer constructive criticism and useful suggestions to improve the paper, beyond just pointing out flaws?",
    'ENG': "Does the reviewer appropriately discuss the paper’s positioning relative to other related works, if applicable?",
    'ACC': "Does the reviewer demonstrate a correct and thorough understanding of the paper's contributions, methods, and results?",
    'CST': "Are the points made in the review consistent with the final recommendation (e.g., reject, accept, revise)?",
    'NOV': "Does the review acknowledge and adequately assess the originality of the work, including any novel aspects of the methodology or findings?",
    'ETH': "Does the review consider ethical aspects where relevant, such as reproducibility, responsible AI, or proper citation of others’ work?"
}

def generate_annotation_for_question(review_text):
    prompt = (
        f"You are an assistant tasked with annotating peer reviews. Consider that these peer reviews are from ICLR so most of them will be from competent and experienced reviewers. Output in less than 100 words."
        f"Here is the peer review text:\n\n{review_text}\n\n"
        f"Please answer the following questions: {questions.values()}\n\n"
        f"Use the format [CODE-POS] or [CODE-NEG] where code is one of {questions.keys()}. Give annotations as NEG (negative) if not evidence is present for positive or negative score although do try to avoid this as much as possible."
    )
    
    attempt, max_retries, retry_delay = 0, 3, 20
    while attempt < max_retries:
        try:
            chat_response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            )
            response_text = chat_response.choices[0].message.content
            return response_text
        except Exception as e:
            attempt += 1
            print(f"Error: {e}. Attempt {attempt} of {max_retries}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    print("Failed to generate content after multiple retries.")
    return "None"

def extract_annotations(annotation_text):
    question_codes = ['CLA', 'JUS', 'DEP', 'FAI', 'CON', 'ENG', 'ACC', 'CST', 'NOV', 'ETH']
    annotations_list = []

    for code in question_codes:
        pattern = fr'{code}-\w{{3}}'
        match = re.search(pattern, annotation_text)
        if match:
            annotations_list.append(f"[{match.group(0)}]")
        else:
            annotations_list.append(f"[{code}-NEG]")

    final_annotations = f"[{','.join(annotations_list)}]"
    return final_annotations

processed_files = 0
max_files = 905

for filename in os.listdir(directory):
    if processed_files >= max_files:
        break
    
    if filename.endswith('.txt'):

        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            review_content = file.read()

        response = generate_annotation_for_question(review_content)
        annotations = extract_annotations(response)

        new_filename = filename.replace('.txt', '_annotated.txt')
        new_file_path = os.path.join(output_directory, new_filename)

        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(f"{review_content[2:-1]}{annotations}")
        
        processed_files += 1

        print(f"Annotated: {new_filename}")
        print(annotations)

        if processed_files % 50 == 0:
            print(f"\nProcessed {processed_files} files!\n")

print(f"Total files annotated: {processed_files}")
