import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

baf_results_path = "../results/baf_results/"
df_quad_results_path = "../results/df_quad_results/"

def load_results(directory):
    all_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]
    return pd.concat([pd.read_csv(file) for file in all_files[:1]], ignore_index=True)

baf_results = load_results(baf_results_path)
df_quad_results = load_results(df_quad_results_path)

def evaluate_baf_results(df):
    summary = df.groupby("Majority_Voting_Score").size().reset_index(name="Count")
    print("\nBAF Majority Voting Results:\n", summary)

    summary = df.groupby("All_Accept_Score").size().reset_index(name="Count")
    print("\nBAF All Accept Voting Results:\n", summary)

def evaluate_df_quad_results(df):
    score_summary = df["Five_Level_Score"].value_counts().reset_index()
    score_summary.columns = ["Score Level", "Count"]
    print("\nDF-QuAD Five-Level Score Distribution:\n", score_summary)

    print("\nDF-QuAD Support and Attack Values Summary:\n")
    print(df[["Support_Value", "Attack_Value"]].describe())

def plot_baf_results(df):
    majority_counts = df["Majority_Voting_Score"].value_counts()
    majority_counts.plot(kind='bar', color=['blue', 'orange'], title="BAF Majority Voting Results")
    plt.xlabel("Score")
    plt.ylabel("Number of Reviews")
    plt.show()

    all_accept_counts = df["All_Accept_Score"].value_counts()
    all_accept_counts.plot(kind='bar', color=['blue', 'orange'], title="BAF All Accept Voting Results")
    plt.xlabel("Score")
    plt.ylabel("Number of Reviews")
    plt.show()

def plot_df_quad_results(df):
    sns.countplot(data=df, x="Five_Level_Score", order=["excellent", "good", "moderate", "bad", "terrible"], palette="viridis")
    plt.title("DF-QuAD Five-Level Score Distribution")
    plt.xlabel("Score Level")
    plt.ylabel("Count")
    plt.show()

    df[["Support_Value", "Attack_Value"]].boxplot()
    plt.title("Box Plot of Support and Attack Values")
    plt.ylabel("Value")
    plt.show()

    plt.scatter(df["Support_Value"], df["Attack_Value"], alpha=0.6, c='purple')
    plt.title("Scatter Plot of Support vs. Attack Values")
    plt.xlabel("Support Value")
    plt.ylabel("Attack Value")
    plt.grid()
    plt.show()

evaluate_baf_results(baf_results)
plot_baf_results(baf_results)

evaluate_df_quad_results(df_quad_results)
plot_df_quad_results(df_quad_results)
