#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd

# Load the dataset
df = pd.read_csv("user_traits_with_clusters.csv")

# Define traits and their prefixes
traits = {
    'EXT': [f'EXT{i}' for i in range(1, 11)],
    'EST': [f'EST{i}' for i in range(1, 11)],
    'AGR': [f'AGR{i}' for i in range(1, 11)],
    'CSN': [f'CSN{i}' for i in range(1, 11)],
    'OPN': [f'OPN{i}' for i in range(1, 11)],
}

# --- METHOD 1: Based on Variance (Standard Deviation)
top_questions_variance = {}

for trait, columns in traits.items():
    stds = df[columns].std().sort_values(ascending=False)
    top_questions_variance[trait] = list(stds.head(2).index)

# --- METHOD 2: Based on Correlation with Cluster
top_questions_correlation = {}

for trait, columns in traits.items():
    corrs = df[columns].corrwith(df['Clusters']).abs().sort_values(ascending=False)
    top_questions_correlation[trait] = list(corrs.head(2).index)

# Print the selected questions
print("🔹 Top 2 Questions per Trait (Based on Variance):")
for trait, questions in top_questions_variance.items():
    print(f"{trait}: {questions}")

print("\n🔹 Top 2 Questions per Trait (Based on Correlation with Cluster):")
for trait, questions in top_questions_correlation.items():
    print(f"{trait}: {questions}")


# In[10]:


# # Combine 1 from variance and 1 from correlation for each trait
# final_selected_questions = {}

# for trait in traits:
#     var_qs = top_questions_variance[trait]
#     corr_qs = top_questions_correlation[trait]

#     # Ensure unique selection
#     combined = []
#     combined.append(var_qs[0])
    
#     # Add a different question from correlation-based if possible
#     if corr_qs[0] != var_qs[0]:
#         combined.append(corr_qs[0])
#     else:
#         combined.append(corr_qs[1])  # Fallback to second if same

#     final_selected_questions[trait] = combined

# # Print the final hybrid selection
# print("🔹 Final Questionnaire (1 from variance, 1 from correlation):")
# for trait, questions in final_selected_questions.items():
#     print(f"{trait}: {questions}")

