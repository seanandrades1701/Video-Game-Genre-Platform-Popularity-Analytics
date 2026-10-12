# Video Game Genre & Platform Popularity Analytics

**Explore gaming trends. Compare platforms. Discover what drives video game sales.**

An interactive data analytics platform that transforms historical video game sales data into actionable insights through data processing, statistical analysis, machine learning, and interactive visualizations.

Built with Python, Pandas, Plotly, Scikit-learn, and Streamlit.

---

## Overview

Video Game Genre & Platform Popularity Analytics provides a unified way to explore historical video game sales across genres, gaming platforms, publishers, regions, and release periods.

The project combines a data processing pipeline with an interactive dashboard, enabling users to investigate sales patterns, compare market performance, explore regional preferences, and examine relationships between game characteristics and commercial success.

## Key Features

- **Interactive Dashboard** — Explore sales metrics and visualizations through a Streamlit interface.
- **Genre Analytics** — Compare genres by total sales, average performance, and number of games.
- **Platform Comparison** — Identify leading gaming platforms and compare their historical performance.
- **Publisher Insights** — Analyze publisher portfolios and sales performance.
- **Regional Analysis** — Compare North American, European, Japanese, and other regional sales.
- **Historical Trends** — Investigate yearly and decade-wise changes in releases and sales.
- **Game Rankings** — Explore the highest-selling titles in the dataset.
- **Genre–Platform Analysis** — Examine sales patterns across genre and platform combinations.
- **Sales Segmentation** — Group games into Low, Medium, High, and Very High global sales categories.
- **Machine Learning** — Apply clustering, regression, and classification to explore patterns in game sales.
- **Interactive Filtering** — Filter data by multiple genres, platforms, publishers, and release years.
- **Exportable Results** — Access analytical outputs stored as CSV files.

## Analytics Dashboard

The dashboard provides a centralized interface for exploring the project's results.

| Section | Description |
|---|---|
| Dashboard | High-level metrics and an overview of video game sales |
| Analytics | Detailed comparisons across genres, platforms, publishers, and regions |
| Dataset | Explore the processed dataset and its records |
| Machine Learning | Examine clustering, regression, classification, and model results |
| About Project | Project information and analytical context |

The interface uses interactive charts to make comparisons and patterns easier to investigate.

## Machine Learning

Three complementary machine learning approaches are implemented alongside a clustering workflow.

| Model | Objective | Result |
|---|---|---|
| K-Means Clustering | Group games using regional sales patterns | Selected \(K=2\); silhouette score: 0.7748 |
| Random Forest Regression | Estimate global sales from game attributes | \(R^2 = 0.1074\) |
| Gradient Boosting Regression | Compare an alternative sales prediction model | \(R^2 = 0.0911\) |
| Random Forest Classification | Classify games into sales categories | Accuracy: 79.56% |

The regression models have limited predictive power, so their results should be interpreted cautiously. The classification accuracy also requires context: the dataset is highly imbalanced, with most games belonging to the Low sales category.

The machine learning components are intended to explore data patterns and evaluate model performance, rather than guarantee accurate predictions of commercial success.

## Selected Insights

The analysis of the cleaned dataset produced the following findings:

| Area | Finding |
|---|---|
| Leading genre | Action |
| Leading platform | PlayStation 2 (PS2) |
| Leading publisher by total sales | Nintendo |
| Largest regional sales share | North America — 49.14% |
| Highest-sales year | 2008 |
| Highest-sales decade | The 2000s |
| Highest-selling game | Wii Sports — 82.74 million units |

These findings reflect the available dataset and its historical coverage, not the current state of the gaming market.

## Data Pipeline

The project follows a structured workflow from raw data to interactive exploration.

```text
Raw VGSales Dataset
        |
        v
Data Validation
        |
        v
Data Cleaning
        |
        v
Feature Engineering
        |
        v
Exploratory Data Analysis
        |
        v
Statistical Aggregation
        |
        v
Machine Learning
        |
        v
Visualization & Results
        |
        v
Interactive Streamlit Dashboard
```

### Data Processing

The original dataset contains 16,598 records and 11 columns.

Processing includes:

- Checking data quality and duplicate records.
- Handling missing release years and publisher values.
- Validating sales values and data types.
- Creating decade and sales-category features.
- Calculating regional sales totals and percentages.

The cleaned dataset contains **16,291 records**. The transformed dataset contains 18 columns for additional analytical exploration.

### Sales Categories

Games are segmented by recorded global sales:

| Category | Global sales |
|---|---:|
| Low | Less than 1 million |
| Medium | 1 million to less than 5 million |
| High | 5 million to less than 10 million |
| Very High | 10 million or more |

## Technology Stack

| Technology | Role |
|---|---|
| Python | Data processing and application logic |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Matplotlib & Seaborn | Static data visualization |
| Plotly | Interactive charts |
| Scikit-learn | Machine learning and model evaluation |
| Streamlit | Interactive web dashboard |
| Git & GitHub | Version control and source management |

## Project Structure

```text
Video-Game-Genre-Platform-Popularity-Analytics/
│
├── dataset/
│   ├── vgsales.csv
│   ├── vgsales_cleaned.csv
│   └── vgsales_transformed.csv
│
├── src/
│   ├── check_dataset.py
│   ├── data_cleaning.py
│   ├── data_transformation.py
│   ├── genre_analysis.py
│   ├── platform_analysis.py
│   ├── publisher_analysis.py
│   ├── regional_analysis.py
│   ├── year_analysis.py
│   ├── top_games_analysis.py
│   ├── genre_platform_analysis.py
│   ├── sales_category_analysis.py
│   ├── visualization.py
│   ├── kmeans_clustering.py
│   ├── random_forest_regression.py
│   ├── gradient_boosting_regression.py
│   ├── compare_regression_models.py
│   └── random_forest_classification.py
│
├── dashboard/
│   └── app.py
│
├── results/
│   └── Analytical outputs and model evaluation CSVs
│
├── visualizations/
│   └── Generated charts and model evaluation plots
│
├── requirements.txt
├── .gitignore
└── README.md
```

*The structure above describes the main project components. Individual files may differ depending on the latest repository version.*

## Getting Started

### Prerequisites

- Python 3.10 or a compatible newer version supported by the installed dependencies.
- Git.
- A terminal or code editor such as Visual Studio Code.

### 1. Clone the repository

```bash
git clone https://github.com/seanandrades1701/Video-Game-Genre-Platform-Popularity-Analytics.git
```

```bash
cd Video-Game-Genre-Platform-Popularity-Analytics
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```cmd
venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Launch the dashboard

From the project root, run:

```bash
streamlit run dashboard/app.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`, where you can explore the dashboard.

## Running the Analysis Scripts

Run the following commands from the project root when you want to regenerate the corresponding data or results.

**Data validation and preprocessing**

```bash
python src/check_dataset.py
python src/data_cleaning.py
python src/data_transformation.py
```

**Generate analytical visualizations**

```bash
python src/visualization.py
```

**Machine learning**

```bash
python src/kmeans_clustering.py
python src/random_forest_regression.py
python src/gradient_boosting_regression.py
python src/compare_regression_models.py
python src/random_forest_classification.py
```

Run the data processing steps before downstream scripts if their required cleaned or transformed files do not already exist. The exact dependencies between scripts depend on their input and output paths.

## Deployment

The Streamlit dashboard can be hosted using [Streamlit Community Cloud](https://share.streamlit.io/).

Typical deployment configuration:

- **Repository:** `seanandrades1701/Video-Game-Genre-Platform-Popularity-Analytics`
- **Branch:** `main`
- **Main file:** `dashboard/app.py`

Ensure that `requirements.txt` includes every package imported by the dashboard and that the required dataset files are available in the deployed repository or through an explicitly configured data source.

A custom domain is not required for a standard Streamlit Community Cloud deployment.

## Limitations

- The dataset represents historical sales rather than live market activity.
- Some release years have incomplete coverage.
- Regression performance is limited on the selected features.
- Sales-category imbalance affects classification metrics, especially for less common categories.
- Historical associations do not establish causation or guarantee future performance.

## Future Improvements

- Add richer filtering and cross-chart interactions.
- Improve model evaluation using stronger baselines and additional features.
- Explore time-series forecasting where the data supports it.
- Add model comparison and evaluation summaries to the dashboard.
- Automate dataset updates and processing.
- Improve deployment reliability and data-loading performance.

## Author

**Sean Andrades**

Developed using Python, Pandas, Scikit-learn, Plotly, and Streamlit.

## Acknowledgements

The project uses the VGSales dataset for historical video game sales analysis. Dataset attribution, licensing, and usage conditions should follow the terms of the original source.

---

**Explore the data. Understand the trends. Discover the patterns.**
