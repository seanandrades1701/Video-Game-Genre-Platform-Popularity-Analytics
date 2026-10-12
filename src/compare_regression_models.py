
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]

RESULTS_DIR = PROJECT_DIR / "results"
VISUALIZATIONS_DIR = PROJECT_DIR / "visualizations"

RF_PATH = RESULTS_DIR / "random_forest_metrics.csv"
GB_PATH = RESULTS_DIR / "gradient_boosting_metrics.csv"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOAD MODEL METRICS
# --------------------------------------------------

def main():

    print("=" * 60)
    print("REGRESSION MODEL COMPARISON")
    print("=" * 60)

    for path in [RF_PATH, GB_PATH]:
        if not path.exists():
            raise FileNotFoundError(
                f"Metrics file not found: {path}"
            )

    rf = pd.read_csv(RF_PATH)
    gb = pd.read_csv(GB_PATH)

    rf_metrics = dict(zip(rf["Metric"], rf["Value"]))
    gb_metrics = dict(zip(gb["Metric"], gb["Value"]))

    comparison = pd.DataFrame({
        "Metric": [
            "MAE",
            "RMSE",
            "R2"
        ],
        "Random_Forest": [
            rf_metrics["Mean Absolute Error (MAE)"],
            rf_metrics["Root Mean Squared Error (RMSE)"],
            rf_metrics["R2 Score"]
        ],
        "Gradient_Boosting": [
            gb_metrics["Mean Absolute Error (MAE)"],
            gb_metrics["Root Mean Squared Error (RMSE)"],
            gb_metrics["R2 Score"]
        ]
    })

    comparison.to_csv(
        RESULTS_DIR / "regression_model_comparison.csv",
        index=False
    )

    print("\nMODEL COMPARISON")
    print(comparison.to_string(index=False))


    # --------------------------------------------------
    # 3. PLOT MAE AND RMSE
    # --------------------------------------------------

    error_comparison = comparison[
        comparison["Metric"].isin(["MAE", "RMSE"])
    ]

    ax = error_comparison.set_index("Metric")[
        ["Random_Forest", "Gradient_Boosting"]
    ].plot(
        kind="bar",
        figsize=(9, 5)
    )

    ax.set_title("Regression Models: Error Comparison")
    ax.set_xlabel("Evaluation Metric")
    ax.set_ylabel("Error (Millions of Units)")
    ax.tick_params(axis="x", rotation=0)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(["Random Forest", "Gradient Boosting"])

    plt.tight_layout()

    plt.savefig(
        VISUALIZATIONS_DIR
        / "regression_error_comparison.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    # --------------------------------------------------
    # 4. PLOT R2 SCORE
    # --------------------------------------------------

    r2_values = comparison[
        comparison["Metric"] == "R2"
    ]

    ax = r2_values.set_index("Metric")[
        ["Random_Forest", "Gradient_Boosting"]
    ].plot(
        kind="bar",
        figsize=(7, 5)
    )

    ax.set_title("Regression Models: R2 Comparison")
    ax.set_xlabel("")
    ax.set_ylabel("R2 Score")
    ax.tick_params(axis="x", rotation=0)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(["Random Forest", "Gradient Boosting"])

    plt.tight_layout()

    plt.savefig(
        VISUALIZATIONS_DIR
        / "regression_r2_comparison.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("\nGenerated files:")
    print("- results/regression_model_comparison.csv")
    print("- visualizations/regression_error_comparison.png")
    print("- visualizations/regression_r2_comparison.png")

    print("\nModel comparison completed successfully.")


if __name__ == "__main__":
    main()
