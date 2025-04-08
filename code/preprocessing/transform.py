import pandas as pd

datasets = ['../../analysis/preprocessed/manually_annotated.csv', '../../analysis/preprocessed/gpt_annotated.csv', '../../analysis/preprocessed/llama_annotated.csv', '../../analysis/preprocessed/gemini_annotated.csv', '../../analysis/preprocessed/mistral_annotated.csv']
column_mapping = {
    "Clarity of Review": "CLA",
    "Justification of Scores": "JUS",
    "Depth of Analysis": "DEP",
    "Fairness and Objectivity": "FAI",
    "Constructiveness of Feedback": "CON",
    "Engagement with Related Work": "ENG",
    "Accuracy in Understanding": "ACC",
    "Consistency of Evaluation": "CST",
    "Identification of Novelty": "NOV",
    "Ethical Considerations and Responsibility": "ETH"
}

for df in datasets:
    dataset = pd.read_csv(df, index_col='Index')
    dataset = dataset.rename(columns=column_mapping)
    for i,row in dataset.iterrows():
        for col in dataset.columns[2:]: 
            dataset.loc[i, col] = f"{col}-POS" if row[col] == 1 else f"{col}-NEG"
    dataset.to_csv("../results/transformed/transformed_" + df[len("../../analysis/preprocessed/"):])
