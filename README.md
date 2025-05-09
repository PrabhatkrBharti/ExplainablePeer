# ArGU-LLM: Interpretable Scientific Peer Review Assessment via Argumentation-Guided LLMs

This repository provides the codebase, datasets, and analysis scripts for the paper "ArGU-LLM: Interpretable Scientific Peer Review Assessment via Argumentation-Guided LLMs." This reseach work presents a novel framework that utilizes argumentation theory to guide large language models (LLMs) in evaluating scientific peer reviews. ArGU-LLM assesses reviews across ten key evaluation criteria, enabling interpretable, consistent, and criterion-aligned review quality assessment. The approach is validated using multiple datasets annotated by both human experts and LLMs.

## Repository Structure

### 1. **analysis/**
Contains all scripts and notebooks for analyzing and visualizing data.

- **notebooks/**  
  Jupyter notebooks for data evaluation, qualitative/quantitative analysis, and argumentation results:
  - `1_data_evaluation.ipynb`  
  - `2_advanced_dataset_evaluation.ipynb`  
  - `3_qualitative.ipynb`  
  - `4_quantitative.ipynb`  
  - `5_advanced_quantitative.ipynb`  
  - `6_comp_arg_result_analysis.ipynb`  

- **preprocessed/**  
  Preprocessed datasets and scripts:  
  - `clean.py`: Cleans raw data.  
  - Annotated datasets (e.g., `gemini_annotated.csv`, `gpt_annotated.csv`, etc.).  

- **results/**  
  Stores result graphs and metrics:  
  - **arg_graphs/**: Argumentation graphs (e.g., `arg_graph.png`, `bfa_graph.png`).  
  - **metrics/**: Evaluation metrics like Cohen's Kappa (`cohen_kappa.png`).  

- **visualization/**  
  Tools for visualizing argumentation graphs:  
  - `argumentation_graph.html`  
  - `comp_arg_vis.py`  

---

### 2. **code/**
Code modules organized by tasks.

- **annotation/**  
  Scripts for annotating datasets:  
  - `annotate_gemini.py`, `annotate_gpt.py`, etc.  

- **argumentation/**  
  Argumentation models and transformations:  
  - `baf.py`: Bipolar Argumentation Framework (BAF).  
  - `dfquad.py`: DF-Quad semantics for argument analysis.  

- **evaluation/**  
  Tools for intra- and inter-model evaluations:  
  - `inter_model.ipynb`  
  - `intra_model.py`  

- **preprocessing/**  
  Scripts for cleaning, combining, and transforming datasets:  
  - `clean.py`, `combine.py`, `create_dataset.py`.  

- **results/**  
  Organized results for various analyses:  
  - **aggregated/**: Consolidated results (e.g., `all_models_annotated_reviews_dataset.csv`).  
  - **baf_results/** and **df_quad_results/**: Model-specific BAF/DF-Quad transformations.  
  - **combined/**: Combined analysis results (e.g., `combined_baf_data.csv`).  
  - **transformed/**: Transformed datasets for each model.  
  - **visualizations/**: Visualization outputs (e.g., `inter_model_A.png`).  

---

### 3. **diagrams/**
Visual diagrams of workflows and processes:  
- `flowchart.png`, `workflow.png`, `workflow2.png`.

---

### 5. **resources/**
Sample datasets and other resources:  
- `annotations_sample.csv`  
- `sample_data.csv`  

---

## Usage Instructions

### 1. **Preprocessing Datasets**
Run scripts in `code/preprocessing/` to clean and prepare datasets for analysis.

### 2. **Dataset Annotation**
Use annotation scripts in `code/annotation/` to generate model-specific annotations.

### 3. **Argumentation Analysis**
Run the argumentation scripts in `code/argumentation/` for BAF and DF-Quad transformations.

### 4. **Analysis and Visualization**
- Open the notebooks in `analysis/notebooks/` to explore evaluations and generate insights.
- Use visualization tools in `analysis/visualization/` to view argumentation graphs.

### 5. **Results and Evaluation**
Evaluate results stored in `code/results/` and `analysis/results/` using both qualitative and quantitative approaches.

---

## Research Focus

This research investigates:
1. The scoring of peer reviews based on structured argumentation frameworks.
2. Comparisons of annotations from human reviewers and LLMs (GPT, Gemini, Mistral, and Llama).
3. Quantitative metrics (e.g., Cohen's Kappa, Fleiss' Kappa) to evaluate inter-annotator agreement.
4. Visualization and interpretation of argumentation frameworks.

---

## Contributing

Contributions to improve datasets, models, or analyses are welcome. Please submit a pull request with your updates.

---

## License

This repository is licensed under the MIT License. See `LICENSE` for details.
