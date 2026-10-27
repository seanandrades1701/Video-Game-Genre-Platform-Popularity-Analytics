
from pathlib import Path

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "dataset" / "vgsales_transformed.csv"
RESULTS_DIR = PROJECT_DIR / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# APRIORI ASSOCIATION RULE MINING
# --------------------------------------------------

def main():
    print("=" * 70)
    print("VIDEO GAME MARKET: HIDDEN PATTERN ANALYSIS")
    print("=" * 70)

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Run data_cleaning.py and data_transformation.py first."
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = [
        "Name",
        "Platform",
        "Genre",
        "Publisher",
        "Decade",
        "Sales_Category",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Each game is treated as one transaction.
    # Attributes become items that can appear together.
    transactions = pd.DataFrame({
        "Genre": "Genre=" + df["Genre"].astype(str),
        "Platform": "Platform=" + df["Platform"].astype(str),
        "Publisher": "Publisher=" + df["Publisher"].astype(str),
        "Decade": "Decade=" + df["Decade"].astype(str),
        "Sales_Category": "Sales=" + df["Sales_Category"].astype(str),
    })

    # Convert each transaction into a one-hot encoded basket.
    encoded = pd.get_dummies(transactions.stack()).groupby(level=0).max()
    encoded = encoded.astype(bool)

    print(f"\nGames analysed: {len(df):,}")
    print(f"Unique attribute items: {encoded.shape[1]:,}")

    # Find frequently occurring combinations.
    print("\nFinding frequent itemsets...")

    frequent_itemsets = apriori(
        encoded,
        min_support=0.02,
        use_colnames=True,
        max_len=3,
        low_memory=True,
    )

    if frequent_itemsets.empty:
        print("No frequent itemsets found. Try lowering min_support.")
        return

    frequent_itemsets["itemsets"] = frequent_itemsets["itemsets"].apply(
        lambda items: " + ".join(sorted(items))
    )

    frequent_itemsets = frequent_itemsets.sort_values(
        "support", ascending=False
    )

    itemsets_path = RESULTS_DIR / "apriori_frequent_itemsets.csv"
    frequent_itemsets.to_csv(itemsets_path, index=False)

    # Recalculate itemsets in their original frozenset format for rule creation.
    original_itemsets = apriori(
        encoded,
        min_support=0.02,
        use_colnames=True,
        max_len=3,
        low_memory=True,
    )

    rules = association_rules(
        original_itemsets,
        metric="confidence",
        min_threshold=0.20,
    )

    if rules.empty:
        print("No association rules found with the current thresholds.")
        print(f"Frequent itemsets saved to: {itemsets_path}")
        return

    # Keep rules that reveal relationships between different attributes.
    attribute_prefixes = [
        "Genre=",
        "Platform=",
        "Publisher=",
        "Decade=",
        "Sales=",
    ]

    def get_attributes(itemset):
        return {
            prefix
            for item in itemset
            for prefix in attribute_prefixes
            if item.startswith(prefix)
        }

    # Rules should connect at least two different attribute types.
    rules = rules[
        rules.apply(
            lambda row: len(
                get_attributes(row["antecedents"])
                | get_attributes(row["consequents"])
            ) >= 2,
            axis=1,
        )
    ].copy()

    if rules.empty:
        print("No cross-attribute rules found.")
        return

    # Human-readable rule columns.
    rules["Antecedent"] = rules["antecedents"].apply(
        lambda items: " + ".join(sorted(items))
    )
    rules["Consequent"] = rules["consequents"].apply(
        lambda items: " + ".join(sorted(items))
    )

    # Lift > 1 indicates a positive association compared with independence.
    rules["Insight"] = rules["lift"].apply(
        lambda lift: (
            "Positive association" if lift > 1
            else "Negative association" if lift < 1
            else "No association"
        )
    )

    output_columns = [
        "Antecedent",
        "Consequent",
        "support",
        "confidence",
        "lift",
        "leverage",
        "conviction",
        "Insight",
    ]

    rules = rules[output_columns].sort_values(
        ["lift", "confidence", "support"],
        ascending=[False, False, False],
    )

    rules_path = RESULTS_DIR / "apriori_association_rules.csv"
    rules.to_csv(rules_path, index=False)

    print("\nTOP 15 ASSOCIATION RULES")
    print("-" * 70)

    display_rules = rules.head(15).copy()
    for col in ["support", "confidence", "lift"]:
        display_rules[col] = display_rules[col].round(3)

    print(display_rules.to_string(index=False))

    print("\nINTERPRETATION")
    print("-" * 70)
    print("Support: fraction of games containing the full combination.")
    print("Confidence: fraction of games with the antecedent that also")
    print("            contain the consequent.")
    print("Lift > 1: the consequent occurs more often with the antecedent")
    print("          than expected if the two were independent.")
    print("\nThese are historical associations, not proof of causation.")
    print("Sales-category relationships are descriptive, not sales forecasts.")

    print("\nGenerated files:")
    print(f"- {itemsets_path.relative_to(PROJECT_DIR)}")
    print(f"- {rules_path.relative_to(PROJECT_DIR)}")
    print("\nAnalysis completed.")


if __name__ == "__main__":
    main()
