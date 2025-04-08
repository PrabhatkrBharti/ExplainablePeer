import pandas as pd

def combine_csvs_with_source(file_paths):
  df_list = []
  for file_path in file_paths:
    df = pd.read_csv(file_path)
    df['Source'] = file_path[12 : -14]
    df_list.append(df)

  combined_df = pd.concat(df_list, ignore_index=True)
  return combined_df

file_paths = [
  '../results/transformed/transformed_gemini_annotated.csv',
  '../results/transformed/transformed_gpt_annotated.csv',
  '../results/transformed/transformed_mistral_annotated.csv',
  '../results/transformed/transformed_llama_annotated.csv',
  '../results/transformed/transformed_manually_annotated.csv'
]

combined_df = combine_csvs_with_source(file_paths)
combined_df.to_csv('../results/combined/combined_data.csv', index=False)