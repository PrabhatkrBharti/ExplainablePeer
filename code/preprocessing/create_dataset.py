import os
import re
import pandas as pd

def extract_text_and_annotations(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    annotations_pattern = r'\[\[(.*?)\]\]'
    annotations_match = re.search(annotations_pattern, content)

    if annotations_match:
        annotations = annotations_match.group(1).split(',')
        annotations = [ann.strip('[]') for ann in annotations]
        cleaned_content = re.sub(annotations_pattern, '', content).strip()
    else:
        annotations = [''] * 10  
        cleaned_content = content.strip()

    annotation_dict = dict(zip(annotation_keys, annotations))
    return cleaned_content, annotation_dict

data = []
directory = '../../datasets/suggested_gpt_annotated/'
annotation_keys = ['CLA', 'JUS', 'DEP', 'FAI', 'CON', 'ENG', 'ACC', 'CST', 'NOV', 'ETH']

for filename in os.listdir(directory):
    if filename.endswith('.txt'):

        index_pattern = r'ICLR2018-(.*?)_annotated\.txt'
        index_match = re.search(index_pattern, filename)
        index = index_match.group(1) if index_match else None 

        file_path = os.path.join(directory, filename)
        text_content, annotations = extract_text_and_annotations(file_path)

        data.append({'Index': index, 'Text': text_content, **annotations})

df = pd.DataFrame(data)
df.to_csv('../../datasets/preprocessed_datasets/gpt_annotations.csv', index=False)
