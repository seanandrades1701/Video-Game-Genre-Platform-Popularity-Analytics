
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_DIR / "dataset" / "vgsales_transformed.csv"
)

RESULTS_DIR = PROJECT_DIR / "results"
VISUALIZATIONS_DIR = PROJECT_DIR / "visualizations"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOAD DATASET
# --------------------------------------------------

def main():

    print("=" * 60)
    print("VIDEO GAME SALES - K-MEANS CLUSTERING")
    print("=" * 60)

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}\n"
            "Run data_transformation.py first."
        )

    df = pd.read_csv(DATASET_PATH)

    print("\nDataset loaded successfully.")
    print("Dataset shape:", df.shape)

    # Regional sales are used as clustering features.
    features = [
        "NA_Sales",
        "EU_Sales",
        "JP_Sales",
        "Other_Sales"
    ]

    missing_columns = [
        col for col in features if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Preserve the original row index and metadata.
    original_df = df.copy()

    # Convert regional sales columns to numeric values.
    X = df[features].apply(
        pd.to_numeric, errors="coerce"
    )

    # Replace invalid or missing values with column medians.
    X = X.replace([np.inf, -np.inf], np.nan)

    if X.isna().all().any():
        raise ValueError(
            "At least one regional sales column contains "
            "no usable numeric values."
        )

    X = X.fillna(X.median())

    # Sales cannot be negative for this analysis.
    if (X < 0).any().any():
        raise ValueError(
            "Negative regional sales values were found. "
            "Investigate the data before clustering."
        )

    print("\nFeatures used:", features)


    # --------------------------------------------------
    # 3. TRANSFORM AND STANDARDIZE FEATURES
    # --------------------------------------------------

    # Reduce the influence of highly skewed sales values.
    X_log = np.log1p(X)

    # Give the four features comparable scale.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_log)

    print("Feature transformation completed.")


    # --------------------------------------------------
    # 4. TEST DIFFERENT NUMBERS OF CLUSTERS
    # --------------------------------------------------

    evaluation_rows = []

    k_values = range(2, 7)

    # Use a reproducible sample to estimate silhouette score.
    sample_size = min(3000, len(X_scaled))

    if sample_size < 3:
        raise ValueError(
            "Not enough records for clustering evaluation."
        )

    for k in k_values:

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(X_scaled)

        score = silhouette_score(
            X_scaled,
            labels,
            sample_size=sample_size,
            random_state=42
        )

        evaluation_rows.append({
            "K": k,
            "Inertia": model.inertia_,
            "Silhouette_Score": score
        })

        print(
            f"K={k} | "
            f"Inertia={model.inertia_:.2f} | "
            f"Silhouette={score:.4f}"
        )

    evaluation_df = pd.DataFrame(evaluation_rows)

    evaluation_df.to_csv(
        RESULTS_DIR / "clustering_evaluation.csv",
        index=False
    )

    # Choose the candidate with the highest sampled
    # silhouette score among K=2,...,6.
    best_k = int(
        evaluation_df.loc[
            evaluation_df["Silhouette_Score"].idxmax(),
            "K"
        ]
    )

    print("\nSelected K:", best_k)


    # --------------------------------------------------
    # 5. TRAIN FINAL K-MEANS MODEL
    # --------------------------------------------------

    final_model = KMeans(
        n_clusters=best_k,
        random_state=42,
        n_init=10
    )

    cluster_labels = final_model.fit_predict(X_scaled)

    original_df["Cluster"] = cluster_labels

    original_df.to_csv(
        RESULTS_DIR / "clustering_results.csv",
        index=False
    )

    print("\nCluster assignments saved.")


    # --------------------------------------------------
    # 6. CREATE CLUSTER PROFILES
    # --------------------------------------------------

    profile_df = original_df.copy()

    # Use numeric columns for averages.
    numeric_columns = [
        "NA_Sales",
        "EU_Sales",
        "JP_Sales",
        "Other_Sales",
        "Global_Sales"
    ]

    available_numeric = [
        col for col in numeric_columns
        if col in profile_df.columns
    ]

    profile_df[available_numeric] = (
        profile_df[available_numeric]
        .apply(pd.to_numeric, errors="coerce")
    )

    profiles = profile_df.groupby("Cluster").agg(
        Game_Count=("Cluster", "size"),
        **{
            f"Average_{col}": (col, "mean")
            for col in available_numeric
        }
    ).reset_index()

    # Add the most frequent genre and platform if available.
    for col in ["Genre", "Platform"]:
        if col in profile_df.columns:
            top_values = (
                profile_df.groupby("Cluster")[col]
                .agg(
                    lambda values:
                    values.mode().iloc[0]
                    if not values.mode().empty
                    else "Unknown"
                )
            )

            profiles[f"Most_Common_{col}"] = (
                profiles["Cluster"].map(top_values)
            )

    profiles.to_csv(
        RESULTS_DIR / "cluster_profiles.csv",
        index=False
    )

    print("\nCluster profiles:")
    print(profiles.to_string(index=False))


    # --------------------------------------------------
    # 7. PLOT INERTIA AND SILHOUETTE SCORES
    # --------------------------------------------------

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    axes[0].plot(
        evaluation_df["K"],
        evaluation_df["Inertia"],
        marker="o"
    )
    axes[0].set_title("K-Means Elbow Curve")
    axes[0].set_xlabel("Number of Clusters (K)")
    axes[0].set_ylabel("Inertia")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(
        evaluation_df["K"],
        evaluation_df["Silhouette_Score"],
        marker="o"
    )
    axes[1].set_title("Silhouette Score Comparison")
    axes[1].set_xlabel("Number of Clusters (K)")
    axes[1].set_ylabel("Silhouette Score")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        VISUALIZATIONS_DIR / "kmeans_evaluation.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)


    # --------------------------------------------------
    # 8. PCA VISUALIZATION
    # --------------------------------------------------

    pca = PCA(n_components=2)

    X_pca = pca.fit_transform(X_scaled)

    # Sample points for a clearer, faster visualization.
    rng = np.random.default_rng(42)

    plot_size = min(5000, len(X_pca))

    plot_indices = rng.choice(
        len(X_pca),
        size=plot_size,
        replace=False
    )

    fig, ax = plt.subplots(figsize=(10, 7))

    scatter = ax.scatter(
        X_pca[plot_indices, 0],
        X_pca[plot_indices, 1],
        c=cluster_labels[plot_indices],
        cmap="viridis",
        s=12,
        alpha=0.65
    )

    ax.set_title("K-Means Game Clusters Using PCA")
    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")

    ax.legend(
        *scatter.legend_elements(),
        title="Cluster"
    )

    plt.tight_layout()

    plt.savefig(
        VISUALIZATIONS_DIR / "cluster_visualization.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    explained_variance = pca.explained_variance_ratio_.sum()

    print(
        "\nPCA variance explained by two components:",
        f"{explained_variance:.2%}"
    )

    print("\nGenerated files:")
    print("- results/clustering_evaluation.csv")
    print("- results/clustering_results.csv")
    print("- results/cluster_profiles.csv")
    print("- visualizations/kmeans_evaluation.png")
    print("- visualizations/cluster_visualization.png")

    print("\nK-Means clustering completed successfully.")


if __name__ == "__main__":
    main()
