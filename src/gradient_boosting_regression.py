
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


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

    print("=" * 65)
    print("VIDEO GAME SALES - GRADIENT BOOSTING REGRESSION")
    print("=" * 65)

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    print("\nDataset loaded successfully.")
    print("Dataset shape:", df.shape)

    target = "Global_Sales"

    features = [
        "Platform",
        "Genre",
        "Publisher",
        "Year"
    ]

    required_columns = features + [target]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df = df[required_columns].copy()

    df[target] = pd.to_numeric(
        df[target], errors="coerce"
    )

    df["Year"] = pd.to_numeric(
        df["Year"], errors="coerce"
    )

    df = df.dropna(subset=[target])
    df = df[df[target] >= 0]

    for col in ["Platform", "Genre", "Publisher"]:
        df[col] = df[col].fillna("Unknown")

    print("Usable records:", len(df))
    print("Features:", features)
    print("Target:", target)

    if len(df) < 10:
        raise ValueError(
            "Not enough usable records for model training."
        )


    # --------------------------------------------------
    # 3. SPLIT DATA
    # --------------------------------------------------

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    print("\nTraining records:", len(X_train))
    print("Testing records:", len(X_test))


    # --------------------------------------------------
    # 4. PREPROCESS FEATURES
    # --------------------------------------------------

    categorical_features = [
        "Platform",
        "Genre",
        "Publisher"
    ]

    numerical_features = ["Year"]

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent")
            ),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore")
            )
        ]
    )

    numerical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median")
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                categorical_pipeline,
                categorical_features
            ),
            (
                "numerical",
                numerical_pipeline,
                numerical_features
            )
        ]
    )


    # --------------------------------------------------
    # 5. TRAIN GRADIENT BOOSTING MODEL
    # --------------------------------------------------

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                GradientBoostingRegressor(
                    n_estimators=200,
                    learning_rate=0.05,
                    max_depth=3,
                    min_samples_leaf=5,
                    loss="squared_error",
                    random_state=42
                )
            )
        ]
    )

    print("\nTraining Gradient Boosting model...")

    model.fit(X_train, y_train)

    print("Model training completed.")


    # --------------------------------------------------
    # 6. EVALUATE MODEL
    # --------------------------------------------------

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test, predictions
    )

    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    r2 = r2_score(
        y_test, predictions
    )

    metrics = pd.DataFrame({
        "Metric": [
            "Mean Absolute Error (MAE)",
            "Root Mean Squared Error (RMSE)",
            "R2 Score"
        ],
        "Value": [
            mae,
            rmse,
            r2
        ]
    })

    metrics.to_csv(
        RESULTS_DIR / "gradient_boosting_metrics.csv",
        index=False
    )

    print("\nMODEL EVALUATION")
    print("-" * 45)
    print(f"MAE  : {mae:.4f} million units")
    print(f"RMSE : {rmse:.4f} million units")
    print(f"R2   : {r2:.4f}")


    # --------------------------------------------------
    # 7. SAVE PREDICTIONS
    # --------------------------------------------------

    prediction_df = pd.DataFrame({
        "Actual_Global_Sales": y_test.to_numpy(),
        "Predicted_Global_Sales": predictions
    })

    prediction_df["Absolute_Error"] = (
        prediction_df["Actual_Global_Sales"]
        - prediction_df["Predicted_Global_Sales"]
    ).abs()

    prediction_df.to_csv(
        RESULTS_DIR / "gradient_boosting_predictions.csv",
        index=False
    )


    # --------------------------------------------------
    # 8. FEATURE IMPORTANCE
    # --------------------------------------------------

    fitted_preprocessor = model.named_steps[
        "preprocessor"
    ]

    fitted_model = model.named_steps["regressor"]

    feature_names = (
        fitted_preprocessor.get_feature_names_out()
    )

    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": fitted_model.feature_importances_
    }).sort_values(
        "Importance",
        ascending=False
    )

    importance_df.to_csv(
        RESULTS_DIR / "gradient_boosting_feature_importance.csv",
        index=False
    )

    group_rows = []

    for original_feature in features:

        if original_feature == "Year":
            mask = importance_df["Feature"].eq(
                "numerical__Year"
            )
        else:
            prefix = f"categorical__{original_feature}_"

            mask = importance_df["Feature"].str.startswith(
                prefix
            )

        group_rows.append({
            "Feature": original_feature,
            "Importance": importance_df.loc[
                mask, "Importance"
            ].sum()
        })

    grouped_importance = pd.DataFrame(
        group_rows
    ).sort_values(
        "Importance",
        ascending=False
    )

    grouped_importance.to_csv(
        RESULTS_DIR / "gradient_boosting_grouped_importance.csv",
        index=False
    )

    print("\nFEATURE IMPORTANCE")
    print(grouped_importance.to_string(index=False))


    # --------------------------------------------------
    # 9. PLOT FEATURE IMPORTANCE
    # --------------------------------------------------

    plot_df = grouped_importance.sort_values(
        "Importance",
        ascending=True
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(
        plot_df["Feature"],
        plot_df["Importance"]
    )

    ax.set_title(
        "Gradient Boosting - Feature Importance"
    )
    ax.set_xlabel("Total Feature Importance")
    ax.set_ylabel("Input Feature")
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        VISUALIZATIONS_DIR
        / "gradient_boosting_feature_importance.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)


    # --------------------------------------------------
    # 10. ACTUAL VS PREDICTED SALES
    # --------------------------------------------------

    fig, ax = plt.subplots(figsize=(8, 7))

    ax.scatter(
        y_test,
        predictions,
        alpha=0.55,
        s=18
    )

    maximum_value = max(
        float(y_test.max()),
        float(np.max(predictions))
    )

    ax.plot(
        [0, maximum_value],
        [0, maximum_value],
        linestyle="--"
    )

    ax.set_title(
        "Gradient Boosting: Actual vs Predicted Sales"
    )
    ax.set_xlabel("Actual Global Sales (Millions)")
    ax.set_ylabel("Predicted Global Sales (Millions)")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        VISUALIZATIONS_DIR
        / "gradient_boosting_actual_vs_predicted.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)


    # --------------------------------------------------
    # 11. FINISH
    # --------------------------------------------------

    print("\nGenerated files:")
    print("- results/gradient_boosting_metrics.csv")
    print("- results/gradient_boosting_predictions.csv")
    print("- results/gradient_boosting_feature_importance.csv")
    print("- results/gradient_boosting_grouped_importance.csv")
    print("- visualizations/gradient_boosting_feature_importance.png")
    print("- visualizations/gradient_boosting_actual_vs_predicted.png")

    print("\nGradient Boosting Regression completed successfully.")


if __name__ == "__main__":
    main()
