
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    ConfusionMatrixDisplay
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
    print("VIDEO GAME SALES - RANDOM FOREST CLASSIFICATION")
    print("=" * 65)

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}\n"
            "Run data_transformation.py first."
        )

    df = pd.read_csv(DATASET_PATH)

    print("\nDataset loaded successfully.")
    print("Dataset shape:", df.shape)

    target = "Sales_Category"

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

    # Clean the target labels.
    df[target] = df[target].astype("string").str.strip()

    df = df.dropna(subset=[target])
    df = df[df[target] != ""]

    # Convert year to numeric.
    df["Year"] = pd.to_numeric(
        df["Year"], errors="coerce"
    )

    # Fill missing categorical values.
    for col in ["Platform", "Genre", "Publisher"]:
        df[col] = (
            df[col]
            .astype("string")
            .fillna("Unknown")
            .replace("", "Unknown")
        )

    print("Usable records:", len(df))
    print("\nSales category distribution:")
    print(df[target].value_counts())

    print("\nInput features:", features)
    print("Target:", target)

    if df[target].nunique() < 2:
        raise ValueError(
            "Classification requires at least two target classes."
        )

    # Each class needs enough records for a stratified split.
    class_counts = df[target].value_counts()

    if class_counts.min() < 2:
        raise ValueError(
            "At least one sales category has fewer than two "
            "records. Check the category labels before splitting."
        )


    # --------------------------------------------------
    # 3. DEFINE FEATURES AND TARGET
    # --------------------------------------------------

    X = df[features]
    y = df[target]

    # Keep a consistent, meaningful class order for reports.
    preferred_order = [
        "Low",
        "Medium",
        "High",
        "Very High"
    ]

    class_labels = [
        label for label in preferred_order
        if label in y.unique()
    ]

    # Include any unexpected labels rather than silently
    # excluding records.
    class_labels += sorted(
        label for label in y.unique()
        if label not in class_labels
    )


    # --------------------------------------------------
    # 4. SPLIT DATA
    # --------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\nTraining records:", len(X_train))
    print("Testing records:", len(X_test))


    # --------------------------------------------------
    # 5. PREPROCESS FEATURES
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
    # 6. TRAIN RANDOM FOREST CLASSIFIER
    # --------------------------------------------------

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    random_state=42,
                    n_jobs=-1,
                    min_samples_leaf=2,
                    class_weight="balanced_subsample"
                )
            )
        ]
    )

    print("\nTraining Random Forest Classifier...")

    model.fit(X_train, y_train)

    print("Model training completed.")


    # --------------------------------------------------
    # 7. MAKE PREDICTIONS
    # --------------------------------------------------

    predictions = model.predict(X_test)


    # --------------------------------------------------
    # 8. EVALUATE MODEL
    # --------------------------------------------------

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    macro_f1 = f1_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    weighted_f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    metrics_df = pd.DataFrame({
        "Metric": [
            "Accuracy",
            "Macro_Precision",
            "Macro_Recall",
            "Macro_F1",
            "Weighted_F1"
        ],
        "Value": [
            accuracy,
            precision,
            recall,
            macro_f1,
            weighted_f1
        ]
    })

    metrics_df.to_csv(
        RESULTS_DIR / "random_forest_classification_metrics.csv",
        index=False
    )

    print("\nMODEL EVALUATION")
    print("-" * 50)
    print(f"Accuracy        : {accuracy:.4f}")
    print(f"Macro Precision : {precision:.4f}")
    print(f"Macro Recall    : {recall:.4f}")
    print(f"Macro F1        : {macro_f1:.4f}")
    print(f"Weighted F1     : {weighted_f1:.4f}")

    report = classification_report(
        y_test,
        predictions,
        labels=class_labels,
        output_dict=True,
        zero_division=0
    )

    report_df = pd.DataFrame(report).transpose()

    report_df.to_csv(
        RESULTS_DIR / "random_forest_classification_report.csv"
    )

    print("\nCLASSIFICATION REPORT")
    print(
        classification_report(
            y_test,
            predictions,
            labels=class_labels,
            zero_division=0
        )
    )


    # --------------------------------------------------
    # 9. SAVE ACTUAL AND PREDICTED CATEGORIES
    # --------------------------------------------------

    prediction_df = pd.DataFrame({
        "Actual_Category": y_test.to_numpy(),
        "Predicted_Category": predictions
    })

    prediction_df["Correct"] = (
        prediction_df["Actual_Category"]
        == prediction_df["Predicted_Category"]
    )

    prediction_df.to_csv(
        RESULTS_DIR / "random_forest_classification_predictions.csv",
        index=False
    )


    # --------------------------------------------------
    # 10. CONFUSION MATRIX
    # --------------------------------------------------

    fig, ax = plt.subplots(figsize=(9, 7))

    ConfusionMatrixDisplay.from_predictions(
        y_test,
        predictions,
        labels=class_labels,
        display_labels=class_labels,
        cmap="Blues",
        values_format="d",
        xticks_rotation=30,
        ax=ax
    )

    ax.set_title(
        "Random Forest Classification - Confusion Matrix"
    )
    ax.set_xlabel("Predicted Category")
    ax.set_ylabel("Actual Category")

    plt.tight_layout()

    plt.savefig(
        VISUALIZATIONS_DIR
        / "random_forest_confusion_matrix.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)


    # --------------------------------------------------
    # 11. FEATURE IMPORTANCE
    # --------------------------------------------------

    fitted_preprocessor = model.named_steps["preprocessor"]
    fitted_classifier = model.named_steps["classifier"]

    feature_names = (
        fitted_preprocessor.get_feature_names_out()
    )

    importance_df = pd.DataFrame({
        "Encoded_Feature": feature_names,
        "Importance": fitted_classifier.feature_importances_
    })

    # Combine encoded categories into their original feature.
    def get_feature_group(encoded_name):

        if encoded_name.startswith("categorical__"):
            name = encoded_name.replace(
                "categorical__", "", 1
            )

            for feature in categorical_features:
                if name.startswith(feature + "_"):
                    return feature

        if encoded_name == "numerical__Year":
            return "Year"

        return encoded_name

    importance_df["Feature"] = (
        importance_df["Encoded_Feature"]
        .apply(get_feature_group)
    )

    grouped_importance = (
        importance_df.groupby("Feature", as_index=False)
        ["Importance"].sum()
        .sort_values("Importance", ascending=False)
    )

    grouped_importance.to_csv(
        RESULTS_DIR
        / "random_forest_classification_feature_importance.csv",
        index=False
    )

    print("\nFEATURE IMPORTANCE")
    print(grouped_importance.to_string(index=False))


    # --------------------------------------------------
    # 12. PLOT FEATURE IMPORTANCE
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
        "Random Forest Classifier - Feature Importance"
    )
    ax.set_xlabel("Total Feature Importance")
    ax.set_ylabel("Input Feature")
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        VISUALIZATIONS_DIR
        / "random_forest_classification_feature_importance.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)


    # --------------------------------------------------
    # 13. FINISH
    # --------------------------------------------------

    print("\nGenerated files:")
    print("- results/random_forest_classification_metrics.csv")
    print("- results/random_forest_classification_report.csv")
    print("- results/random_forest_classification_predictions.csv")
    print("- results/random_forest_classification_feature_importance.csv")
    print("- visualizations/random_forest_confusion_matrix.png")
    print(
        "- visualizations/"
        "random_forest_classification_feature_importance.png"
    )

    print("\nRandom Forest Classification completed successfully.")


if __name__ == "__main__":
    main()
