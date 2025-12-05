#!/usr/bin/env python
# coding: utf-8

# In[3]:


get_ipython().system('pip install kmodes')


# In[17]:


import pandas as pd
from kmodes.kprototypes import KPrototypes
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np


# In[19]:


df = pd.read_csv("data-final.csv", sep="\t", encoding="utf-8")


# In[20]:


df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace("\ufeff", "")  


# In[21]:


df = df.iloc[:60000]


# In[22]:


trait_prefixes = ["EXT", "EST", "AGR", "CSN", "OPN"]
for prefix in trait_prefixes:
    for i in range(1, 11):
        col = f"{prefix}{i}"
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")


# In[23]:


df["extraversion"] = df[[f"EXT{i}" for i in range(1, 11)]].mean(axis=1)
df["neuroticism"] = df[[f"EST{i}" for i in range(1, 11)]].mean(axis=1)
df["agreeableness"] = df[[f"AGR{i}" for i in range(1, 11)]].mean(axis=1)
df["conscientiousness"] = df[[f"CSN{i}" for i in range(1, 11)]].mean(axis=1)
df["openness"] = df[[f"OPN{i}" for i in range(1, 11)]].mean(axis=1)


# In[24]:


df.dropna(subset=["extraversion", "neuroticism", "agreeableness", "conscientiousness", "openness", "country"], inplace=True)


# In[28]:


scaler = StandardScaler()
numeric_scaled = scaler.fit_transform(df[["extraversion", "neuroticism", "agreeableness", "conscientiousness", "openness"]])


# In[26]:


df["country"] = df["country"].astype("category")
encoded_country = df["country"].cat.codes


# In[13]:


# # Step 9: Combine numeric and categorical features
# X = pd.DataFrame(numeric_data, columns=["extraversion", "neuroticism", "agreeableness", "conscientiousness", "openness"])
# X["country"] = encoded_country.values
# X_matrix = X.values


# In[30]:


import numpy as np
X_matrix = np.hstack([numeric_scaled, encoded_country.values.reshape(-1, 1)])
print(" Feature engineering complete. Shape of X_matrix:", X_matrix.shape)


# In[31]:


kproto = KPrototypes(n_clusters=5, init="Cao", n_init=5, verbose=2, random_state=42)
clusters = kproto.fit_predict(X_matrix, categorical=[5])
df["cluster"] = clusters


# In[34]:


print("🔢 Cluster Distribution:")
print(df["cluster"].value_counts().sort_index())


# In[35]:


# cluster_summary = df.groupby("cluster")[["extraversion", "neuroticism", "agreeableness", "conscientiousness", "openness"]].mean()
# print(cluster_summary)


# In[38]:


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


# In[37]:


from sklearn.metrics import silhouette_score, davies_bouldin_score

sil = silhouette_score(X_numeric, clusters)
db = davies_bouldin_score(X_numeric, clusters)

print(f"\n📐 Silhouette Score (numeric traits only): {sil:.4f}")
print(f"📉 Davies-Bouldin Index: {db:.4f}")


# In[53]:


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
df_full.to_csv("C:/Users/Sannidhi Hegde/Desktop/VS Code/mental_health_tracker/data/user_traits_with_clusters.csv", index=False)

print("✅ Final dataset with Big Five questions, country, and Clusters saved as: 'user_traits_with_clusters.csv'")


# In[54]:


import pandas as pd

df_clustered = pd.read_csv("data/user_traits_with_clusters.csv")
df_clustered.head(10)  # Shows first 5 rows


# In[ ]:


# Optional: Map clusters to personality names (can customize)
personality_labels = {
    0: "The Communicator",
    1: "The Analyzer",
    2: "The Explorer",
    3: "The Helper",
    4: "The Organizer"
}
df["personality_type"] = df["cluster"].map(personality_labels)


# In[ ]:


df.to_csv("data/clustered_bigfive_personality.csv", index=False)
print("\n✅ Model training complete. Labeled dataset and model artifacts saved.")


# In[ ]:




