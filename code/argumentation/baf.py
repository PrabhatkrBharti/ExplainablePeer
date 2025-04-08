import pandas as pd
import networkx as nx
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CRITERIA = ['CLA', 'JUS', 'DEP', 'FAI', 'CON', 'ENG', 'ACC', 'CST', 'NOV', 'ETH']
POS_CRITERIA = [f"{criterion}-POS" for criterion in CRITERIA]
NEG_CRITERIA = [f"{criterion}-NEG" for criterion in CRITERIA]
SUPPORT_RELATIONS = [(a, b) for lst in [POS_CRITERIA, NEG_CRITERIA] for a in lst for b in lst if a != b]
ATTACK_RELATIONS = [(a, b) for a in POS_CRITERIA for b in NEG_CRITERIA]

def add_relations(G, arguments):
    for arg1 in arguments:
        for arg2 in arguments:
            if (arg1, arg2) in ATTACK_RELATIONS:
                G.add_edge(arg1, arg2, relation='attacks')
            elif (arg1, arg2) in SUPPORT_RELATIONS:
                G.add_edge(arg1, arg2, relation='supports')

def evaluate_review(G, choice):
    pos_count = sum(1 for node in G.nodes if 'POS' in node)
    neg_count = sum(1 for node in G.nodes if 'NEG' in node)
    if choice == 'majority voting':
        return "good" if pos_count > neg_count else "bad"
    elif choice == 'all accept':
        return "good" if neg_count == 0 else "bad"

def process_dataset(dataset_path, output_dir):
    df = pd.read_csv(dataset_path)
    df.columns = ['Index', 'Text', 'CLA', 'JUS', 'DEP', 'FAI', 'CON', 'ENG', 'ACC', 'CST', 'NOV', 'ETH']
    G = nx.DiGraph()

    df["Majority_Voting_Score"] = ""
    df["All_Accept_Score"] = ""

    for idx, row in df.iterrows():
        G.clear()
        arguments = [f"{row[criterion]}" for criterion in CRITERIA]
        G.add_nodes_from(arguments)
        add_relations(G, arguments)

        df.at[idx, "Majority_Voting_Score"] = evaluate_review(G, 'majority voting')
        df.at[idx, "All_Accept_Score"] = evaluate_review(G, 'all accept')

    output_file = os.path.join(output_dir, f"results_baf_{os.path.basename(dataset_path).split('.')[0]}.csv")
    df.to_csv(output_file, index=False)
    logging.info(f"Processed dataset saved to {output_file}")

datasets = ['../results/transformed/transformed_manually_annotated.csv', '../results/transformed/transformed_gpt_annotated.csv', '../results/transformed/transformed_llama_annotated.csv', '../results/transformed/transformed_gemini_annotated.csv', '../results/transformed/transformed_mistral_annotated.csv']
output_directory = "../results/transformed/baf_results/"
os.makedirs(output_directory, exist_ok=True)

for dataset in datasets:
    process_dataset(dataset, output_directory)
