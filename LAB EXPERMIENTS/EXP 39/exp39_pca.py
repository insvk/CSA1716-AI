from sklearn.datasets import load_breast_cancer
from sklearn.decomposition import PCA

# Load high-dimensional data (30 features)
data = load_breast_cancer()
X = data.data
y = data.target

# Perform PCA to reduce to 2 dimensions
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

print(f"Original shape: {X.shape}")
print(f"Reduced shape: {X_pca.shape}")
print(f"Explained Variance Ratio: {pca.explained_variance_ratio_}")