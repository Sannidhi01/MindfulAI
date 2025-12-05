get_ipython().system('pip install kmodes')

import pandas as pd
from kmodes.kprototypes import KPrototypes
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np

df = pd.read_csv("data-final.csv", sep="\t", encoding="utf-8")

df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace("\ufeff", "")  

df = df.iloc[:60000]

trait_prefixes = ["EXT", "EST", "AGR", "CSN", "OPN"]
for prefix in trait_prefixes:
    for i in range(1, 11):
        col = f"{prefix}{i}"
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

df["extraversion"] = df[[f"EXT{i}" for i in range(1, 11)]].mean(axis=1)
df["neuroticism"] = df[[f"EST{i}" for i in range(1, 11)]].mean(axis=1)
df["agreeableness"] = df[[f"AGR{i}" for i in range(1, 11)]].mean(axis=1)
df["conscientiousness"] = df[[f"CSN{i}" for i in range(1, 11)]].mean(axis=1)
df["openness"] = df[[f"OPN{i}" for i in range(1, 11)]].mean(axis=1)

df.dropna(subset=["extraversion", "neuroticism", "agreeableness", "conscientiousness", "openness", "country"], inplace=True)


scaler = StandardScaler()
numeric_scaled = scaler.fit_transform(df[["extraversion", "neuroticism", "agreeableness", "conscientiousness", "openness"]])


df["country"] = df["country"].astype("category")
encoded_country = df["country"].cat.codes


X_matrix = np.hstack([numeric_scaled, encoded_country.values.reshape(-1, 1)])
print(" Feature engineering complete. Shape of X_matrix:", X_matrix.shape)

kproto = KPrototypes(n_clusters=5, init="Cao", n_init=5, verbose=2, random_state=42)
clusters = kproto.fit_predict(X_matrix, categorical=[5])
df["cluster"] = clusters



print(" Cluster Distribution:")
print(df["cluster"].value_counts().sort_index())


from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

pca = PCA(n_components=2)
X_numeric = X_matrix[:, :5].astype(float)  # only numeric part
X_pca = pca.fit_transform(X_numeric)

plt.figure(figsize=(6, 4))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='tab10', alpha=0.6)
plt.title("PCA of Personality Traits Colored by Cluster")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.colorbar(label="Cluster")
plt.grid(True)
plt.show()


from sklearn.metrics import davies_bouldin_score

db = davies_bouldin_score(X_numeric, clusters)

print(f"\n Silhouette Score (numeric traits only): {sil:.4f}")
print(f" Davies-Bouldin Index: {db:.4f}")

# List the exact expected Big Five questionnaire columns
trait_columns = [f"{prefix}{i}" for prefix in ["EXT", "EST", "AGR", "CSN", "OPN"] for i in range(1, 11)]

# Ensure column names are clean
df.columns = df.columns.str.strip().str.replace("\ufeff", "")

# Keep only the trait columns that actually exist in the DataFrame
existing_traits = [col for col in trait_columns if col in df.columns]

# Add Clusters column (if not already)
df["Clusters"] = df["cluster"]

# Add country
final_columns = existing_traits + ["country", "Clusters"]

# Create the final dataset
df_full = df[final_columns].copy()

# Save to CSV
df_full.to_csv("path/data/user_traits_with_clusters.csv", index=False)
print(" Final dataset with Big Five questions, country, and Clusters saved as: 'user_traits_with_clusters.csv'")

df_clustered = pd.read_csv("data/user_traits_with_clusters.csv")
df_clustered.head(10) 

personality_labels = {
    0: "The Communicator",
    1: "The Analyzer",
    2: "The Explorer",
    3: "The Helper",
    4: "The Organizer"
}
df["personality_type"] = df["cluster"].map(personality_labels)


df.to_csv("data/clustered_bigfive_personality.csv", index=False)
print("\n Model training complete. Labeled dataset and model artifacts saved.")
