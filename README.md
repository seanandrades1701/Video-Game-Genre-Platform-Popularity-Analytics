# 🎮 Video Game Genre & Platform Popularity Analytics

> A Big Data Analytics project that analyzes historical video game sales data to identify trends, popularity patterns, regional preferences, and performance across genres, platforms, publishers, and release periods.

## 📌 Project Overview

The **Video Game Genre & Platform Popularity Analytics** project explores historical video game sales data to understand how games performed across different:

- 🎯 Genres
- 🎮 Gaming platforms
- 🏢 Publishers
- 🌎 Regions
- 📅 Years and decades
- 🏆 Individual game titles
- 📊 Sales categories

The project follows a complete data analytics pipeline:

```text
Raw Dataset
     ↓
Data Validation
     ↓
Data Cleaning
     ↓
Data Transformation
     ↓
Exploratory Analysis
     ↓
Statistical Aggregation
     ↓
Visualization
     ↓
Interactive Streamlit Dashboard
```

The final result is an interactive analytics dashboard that allows users to explore the dataset using filters and interactive visualizations.

---

## 🎯 Objectives

The primary objectives of this project are:

1. Analyze historical video game sales data.
2. Identify the most successful game genres.
3. Compare gaming platforms based on total sales.
4. Analyze publisher performance.
5. Study regional sales preferences.
6. Identify yearly and decade-wise sales trends.
7. Find the highest-selling individual games.
8. Analyze the relationship between genres and platforms.
9. Categorize games according to their global sales.
10. Build an interactive dashboard for exploring the results.

---

## ✨ Key Features

### 📊 Data Analysis

The project performs analysis across multiple dimensions:

- Genre-wise sales
- Platform-wise sales
- Publisher-wise sales
- Regional sales
- Year-wise sales
- Decade-wise sales
- Top-selling games
- Genre × Platform analysis
- Sales category distribution

### 🧹 Data Cleaning

The dataset is processed before analysis by:

- Removing duplicate records
- Handling missing years
- Handling missing publishers
- Converting year values into integer format
- Checking for negative sales values
- Validating the final dataset

### 🔄 Data Transformation

Additional analytical columns are generated, including:

- `Decade`
- `Sales_Category`
- `Regional_Total`
- `NA_Percentage`
- `EU_Percentage`
- `JP_Percentage`
- `Other_Percentage`

### 📈 Visualization

The project generates visualizations for:

- Global sales by genre
- Top platforms
- Top publishers
- Regional sales
- Yearly sales trends
- Decade-wise sales
- Genre-platform relationships
- Top 10 games
- Sales category distribution

### 🖥️ Interactive Dashboard

A Streamlit dashboard provides:

- Multi-select genre filtering
- Multi-select platform filtering
- Multi-select publisher filtering
- Year range filtering
- KPI cards
- Interactive Plotly charts
- Dataset exploration
- Analytical tabs
- CSV download functionality

---

# 📂 Project Structure

```text
VideoGame-BigData-Analytics/
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
│   └── visualization.py
│
├── results/
│   ├── genre_analysis.csv
│   ├── platform_analysis.csv
│   ├── publisher_analysis.csv
│   ├── regional_sales_analysis.csv
│   ├── genre_regional_analysis.csv
│   ├── year_analysis.csv
│   ├── decade_analysis.csv
│   ├── top_games_analysis.csv
│   ├── genre_platform_analysis.csv
│   ├── genre_platform_matrix.csv
│   └── sales_category_analysis.csv
│
├── visualizations/
│   ├── decade_sales.png
│   ├── genre_platform_heatmap.png
│   ├── global_sales_by_genre.png
│   ├── regional_sales.png
│   ├── sales_category_distribution.png
│   ├── top_10_games.png
│   ├── top_10_platforms.png
│   ├── top_10_publishers.png
│   └── yearly_sales_trend.png
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🗃️ Dataset

The project uses the **VGSales** video game sales dataset.

The original dataset contains historical information about video games, including:

| Column | Description |
|---|---|
| `Rank` | Ranking of the game |
| `Name` | Game title |
| `Platform` | Gaming platform |
| `Year` | Release year |
| `Genre` | Game genre |
| `Publisher` | Game publisher |
| `NA_Sales` | North American sales |
| `EU_Sales` | European sales |
| `JP_Sales` | Japanese sales |
| `Other_Sales` | Sales in other regions |
| `Global_Sales` | Global sales |

Sales values are represented in **millions of units**.

---

# 🧹 Data Cleaning

The original dataset contained:

```text
16,598 records
11 columns
```

The cleaning process includes:

### 1. Duplicate Removal

Duplicate records are checked and removed.

### 2. Missing Year Handling

Records with missing release years are removed because year-based analysis requires valid year values.

### 3. Missing Publisher Handling

Remaining records with missing publisher information are removed.

### 4. Data Type Conversion

The `Year` column is converted into integer format.

### 5. Sales Validation

Sales columns are checked for invalid negative values.

### Final Clean Dataset

```text
Records: 16,291
Columns: 11
Missing values: 0
Duplicate records: 0
Negative sales values: 0
```

---

# 🔄 Data Transformation

The cleaned dataset is transformed to support deeper analysis.

## Decade

The release year is converted into a decade category.

Example:

```text
1985 → 1980
1996 → 1990
2008 → 2000
2014 → 2010
```

## Sales Category

Games are categorized using their global sales:

| Category | Global Sales |
|---|---:|
| Low | < 1 million |
| Medium | 1 – < 5 million |
| High | 5 – < 10 million |
| Very High | ≥ 10 million |

## Regional Metrics

Additional regional metrics are calculated, including:

```text
Regional_Total
NA_Percentage
EU_Percentage
JP_Percentage
Other_Percentage
```

The transformed dataset contains:

```text
16,291 records
18 columns
```

---

# 📊 Analytics Performed

## 1. Genre Analysis

The genre analysis examines:

- Number of games
- Total global sales
- Average sales
- Maximum sales

### Key Finding

**Action** is the highest-selling genre by total global sales.

```text
Action
Total Sales: 1,722.84 million
```

Other major genres include:

- Sports
- Shooter
- Role-Playing
- Platform
- Misc
- Racing

---

## 2. Platform Analysis

Platforms are compared using

- Number of games
- Total global sales
- Average sales
- Maximum sales

### Key Finding

**PlayStation 2 (PS2)** has the highest total global sales among the analyzed platforms.

```text
PS2
Total Sales: 1,233.46 million
```

Other major platforms include:

- Xbox 360
- PlayStation 3
- Wii
- Nintendo DS
- PlayStation

---

## 3. Publisher Analysis

Publisher performance is analyzed based on:

- Number of games
- Total sales
- Average sales
- Maximum sales

### Key Findings

**Nintendo** has the highest total global sales:

```text
Nintendo
Total Sales: 1,784.43 million
```

**Electronic Arts** has the largest number of games in the analyzed publisher results:

```text
Electronic Arts
Games: 1,339
```

---

## 4. Regional Analysis

Global sales are divided into four regions:

```text
North America
Europe
Japan
Other
```

### Regional Distribution

| Region | Sales | Share |
|---|---:|---:|
| North America | 4,327.65M | 49.14% |
| Europe | 2,406.69M | 27.33% |
| Japan | 1,284.27M | 14.58% |
| Other | 788.91M | 8.96% |

### Key Finding

**North America contributes the largest share of recorded global sales.**

---

## 5. Year Analysis

The project analyzes game releases and sales over time.

### Key Findings

**2008** recorded the highest annual global sales:

```text
678.90 million
```

**2009** had the highest number of game releases:

```text
1,431 games
```

---

## 6. Decade Analysis

The dataset is grouped into decades.

### Key Finding

The **2000s** represent the largest period in the dataset by both:

- Number of game releases
- Total recorded global sales

```text
Games: 9,183
Sales: 4,636.08 million
```

> **Note:** The source dataset contains relatively sparse records for some later years. Therefore, recent-decade values should be interpreted as dataset coverage rather than a complete representation of the entire video game industry.

---

# 🏆 Top 10 Games

The highest-selling games in the cleaned dataset include:

| Rank | Game | Platform | Genre | Global Sales |
|---:|---|---|---|---:|
| 1 | Wii Sports | Wii | Sports | 82.74M |
| 2 | Super Mario Bros. | NES | Platform | 40.24M |
| 3 | Mario Kart Wii | Wii | Racing | 35.82M |
| 4 | Wii Sports Resort | Wii | Sports | 33.00M |
| 5 | Pokémon Red/Pokémon Blue | GB | Role-Playing | 31.37M |
| 6 | Tetris | GB | Puzzle | 30.26M |
| 7 | New Super Mario Bros. | DS | Platform | 30.01M |
| 8 | Wii Play | Wii | Misc | 29.02M |
| 9 | New Super Mario Bros. Wii | Wii | Platform | 28.62M |
| 10 | Duck Hunt | NES | Shooter | 28.31M |

### Highest-Selling Game

🏆 **Wii Sports**

```text
Global Sales: 82.74 million
Platform: Wii
Publisher: Nintendo
Genre: Sports
```

---

# 🔗 Genre × Platform Analysis

The project also examines how game genres are distributed across gaming platforms.

This analysis helps answer questions such as:

- Which genres are common on specific platforms?
- Which platforms have the highest sales within particular genres?
- How do genre preferences differ across platforms?
- Which genre-platform combinations contribute the most sales?

The results are stored in:

```text
results/genre_platform_analysis.csv
results/genre_platform_matrix.csv
```

A heatmap is also generated to visualize the relationship between genres and platforms.

---

# 📈 Visualizations

The project generates the following visualizations:

### Global Sales by Genre

Shows the total global sales generated by each genre.

### Top Platforms

Compares platforms based on total global sales.

### Top Publishers

Highlights publishers with the highest sales.

### Regional Sales

Shows the distribution of sales across regions.

### Yearly Sales Trend

Displays changes in global sales over time.

### Decade Sales

Compares sales across different decades.

### Genre × Platform Heatmap

Visualizes the relationship between genres and platforms.

### Top 10 Games

Displays the highest-selling games.

### Sales Category Distribution

Shows how games are distributed across sales categories.

---

# 🖥️ Interactive Dashboard

The project includes a Streamlit-based dashboard for interactive exploration.

The dashboard provides:

### Navigation

- Dashboard
- Analytics
- Dataset
- About Project

### Filters

Users can filter the dataset using:

- Genre
- Platform
- Publisher
- Year range

Multiple values can be selected for the categorical filters.

### KPI Metrics

The dashboard displays:

```text
Total Games
Global Sales
Number of Genres
Number of Platforms
```

### Interactive Charts

The dashboard uses Plotly to provide interactive:

- Bar charts
- Line charts
- Pie/donut charts
- Regional comparisons
- Top-game analysis
- Platform comparisons

---

# ⚙️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical processing |
| Matplotlib | Static visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive visualization |
| Streamlit | Interactive dashboard |
| Git | Version control |
| GitHub | Source code repository |
| VS Code | Development environment |

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/seanandrades1701/Video-Game-Genre-Platform-Popularity-Analytics.git
```

Move into the project directory:

```bash
cd Video-Game-Genre-Platform-Popularity-Analytics
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

If required, dependencies can also be installed using:

```powershell
pip install pandas numpy matplotlib seaborn plotly streamlit
```

---

# ▶️ Running the Project

## Run Data Processing

From the project root:

```powershell
python src/check_dataset.py
```

Run data cleaning:

```powershell
python src/data_cleaning.py
```

Run data transformation:

```powershell
python src/data_transformation.py
```

---

# 📊 Running the Analytics

Individual analysis scripts can be executed from the project root.

### Genre

```powershell
python src/genre_analysis.py
```

### Platform

```powershell
python src/platform_analysis.py
```

### Publisher

```powershell
python src/publisher_analysis.py
```

### Regional

```powershell
python src/regional_analysis.py
```

### Year

```powershell
python src/year_analysis.py
```

### Top Games

```powershell
python src/top_games_analysis.py
```

### Genre × Platform

```powershell
python src/genre_platform_analysis.py
```

### Sales Categories

```powershell
python src/sales_category_analysis.py
```

---

# 📈 Generate Visualizations

Run:

```powershell
python src/visualization.py
```

Generated charts are saved inside:

```text
visualizations/
```

---

# 🖥️ Run the Dashboard

From the project root:

```powershell
streamlit run dashboard/app.py
```

The dashboard will open in your browser.

---

# 🌐 Live Deployment

The dashboard can be deployed using **Streamlit Community Cloud**.

Deployment configuration:

```text
Repository:
seanandrades1701/Video-Game-Genre-Platform-Popularity-Analytics

Branch:
main

Main file:
dashboard/app.py
```

The application uses Streamlit's hosted `streamlit.app` URL rather than requiring a purchased custom domain.

---

# 📁 Output Files

Analysis results are exported as CSV files inside:

```text
results/
```

Examples:

```text
genre_analysis.csv
platform_analysis.csv
publisher_analysis.csv
regional_sales_analysis.csv
year_analysis.csv
decade_analysis.csv
top_games_analysis.csv
genre_platform_analysis.csv
sales_category_analysis.csv
```

This makes the analytical results reusable for further analysis, reporting, or visualization.

---

# 🔍 Key Findings

The analysis produced several notable findings:

### 🎯 Genre

**Action** generated the highest total global sales among the analyzed genres.

### 🎮 Platform

**PS2** recorded the highest total global sales among platforms.

### 🏢 Publisher

**Nintendo** recorded the highest total global sales among publishers.

### 🌎 Region

**North America** contributed the largest share of recorded sales.

### 📅 Year

**2008** recorded the highest annual global sales.

### 🗓️ Decade

The **2000s** had the largest number of games and the highest total recorded sales.

### 🏆 Individual Game

**Wii Sports** was the highest-selling individual game in the dataset.

---

# 💡 Project Significance

The project demonstrates how historical sales data can be transformed into meaningful business and analytical insights.

The analysis can help understand:

- Consumer preferences
- Platform popularity
- Genre performance
- Publisher performance
- Regional market differences
- Historical changes in the gaming industry
- Sales distribution patterns

The interactive dashboard makes these insights easier to explore than examining raw CSV data alone.

---

# 🔮 Future Scope

Possible future improvements include:

- Adding machine learning for sales prediction
- Predicting game success based on genre and platform
- Time-series forecasting
- Publisher recommendation analysis
- Regional preference prediction
- Advanced clustering of games
- Real-time or regularly updated datasets
- More advanced dashboard filtering
- Automated data ingestion pipelines
- Cloud-based deployment and storage
- Additional interactive visualizations

---

# ⚠️ Limitations

The project is based on the available VGSales dataset.

Important limitations include:

- The dataset represents historical records rather than current market data.
- Some release years have incomplete coverage.
- Sales figures represent recorded dataset values.
- Later-year records are comparatively sparse.
- The analysis describes historical patterns and does not establish causal relationships.

Therefore, conclusions should be interpreted within the scope of the dataset.

---

# 🧪 Project Workflow

```text
                    ┌──────────────────┐
                    │   VGSales CSV    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Dataset Checking │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Data Cleaning   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Transformation   │
                    └────────┬─────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │      Data Analytics          │
              ├──────────────────────────────┤
              │ Genre                        │
              │ Platform                     │
              │ Publisher                    │
              │ Region                       │
              │ Year / Decade                │
              │ Top Games                    │
              │ Genre × Platform             │
              │ Sales Categories             │
              └──────────────┬───────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Visualization   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Streamlit        │
                    │ Interactive      │
                    │ Dashboard        │
                    └──────────────────┘
```

---

# 👨‍💻 Author

**Sean Andrades**

Big Data Analytics Project

Developed using Python, Pandas, Plotly and Streamlit.

---

# 📚 Academic Context

This project was developed as part of the **Big Data Analysis (CSC702)** coursework.

The project demonstrates practical application of:

- Data preprocessing
- Data transformation
- Exploratory data analysis
- Statistical aggregation
- Data visualization
- Interactive analytics
- Python-based data processing
- Dashboard development

---

# 📜 License

This project is intended primarily for academic and educational purposes.

The dataset remains subject to its original source and usage terms.

---

## ⭐ Acknowledgement

This project uses the VGSales dataset for analytical purposes and demonstrates how historical video game sales data can be processed and visualized to discover meaningful patterns.

---

## ⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub.
