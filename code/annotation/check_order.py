import os

cleaned_directory = '../../datasets/cleaned_data/'
annotated_directory = '../../datasets/manual_annotated/'

# Get sorted lists of files from each directory
# cleaned_files = sorted(os.listdir(cleaned_directory))
# annotated_files = sorted(os.listdir(annotated_directory))

cleaned_files = os.listdir(cleaned_directory)
annotated_files = os.listdir(annotated_directory)

cleaned_files_no_ext = [f.replace('.txt', '') for f in cleaned_files]
annotated_files_no_ext = [f.replace('_annotated.txt', '') for f in annotated_files]

missing_in_annotated = []
out_of_order_files = []

missing_in_annotated = [f for f in cleaned_files_no_ext if f not in annotated_files_no_ext]

for i, file in enumerate(cleaned_files_no_ext):
    if file in annotated_files_no_ext:
        annotated_index = annotated_files_no_ext.index(file)
        if annotated_index != i:
            out_of_order_files.append((file, i, annotated_index))

# if missing_in_annotated:
#     print("Files missing in annotated directory:", missing_in_annotated)
# else:
#     print("No files missing in annotated directory.")

if out_of_order_files:
    print("\nFiles out of order:")
    for file, cleaned_index, annotated_index in out_of_order_files:
        print(f"{file} - Expected index: {cleaned_index}, Found index in annotated: {annotated_index}")
else:
    print("No files out of order.")
