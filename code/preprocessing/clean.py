import os
import re

source_directory = '../../datasets/raw_data/'
destination_directory = '../../datasets/cleaned_data/'
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

annotation_pattern = r'\[\[.*?\]\]'

processed_files = 0
max_files = 910

for filename in os.listdir(source_directory):
    if processed_files >= max_files:
        break
    
    if filename.endswith('.txt'):
        file_path = os.path.join(source_directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        cleaned_content = re.sub(annotation_pattern, '', content)

        match = re.search(r'(.*R[123])', filename)
        new_filename = match.group(1) + '.txt'

        new_file_path = os.path.join(destination_directory, new_filename)
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(cleaned_content)

        processed_files += 1
        print(f"Old File name: {filename}")
        print(f"New File name: {new_filename}")

print(f"Total files processed: {processed_files}")
