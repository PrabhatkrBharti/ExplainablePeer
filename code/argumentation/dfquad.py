import pandas as pd
import networkx as nx
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CRITERIA = ['CLA', 'JUS', 'DEP', 'FAI', 'CON', 'ENG', 'ACC', 'CST', 'NOV', 'ETH']
POS_CRITERIA = [f"{criterion}-POS" for criterion in CRITERIA]
NEG_CRITERIA = [f"{criterion}-NEG" for criterion in CRITERIA]
WEIGHTS = {'POS': 1, 'NEG': -1}
SUPPORT_RELATIONS = [(a, b) for lst in [POS_CRITERIA, NEG_CRITERIA] for a in lst for b in lst if a != b]
ATTACK_RELATIONS = [(a, b) for a in POS_CRITERIA for b in NEG_CRITERIA]

def add_relations(G, arguments):
    for arg1 in arguments:
        for arg2 in arguments:
            if (arg1, arg2) in ATTACK_RELATIONS:
                G.add_edge(arg1, arg2, relation='attacks')
            elif (arg1, arg2) in SUPPORT_RELATIONS:
                G.add_edge(arg1, arg2, relation='supports')

def evaluate_df_quad(G):
    support_value = sum(WEIGHTS['POS'] for node in G.nodes if 'POS' in node)
    attack_value = sum(WEIGHTS['NEG'] for node in G.nodes if 'NEG' in node)
    final_score = support_value + attack_value
    return final_score, support_value, attack_value

def five_level_scoring(df_quad_score, thresholds=(3, 1, 0, -1)):
    excellent, good, moderate, bad = thresholds
    if df_quad_score >= excellent:
        return "excellent"
    elif df_quad_score >= good:
        return "good"
    elif df_quad_score >= moderate:
        return "moderate"
    elif df_quad_score >= bad:
        return "bad"
    else:
        return "terrible"

def process_dataset(dataset_path, output_dir):
    df = pd.read_csv(dataset_path)
    df.columns = ['Index', 'Text', 'CLA', 'JUS', 'DEP', 'FAI', 'CON', 'ENG', 'ACC', 'CST', 'NOV', 'ETH']
    G = nx.DiGraph()

    df["DF_QuAD_Score"] = 0
    df["Five_Level_Score"] = ""
    df["Support_Value"] = 0
    df["Attack_Value"] = 0

    for idx, row in df.iterrows():
        G.clear()
        arguments = [f"{row[criterion]}" for criterion in CRITERIA]
        G.add_nodes_from(arguments)
        add_relations(G, arguments)

        df_quad_score, support_value, attack_value = evaluate_df_quad(G)
        df.at[idx, "DF_QuAD_Score"] = df_quad_score
        df.at[idx, "Five_Level_Score"] = five_level_scoring(df_quad_score)
        df.at[idx, "Support_Value"] = support_value
        df.at[idx, "Attack_Value"] = attack_value

    output_file = os.path.join(output_dir, f"results_df_quad_{os.path.basename(dataset_path).split('.')[0]}.csv")
    df.to_csv(output_file, index=False)
    logging.info(f"Processed dataset saved to {output_file}")

datasets = ['../results/transformed/transformed_manually_annotated.csv', '../results/transformed/transformed_gpt_annotated.csv', '../results/transformed/transformed_llama_annotated.csv', '../results/transformed/transformed_gemini_annotated.csv', '../results/transformed/transformed_mistral_annotated.csv']
output_directory = "../results/df_quad_results/"
os.makedirs(output_directory, exist_ok=True)

for dataset in datasets:
    process_dataset(dataset, output_directory)
