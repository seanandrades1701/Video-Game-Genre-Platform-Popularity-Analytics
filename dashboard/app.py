import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="GameAnalytics",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "dataset" / "vgsales_transformed.csv"


# ============================================================
# COLOR PALETTE
# ============================================================

GREEN = "#00E676"
GREEN_DARK = "#00C853"
GREEN_LIGHT = "#69F0AE"
GREEN_DEEP = "#073B2A"

BLACK = "#050807"
BLACK_2 = "#080D0B"

CARD = "#0C1411"
CARD_2 = "#101A16"

BORDER = "#1D332A"

TEXT = "#F5F7F6"
TEXT_MUTED = "#8FA3A0"


# ============================================================
# HTML HELPER
# ============================================================
# This is the important fix.
# Every multiline HTML block goes through dedent().
# Therefore Streamlit will not display the HTML as a code block.

def html(content):
    clean_html = "\n".join(
        line.strip()
        for line in content.splitlines()
        if line.strip()
    )

    st.html(clean_html)


# ============================================================
# GLOBAL CSS
# ============================================================

html(f"""
<style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {{
        background:
            radial-gradient(
                circle at 75% 10%,
                rgba(0, 230, 118, 0.07),
                transparent 28%
            ),
            radial-gradient(
                circle at 15% 70%,
                rgba(0, 200, 83, 0.035),
                transparent 30%
            ),
            {BLACK};
        color: {TEXT};
    }}

    .main {{
        background: transparent;
    }}

    .block-container {{
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 4rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }}

    /* Remove Streamlit decoration */

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    header {{
        background: transparent !important;
    }}

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                #07100C 0%,
                #050807 100%
            );
        border-right: 1px solid {BORDER};
    }}

    section[data-testid="stSidebar"] > div {{
        padding-top: 1.5rem;
    }}

    .sidebar-brand {{
        padding: 12px 4px 25px 4px;
    }}

    .brand-title {{
        color: {TEXT};
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }}

    .brand-title span {{
        color: {GREEN};
    }}

    .brand-subtitle {{
        color: {TEXT_MUTED};
        font-size: 12px;
        line-height: 1.5;
    }}

    .sidebar-divider {{
        height: 1px;
        background: {BORDER};
        margin: 10px 0 25px 0;
    }}

    .sidebar-section-title {{
        color: {GREEN};
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin: 22px 0 12px 0;
    }}

        /* ========================================================
       SIDEBAR WIDGETS
       ======================================================== */

    /* Select / Multiselect */

    div[data-baseweb="select"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    div[data-baseweb="select"] > div {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 10px !important;
        color: {TEXT} !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    /* Remove Streamlit/BaseWeb red/orange focus */

    div[data-baseweb="select"] > div:focus {{
        border-color: {GREEN} !important;
        box-shadow: 0 0 0 1px {GREEN} !important;
        outline: none !important;
    }}

    div[data-baseweb="select"] > div:focus-within {{
        border-color: {GREEN} !important;
        box-shadow: 0 0 0 1px {GREEN} !important;
        outline: none !important;
    }}

    div[data-baseweb="select"]:focus-within {{
        border-color: {GREEN} !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    /* Hover */

    div[data-baseweb="select"] > div:hover {{
        border-color: {GREEN_DARK} !important;
    }}

    /* Text */

    div[data-baseweb="select"] span {{
        color: {TEXT} !important;
    }}

    div[data-baseweb="select"] input {{
        color: {TEXT} !important;
        caret-color: {GREEN} !important;
    }}

    div[data-baseweb="select"] input::placeholder {{
        color: {TEXT_MUTED} !important;
        opacity: 1 !important;
    }}

    /* Dropdown */

    div[data-baseweb="popover"] {{
        background: {CARD_2} !important;
        border: 1px solid {BORDER} !important;
    }}

    div[role="listbox"] {{
        background: {CARD_2} !important;
        border: 1px solid {BORDER} !important;
    }}

    /* Dropdown options */

    div[role="option"] {{
        background: {CARD_2} !important;
        color: {TEXT} !important;
    }}

    div[role="option"]:hover {{
        background: {GREEN_DEEP} !important;
        color: {GREEN_LIGHT} !important;
    }}

    div[role="option"][aria-selected="true"] {{
        background: {GREEN_DEEP} !important;
        color: {GREEN_LIGHT} !important;
    }}

    /* Multiselect tags */

    span[data-baseweb="tag"] {{
        background: {GREEN_DEEP} !important;
        border: 1px solid {GREEN_DARK} !important;
        color: {GREEN_LIGHT} !important;
    }}

    span[data-baseweb="tag"] span {{
        color: {GREEN_LIGHT} !important;
    }}

    span[data-baseweb="tag"] svg {{
        fill: {GREEN_LIGHT} !important;
        color: {GREEN_LIGHT} !important;
    }}

    /* ========================================================
       SLIDER
       ======================================================== */

    div[data-testid="stSlider"] {{
        padding-top: 5px;
    }}

    div[data-testid="stSlider"] [data-baseweb="slider"] {{
        color: {GREEN} !important;
    }}

    div[data-testid="stSlider"] [role="slider"] {{
        background: {GREEN} !important;
        border-color: {GREEN} !important;
    }}

    div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {{
        background: {GREEN} !important;
    }}

    /* ========================================================
       HERO
       ======================================================== */

    .hero-section {{
        padding-top: 18px;
        padding-bottom: 55px;
        width: 100%;
    }}

    .hero-eyebrow {{
        color: {GREEN};
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 32px;
    }}

    .hero-title {{
        font-size: clamp(58px, 5.2vw, 92px);
        line-height: 0.98;
        font-weight: 800;
        letter-spacing: -4px;
        margin: 0;
        color: {TEXT};
        max-width: 1250px;
    }}

    .hero-title .accent {{
        color: {GREEN};
    }}

    .hero-description {{
        color: {TEXT_MUTED};
        max-width: 1100px;
        font-size: 17px;
        line-height: 1.8;
        margin-top: 30px;
    }}

    /* ========================================================
       META PILLS
       ======================================================== */

    .meta-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 35px;
    }}

    .meta-pill {{
        background: rgba(12, 20, 17, 0.9);
        border: 1px solid {BORDER};
        border-radius: 999px;
        padding: 8px 15px;
        color: {TEXT_MUTED};
        font-size: 12px;
    }}

    .meta-pill strong {{
        color: {GREEN};
        margin-right: 5px;
    }}

    /* ========================================================
       KPI CARDS
       ======================================================== */

    .kpi-card {{
        background:
            linear-gradient(
                145deg,
                {CARD_2},
                {CARD}
            );
        border: 1px solid {BORDER};
        border-radius: 18px;
        padding: 24px;
        min-height: 145px;
        position: relative;
        overflow: hidden;
    }}

    .kpi-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 55px;
        height: 3px;
        background: {GREEN};
        border-radius: 0 0 5px 0;
    }}

    .kpi-label {{
        color: {TEXT_MUTED};
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        margin-bottom: 15px;
    }}

    .kpi-value {{
        color: {TEXT};
        font-size: 35px;
        line-height: 1;
        font-weight: 800;
        letter-spacing: -1px;
    }}

    .kpi-sub {{
        color: {GREEN_LIGHT};
        font-size: 12px;
        margin-top: 12px;
    }}

    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    .section-title {{
        color: {TEXT};
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -0.7px;
        margin-top: 40px;
        margin-bottom: 6px;
    }}

    .section-description {{
        color: {TEXT_MUTED};
        font-size: 13px;
        margin-bottom: 20px;
    }}

    /* ========================================================
       CHART CARDS
       ======================================================== */

    .chart-header {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-bottom: none;
        border-radius: 16px 16px 0 0;
        padding: 18px 20px 5px 20px;
    }}

    .chart-title {{
        color: {TEXT};
        font-size: 15px;
        font-weight: 750;
    }}

    .chart-subtitle {{
        color: {TEXT_MUTED};
        font-size: 11px;
        margin-top: 3px;
    }}

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {{
        width: 100%;
        background: {CARD};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.2s ease;
    }}

    .stButton > button:hover {{
        background: {GREEN_DEEP};
        border-color: {GREEN};
        color: {GREEN_LIGHT};
    }}

    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {{
        color: {TEXT_MUTED} !important;
        font-weight: 700 !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {GREEN} !important;
    }}

    div[data-baseweb="tab-highlight"] {{
        background-color: {GREEN} !important;
    }}

    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 12px;
        overflow: hidden;
    }}

    /* ========================================================
       INFO BOX
       ======================================================== */

    .info-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 18px;
    }}

    .info-card h3 {{
        color: {GREEN};
        font-size: 17px;
        margin-bottom: 10px;
    }}

    .info-card p {{
        color: {TEXT_MUTED};
        line-height: 1.7;
        font-size: 13px;
    }}

    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {{
        margin-top: 70px;
        padding-top: 25px;
        border-top: 1px solid {BORDER};
        color: {TEXT_MUTED};
        font-size: 11px;
        text-align: center;
    }}

    .footer span {{
        color: {GREEN};
    }}

    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 900px) {{

        .block-container {{
            padding-left: 1.2rem;
            padding-right: 1.2rem;
        }}

        .hero-title {{
            font-size: 55px;
            letter-spacing: -3px;
        }}

        .hero-description {{
            font-size: 15px;
        }}

    }}

</style>
""")


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    if not DATA_PATH.exists():
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH)

    # Make sure numeric columns are numeric
    numeric_columns = [
        "Year",
        "NA_Sales",
        "EU_Sales",
        "JP_Sales",
        "Other_Sales",
        "Global_Sales"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Create Decade if it does not exist
    if "Decade" not in df.columns and "Year" in df.columns:
        df["Decade"] = (
            (df["Year"] // 10) * 10
        ).astype("Int64")

    return df


df = load_data()


# ============================================================
# ERROR IF DATASET NOT FOUND
# ============================================================

if df.empty:

    st.error(
        "Dataset not found. Please make sure "
        "'dataset/vgsales_transformed.csv' exists."
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Dashboard"


if "reset_filters" not in st.session_state:
    st.session_state.reset_filters = False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    html("""
    <div class="sidebar-brand">

        <div class="brand-title">
            GAME<span>ANALYTICS</span>
        </div>

        <div class="brand-subtitle">
            Big Data Analytics Project
        </div>

    </div>

    <div class="sidebar-divider"></div>
    """)

    html("""
    <div class="sidebar-section-title">
        Navigation
    </div>
    """)

    page = st.radio(
        "",
        [
            "Dashboard",
            "Analytics",
            "Dataset",
            "About Project"
        ],
        key="navigation"
    )

    html("""
    <div class="sidebar-section-title">
        Filters
    </div>
    """)

    genres = sorted(
        df["Genre"].dropna().unique().tolist()
    ) if "Genre" in df.columns else []

    platforms = sorted(
        df["Platform"].dropna().unique().tolist()
    ) if "Platform" in df.columns else []

    publishers = sorted(
        df["Publisher"].dropna().unique().tolist()
    ) if "Publisher" in df.columns else []

    years = sorted(
        df["Year"].dropna().astype(int).unique().tolist()
    ) if "Year" in df.columns else []

    min_year = min(years) if years else 1980
    max_year = max(years) if years else 2020

    selected_genres = st.multiselect(
        "Genre",
        genres,
        placeholder="All Genres"
    )

    selected_platforms = st.multiselect(
        "Platform",
        platforms,
        placeholder="All Platforms"
    )

    selected_publishers = st.multiselect(
        "Publisher",
        publishers,
        placeholder="All Publishers"
    )

    selected_years = st.slider(
        "Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    st.write("")

    if st.button("Reset Filters"):

        st.session_state.reset_filters = True

        st.rerun()

    html("""
    <div class="sidebar-divider"></div>

    <div style="
        color:#8FA3A0;
        font-size:11px;
        line-height:1.7;
    ">
        Interactive exploration of historical
        video game sales data.
    </div>
    """)


# ============================================================
# RESET FILTERS
# ============================================================

if st.session_state.reset_filters:

    selected_genres = []
    selected_platforms = []
    selected_publishers = []
    selected_years = (min_year, max_year)

    st.session_state.reset_filters = False


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df.copy()


if selected_genres:
    filtered_df = filtered_df[
        filtered_df["Genre"].isin(selected_genres)
    ]


if selected_platforms:
    filtered_df = filtered_df[
        filtered_df["Platform"].isin(selected_platforms)
    ]


if selected_publishers:
    filtered_df = filtered_df[
        filtered_df["Publisher"].isin(selected_publishers)
    ]


if "Year" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Year"].between(
            selected_years[0],
            selected_years[1]
        )
    ]


# ============================================================
# PLOTLY THEME
# ============================================================

PLOTLY_TEMPLATE = "plotly_dark"


def style_chart(fig, height=390):

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial",
            color=TEXT
        ),
        margin=dict(
            l=30,
            r=25,
            t=25,
            b=45
        ),
        hoverlabel=dict(
            bgcolor=CARD_2,
            font_color=TEXT
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                color=TEXT_MUTED
            )
        )
    )

    fig.update_xaxes(
        gridcolor=BORDER,
        zerolinecolor=BORDER
    )

    fig.update_yaxes(
        gridcolor=BORDER,
        zerolinecolor=BORDER
    )

    return fig


# ============================================================
# PAGE: DASHBOARD
# ============================================================

if page == "Dashboard":

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    html("""
    <div class="hero-section">

        <div class="hero-eyebrow">
            DATA DRIVES PLAY
        </div>

        <h1 class="hero-title">
            Video Game Genre &<br>
            <span class="accent">Platform Popularity</span> Analytics
        </h1>

        <div class="hero-description">
            An interactive analysis of historical video game sales revealing
            patterns across genres, platforms, publishers, regions and release periods.
        </div>

    </div>
    """)

    # --------------------------------------------------------
    # META
    # --------------------------------------------------------

    html(f"""
    <div class="meta-row">

        <div class="meta-pill">
            <strong>{len(filtered_df):,}</strong>
            records
        </div>

        <div class="meta-pill">
            <strong>{filtered_df["Genre"].nunique()}</strong>
            genres
        </div>

        <div class="meta-pill">
            <strong>{filtered_df["Platform"].nunique()}</strong>
            platforms
        </div>

        <div class="meta-pill">
            <strong>{filtered_df["Publisher"].nunique()}</strong>
            publishers
        </div>

    </div>
    """)

    # --------------------------------------------------------
    # KPI VALUES
    # --------------------------------------------------------

    total_games = len(filtered_df)

    global_sales = (
        filtered_df["Global_Sales"].sum()
        if not filtered_df.empty
        else 0
    )

    genre_count = (
        filtered_df["Genre"].nunique()
        if not filtered_df.empty
        else 0
    )

    platform_count = (
        filtered_df["Platform"].nunique()
        if not filtered_df.empty
        else 0
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        html(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Games Analysed
            </div>

            <div class="kpi-value">
                {total_games:,}
            </div>

            <div class="kpi-sub">
                Selected records
            </div>

        </div>
        """)

    with k2:

        html(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Global Sales
            </div>

            <div class="kpi-value">
                {global_sales:,.1f}M
            </div>

            <div class="kpi-sub">
                Worldwide sales
            </div>

        </div>
        """)

    with k3:

        html(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Genres
            </div>

            <div class="kpi-value">
                {genre_count}
            </div>

            <div class="kpi-sub">
                Categories represented
            </div>

        </div>
        """)

    with k4:

        html(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Platforms
            </div>

            <div class="kpi-value">
                {platform_count}
            </div>

            <div class="kpi-sub">
                Gaming platforms
            </div>

        </div>
        """)

    # --------------------------------------------------------
    # SECTION
    # --------------------------------------------------------

    html("""
    <div class="section-title">
        Market Overview
    </div>

    <div class="section-description">
        Explore the major patterns across genres, platforms and regions.
    </div>
    """)

    # --------------------------------------------------------
    # GENRE CHART
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        html("""
        <div class="chart-header">

            <div class="chart-title">
                Global Sales by Genre
            </div>

            <div class="chart-subtitle">
                Total worldwide sales in millions
            </div>

        </div>
        """)

        if not filtered_df.empty:

            genre_data = (
                filtered_df
                .groupby("Genre")["Global_Sales"]
                .sum()
                .sort_values(ascending=True)
                .reset_index()
            )

            fig = px.bar(
                genre_data,
                x="Global_Sales",
                y="Genre",
                orientation="h",
                text="Global_Sales"
            )

            fig.update_traces(
                marker_color=GREEN,
                texttemplate="%{text:.1f}M",
                textposition="outside"
            )

            fig.update_layout(
                showlegend=False,
                xaxis_title="Global Sales (Millions)",
                yaxis_title=""
            )

            fig = style_chart(fig, 440)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # --------------------------------------------------------
    # PLATFORM CHART
    # --------------------------------------------------------

    with col2:

        html("""
        <div class="chart-header">

            <div class="chart-title">
                Top Platforms
            </div>

            <div class="chart-subtitle">
                Platforms ranked by global sales
            </div>

        </div>
        """)

        if not filtered_df.empty:

            platform_data = (
                filtered_df
                .groupby("Platform")["Global_Sales"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .sort_values()
                .reset_index()
            )

            fig = px.bar(
                platform_data,
                x="Global_Sales",
                y="Platform",
                orientation="h",
                text="Global_Sales"
            )

            fig.update_traces(
                marker_color=GREEN_LIGHT,
                texttemplate="%{text:.1f}M",
                textposition="outside"
            )

            fig.update_layout(
                showlegend=False,
                xaxis_title="Global Sales (Millions)",
                yaxis_title=""
            )

            fig = style_chart(fig, 440)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # --------------------------------------------------------
    # REGIONAL SALES
    # --------------------------------------------------------

    html("""
    <div class="section-title">
        Regional Performance
    </div>

    <div class="section-description">
        Compare sales distribution across major geographic markets.
    </div>
    """)

    regional_columns = {
        "North America": "NA_Sales",
        "Europe": "EU_Sales",
        "Japan": "JP_Sales",
        "Other": "Other_Sales"
    }

    regional_values = []

    for region, column in regional_columns.items():

        if column in filtered_df.columns:

            regional_values.append({
                "Region": region,
                "Sales": filtered_df[column].sum()
            })

    regional_df = pd.DataFrame(regional_values)

    if not regional_df.empty:

        fig = px.bar(
            regional_df,
            x="Region",
            y="Sales",
            text="Sales"
        )

        fig.update_traces(
            marker_color=GREEN,
            texttemplate="%{text:.1f}M",
            textposition="outside"
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Sales (Millions)"
        )

        fig = style_chart(fig, 380)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # TIME + TOP GAMES
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        html("""
        <div class="chart-header">

            <div class="chart-title">
                Global Sales Over Time
            </div>

            <div class="chart-subtitle">
                Historical yearly sales trend
            </div>

        </div>
        """)

        if not filtered_df.empty:

            yearly = (
                filtered_df
                .groupby("Year")["Global_Sales"]
                .sum()
                .reset_index()
                .sort_values("Year")
            )

            fig = px.line(
                yearly,
                x="Year",
                y="Global_Sales",
                markers=True
            )

            fig.update_traces(
                line=dict(
                    color=GREEN,
                    width=3
                ),
                marker=dict(
                    color=GREEN,
                    size=6
                )
            )

            fig.update_layout(
                showlegend=False,
                xaxis_title="Year",
                yaxis_title="Global Sales (Millions)"
            )

            fig = style_chart(fig, 400)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with col2:

        html("""
        <div class="chart-header">

            <div class="chart-title">
                Top 10 Games
            </div>

            <div class="chart-subtitle">
                Best-selling games by global sales
            </div>

        </div>
        """)

        if not filtered_df.empty:

            top_games = (
                filtered_df[
                    ["Name", "Global_Sales"]
                ]
                .sort_values(
                    "Global_Sales",
                    ascending=False
                )
                .head(10)
                .sort_values("Global_Sales")
            )

            fig = px.bar(
                top_games,
                x="Global_Sales",
                y="Name",
                orientation="h",
                text="Global_Sales"
            )

            fig.update_traces(
                marker_color=GREEN_LIGHT,
                texttemplate="%{text:.2f}M",
                textposition="outside"
            )

            fig.update_layout(
                showlegend=False,
                xaxis_title="Global Sales (Millions)",
                yaxis_title=""
            )

            fig = style_chart(fig, 400)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # --------------------------------------------------------
    # SALES CATEGORY
    # --------------------------------------------------------

    html("""
    <div class="section-title">
        Sales Distribution
    </div>

    <div class="section-description">
        Distribution of games based on global sales categories.
    </div>
    """)

    if "Sales_Category" in filtered_df.columns:

        category_data = (
            filtered_df["Sales_Category"]
            .value_counts()
            .reset_index()
        )

        category_data.columns = [
            "Sales_Category",
            "Count"
        ]

        fig = px.pie(
            category_data,
            names="Sales_Category",
            values="Count",
            hole=0.62
        )

        fig.update_traces(
            textposition="outside",
            textinfo="percent+label",
            marker=dict(
                colors=[
                    GREEN_DEEP,
                    GREEN_DARK,
                    GREEN,
                    GREEN_LIGHT
                ]
            )
        )

        fig.update_layout(
            showlegend=True
        )

        fig = style_chart(fig, 430)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PAGE: ANALYTICS
# ============================================================

elif page == "Analytics":

    html("""
    <div class="hero-section">

        <div class="hero-eyebrow">
            DEEP DIVE
        </div>

        <h1 class="hero-title">
            Analytics <span class="accent">Explorer</span>
        </h1>

        <div class="hero-description">
            Explore detailed patterns across genres, platforms,
            publishers, regions and release periods.
        </div>

    </div>
    """)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Genre",
        "Platform",
        "Publisher",
        "Regional",
        "Time"
    ])

    # --------------------------------------------------------
    # GENRE TAB
    # --------------------------------------------------------

    with tab1:

        html("""
        <div class="section-title">
            Genre Analysis
        </div>

        <div class="section-description">
            Compare the performance and popularity of different game genres.
        </div>
        """)

        genre_analysis = (
            filtered_df
            .groupby("Genre")
            .agg(
                Games=("Name", "count"),
                Global_Sales=("Global_Sales", "sum"),
                Average_Sales=("Global_Sales", "mean")
            )
            .sort_values(
                "Global_Sales",
                ascending=False
            )
            .reset_index()
        )

        st.dataframe(
            genre_analysis,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # PLATFORM TAB
    # --------------------------------------------------------

    with tab2:

        html("""
        <div class="section-title">
            Platform Analysis
        </div>

        <div class="section-description">
            Identify the platforms with the strongest historical sales.
        </div>
        """)

        platform_analysis = (
            filtered_df
            .groupby("Platform")
            .agg(
                Games=("Name", "count"),
                Global_Sales=("Global_Sales", "sum"),
                Average_Sales=("Global_Sales", "mean")
            )
            .sort_values(
                "Global_Sales",
                ascending=False
            )
            .reset_index()
        )

        st.dataframe(
            platform_analysis,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # PUBLISHER TAB
    # --------------------------------------------------------

    with tab3:

        html("""
        <div class="section-title">
            Publisher Analysis
        </div>

        <div class="section-description">
            Explore publisher performance based on game releases and sales.
        </div>
        """)

        publisher_analysis = (
            filtered_df
            .groupby("Publisher")
            .agg(
                Games=("Name", "count"),
                Global_Sales=("Global_Sales", "sum"),
                Average_Sales=("Global_Sales", "mean")
            )
            .sort_values(
                "Global_Sales",
                ascending=False
            )
            .head(30)
            .reset_index()
        )

        st.dataframe(
            publisher_analysis,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # REGIONAL TAB
    # --------------------------------------------------------

    with tab4:

        html("""
        <div class="section-title">
            Regional Analysis
        </div>

        <div class="section-description">
            Examine how gaming sales are distributed across geographic regions.
        </div>
        """)

        regional_table = pd.DataFrame({
            "Region": [
                "North America",
                "Europe",
                "Japan",
                "Other"
            ],
            "Sales": [
                filtered_df["NA_Sales"].sum(),
                filtered_df["EU_Sales"].sum(),
                filtered_df["JP_Sales"].sum(),
                filtered_df["Other_Sales"].sum()
            ]
        })

        regional_table["Percentage"] = (
            regional_table["Sales"]
            / regional_table["Sales"].sum()
            * 100
        )

        st.dataframe(
            regional_table,
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            regional_table,
            x="Region",
            y="Sales",
            text="Sales"
        )

        fig.update_traces(
            marker_color=GREEN,
            texttemplate="%{text:.2f}M",
            textposition="outside"
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Sales (Millions)"
        )

        fig = style_chart(fig, 420)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # TIME TAB
    # --------------------------------------------------------

    with tab5:

        html("""
        <div class="section-title">
            Time Analysis
        </div>

        <div class="section-description">
            Examine historical release and sales trends.
        </div>
        """)

        yearly_analysis = (
            filtered_df
            .groupby("Year")
            .agg(
                Games=("Name", "count"),
                Global_Sales=("Global_Sales", "sum")
            )
            .reset_index()
            .sort_values("Year")
        )

        st.dataframe(
            yearly_analysis,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PAGE: DATASET
# ============================================================

elif page == "Dataset":

    html("""
    <div class="hero-section">

        <div class="hero-eyebrow">
            DATA EXPLORER
        </div>

        <h1 class="hero-title">
            Dataset <span class="accent">Explorer</span>
        </h1>

        <div class="hero-description">
            Browse the cleaned and transformed video game sales dataset
            used throughout this analysis.
        </div>

    </div>
    """)

    # --------------------------------------------------------
    # DATASET STATS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        html(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Rows
            </div>

            <div class="kpi-value">
                {len(filtered_df):,}
            </div>

            <div class="kpi-sub">
                Filtered records
            </div>

        </div>
        """)

    with c2:

        html(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Columns
            </div>

            <div class="kpi-value">
                {len(filtered_df.columns)}
            </div>

            <div class="kpi-sub">
                Dataset attributes
            </div>

        </div>
        """)

    with c3:

        html(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Genres
            </div>

            <div class="kpi-value">
                {filtered_df["Genre"].nunique()}
            </div>

            <div class="kpi-sub">
                Unique categories
            </div>

        </div>
        """)

    with c4:

        html(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Platforms
            </div>

            <div class="kpi-value">
                {filtered_df["Platform"].nunique()}
            </div>

            <div class="kpi-sub">
                Unique platforms
            </div>

        </div>
        """)

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    html("""
    <div class="section-title">
        Records
    </div>

    <div class="section-description">
        Current dataset after applying the selected filters.
    </div>
    """)

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=600,
        hide_index=True
    )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Dataset",
        data=csv_data,
        file_name="vgsales_filtered.csv",
        mime="text/csv"
    )


# ============================================================
# PAGE: ABOUT PROJECT
# ============================================================

elif page == "About Project":

    html("""
    <div class="hero-section">

        <div class="hero-eyebrow">
            PROJECT INFORMATION
        </div>

        <h1 class="hero-title">
            About <span class="accent">The Project</span>
        </h1>

        <div class="hero-description">
            Video Game Genre & Platform Popularity Analytics
            is a Big Data Analytics project focused on discovering
            historical patterns in the video game industry.
        </div>

    </div>
    """)

    # --------------------------------------------------------
    # OBJECTIVE
    # --------------------------------------------------------

    html("""
    <div class="info-card">

        <h3>
            Project Objective
        </h3>

        <p>
            The objective of this project is to analyze historical
            video game sales data and identify meaningful patterns
            across genres, platforms, publishers, geographic regions
            and release periods.
        </p>

    </div>
    """)

    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

    html("""
    <div class="info-card">

        <h3>
            Dataset
        </h3>

        <p>
            The project uses the VGSales dataset containing historical
            video game information including game names, platforms,
            genres, publishers, release years and regional sales.
        </p>

    </div>
    """)

    # --------------------------------------------------------
    # TECHNOLOGY
    # --------------------------------------------------------

    html("""
    <div class="info-card">

        <h3>
            Technology Stack
        </h3>

        <p>
            Python · Pandas · NumPy · Plotly · Matplotlib · Seaborn ·
            Streamlit · VS Code
        </p>

    </div>
    """)

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    html("""
    <div class="info-card">

        <h3>
            Analytics Performed
        </h3>

        <p>
            Genre analysis, platform analysis, publisher analysis,
            regional sales analysis, yearly trends, decade analysis,
            top-selling games, genre-platform relationships and
            sales-category analysis.
        </p>

    </div>
    """)

    # --------------------------------------------------------
    # PROJECT FINDINGS
    # --------------------------------------------------------

    html("""
    <div class="section-title">
        Key Findings
    </div>

    <div class="section-description">
        Major observations from the analyzed dataset.
    </div>
    """)

    finding1, finding2 = st.columns(2)

    with finding1:

        html("""
        <div class="info-card">

            <h3>
                Genre Performance
            </h3>

            <p>
                Action games generated the highest overall global
                sales among the analyzed genres.
            </p>

        </div>
        """)

    with finding2:

        html("""
        <div class="info-card">

            <h3>
                Platform Performance
            </h3>

            <p>
                PlayStation 2 recorded the highest total global
                sales among the platforms in the cleaned dataset.
            </p>

        </div>
        """)

    finding3, finding4 = st.columns(2)

    with finding3:

        html("""
        <div class="info-card">

            <h3>
                Regional Market
            </h3>

            <p>
                North America represented the largest share of
                regional sales in the dataset.
            </p>

        </div>
        """)

    with finding4:

        html("""
        <div class="info-card">

            <h3>
                Historical Period
            </h3>

            <p>
                The 2000s contained the largest number of games
                and the highest overall sales among the analyzed decades.
            </p>

        </div>
        """)


# ============================================================
# FOOTER
# ============================================================

html("""
<div class="footer">
    Video Game Genre & Platform Popularity Analytics
    · Built with <span>Python</span> and <span>Streamlit</span>
</div>
""")