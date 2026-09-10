import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Content Analytics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }

        [data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 10px;
            padding: 18px;
        }

        h1 {
            font-size: 2.4rem;
        }

        h2 {
            margin-top: 1.5rem;
        }

        .insight-box {
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DONNEES
# ============================================================

DATA_FILE = "data/processed/netflix_titles_clean.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    if "date_added" in df.columns:
        df["date_added"] = pd.to_datetime(
            df["date_added"],
            errors="coerce"
        )

    return df


df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Content Analytics")

st.sidebar.markdown(
    "Exploration et analyse d'un catalogue de contenus."
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Vue d'ensemble",
        "Contenus",
        "Catégories",
        "Pays",
        "Classifications",
        "Durées",
        "Insights"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    f"{len(df):,} contenus disponibles".replace(",", " ")
)


# ============================================================
# FILTRES GLOBAUX
# ============================================================

st.sidebar.subheader("Filtres")

content_types = ["Tous"] + sorted(
    df["type"].dropna().unique().tolist()
)

selected_type = st.sidebar.selectbox(
    "Type de contenu",
    content_types
)

filtered_df = df.copy()

if selected_type != "Tous":
    filtered_df = filtered_df[
        filtered_df["type"] == selected_type
    ]


# ============================================================
# PAGE : VUE D'ENSEMBLE
# ============================================================

if page == "Vue d'ensemble":

    st.title("Content Analytics")

    st.markdown(
        "### Vue d'ensemble du catalogue"
    )

    st.divider()

    total = len(filtered_df)

    movies = len(
        filtered_df[filtered_df["type"] == "Movie"]
    )

    tv_shows = len(
        filtered_df[filtered_df["type"] == "TV Show"]
    )

    countries = (
        filtered_df["country"]
        .replace("Unknown", pd.NA)
        .dropna()
        .str.split(", ")
        .explode()
        .nunique()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Contenus",
        f"{total:,}".replace(",", " ")
    )

    col2.metric(
        "Films",
        f"{movies:,}".replace(",", " ")
    )

    col3.metric(
        "Séries",
        f"{tv_shows:,}".replace(",", " ")
    )

    col4.metric(
        "Pays",
        f"{countries:,}".replace(",", " ")
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Répartition des contenus")

        type_counts = filtered_df["type"].value_counts()

        fig, ax = plt.subplots()

        ax.pie(
            type_counts.values,
            labels=type_counts.index,
            autopct="%1.1f%%"
        )

        ax.set_title("Films et séries")

        st.pyplot(fig)

        plt.close(fig)

    with col2:

        st.subheader("Evolution du catalogue")

        yearly = (
            filtered_df["release_year"]
            .value_counts()
            .sort_index()
        )

        fig, ax = plt.subplots()

        ax.plot(
            yearly.index,
            yearly.values
        )

        ax.set_xlabel("Année")
        ax.set_ylabel("Nombre de contenus")

        st.pyplot(fig)

        plt.close(fig)

    st.divider()

    st.subheader("Résumé")

    st.write(
        f"Le catalogue contient actuellement "
        f"**{total:,} contenus**.".replace(",", " ")
    )

    st.write(
        f"Il comprend **{movies:,} films** et "
        f"**{tv_shows:,} séries**.".replace(",", " ")
    )


# ============================================================
# PAGE : CONTENUS
# ============================================================

elif page == "Contenus":

    st.title("Analyse des contenus")

    st.markdown(
        "Analyse de la répartition et de l'évolution des contenus."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Répartition par type")

        type_counts = filtered_df["type"].value_counts()

        st.bar_chart(type_counts)

    with col2:

        st.subheader("Années de sortie")

        yearly = (
            filtered_df["release_year"]
            .value_counts()
            .sort_index()
        )

        st.line_chart(yearly)

    st.divider()

    st.subheader("Contenus les plus récents")

    recent = filtered_df.sort_values(
        "release_year",
        ascending=False
    )

    columns = [
        "title",
        "type",
        "release_year",
        "rating"
    ]

    available_columns = [
        column
        for column in columns
        if column in recent.columns
    ]

    st.dataframe(
        recent[available_columns].head(20),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE : CATEGORIES
# ============================================================

elif page == "Catégories":

    st.title("Analyse des catégories")

    st.markdown(
        "Les catégories représentent les différents types de contenus associés au catalogue."
    )

    st.divider()

    categories = (
        filtered_df["listed_in"]
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
    )

    top_n = st.slider(
        "Nombre de catégories à afficher",
        min_value=5,
        max_value=20,
        value=10
    )

    top_categories = categories.head(top_n)

    fig, ax = plt.subplots(figsize=(10, 6))

    top_categories.sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Nombre de contenus")
    ax.set_ylabel("Catégorie")
    ax.set_title("Catégories les plus représentées")

    st.pyplot(fig)

    plt.close(fig)

    st.divider()

    st.subheader("Top catégories")

    st.dataframe(
        top_categories.rename("Nombre de contenus"),
        use_container_width=True
    )


# ============================================================
# PAGE : PAYS
# ============================================================

elif page == "Pays":

    st.title("Analyse géographique")

    st.markdown(
        "Analyse des pays associés aux contenus."
    )

    st.divider()

    countries = (
        filtered_df["country"]
        .replace("Unknown", pd.NA)
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
    )

    top_n = st.slider(
        "Nombre de pays à afficher",
        min_value=5,
        max_value=20,
        value=10
    )

    top_countries = countries.head(top_n)

    fig, ax = plt.subplots(figsize=(10, 6))

    top_countries.sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Nombre de contenus")
    ax.set_ylabel("Pays")
    ax.set_title("Pays les plus représentés")

    st.pyplot(fig)

    plt.close(fig)

    st.divider()

    st.subheader("Top pays")

    st.dataframe(
        top_countries.rename("Nombre de contenus"),
        use_container_width=True
    )


# ============================================================
# PAGE : CLASSIFICATIONS
# ============================================================

elif page == "Classifications":

    st.title("Analyse des classifications")

    st.markdown(
        "Répartition des classifications présentes dans le catalogue."
    )

    st.divider()

    ratings = (
        filtered_df["rating"]
        .dropna()
        .value_counts()
    )

    top_n = st.slider(
        "Nombre de classifications à afficher",
        min_value=5,
        max_value=15,
        value=10
    )

    ratings = ratings.head(top_n)

    st.bar_chart(ratings)

    st.divider()

    st.subheader("Répartition")

    st.dataframe(
        ratings.rename("Nombre de contenus"),
        use_container_width=True
    )


# ============================================================
# PAGE : DUREES
# ============================================================

elif page == "Durées":

    st.title("Analyse des durées")

    st.markdown(
        "Analyse de la durée des films présents dans le catalogue."
    )

    st.divider()

    movies_df = filtered_df[
        filtered_df["type"] == "Movie"
    ].copy()

    duration = (
        movies_df["duration"]
        .astype("string")
        .str.extract(r"(\d+)", expand=False)
    )

    movies_df["duration_minutes"] = pd.to_numeric(
        duration,
        errors="coerce"
    )

    valid_durations = movies_df[
        movies_df["duration_minutes"].notna()
    ]

    if len(valid_durations) > 0:

        average_duration = (
            valid_durations["duration_minutes"]
            .mean()
        )

        median_duration = (
            valid_durations["duration_minutes"]
            .median()
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Durée moyenne",
            f"{average_duration:.1f} min"
        )

        col2.metric(
            "Durée médiane",
            f"{median_duration:.1f} min"
        )

        st.divider()

        st.subheader("Distribution des durées")

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.hist(
            valid_durations["duration_minutes"],
            bins=30
        )

        ax.set_xlabel("Durée en minutes")
        ax.set_ylabel("Nombre de films")
        ax.set_title("Distribution des durées")

        st.pyplot(fig)

        plt.close(fig)

    else:

        st.warning(
            "Aucune donnée de durée exploitable."
        )


# ============================================================
# PAGE : INSIGHTS
# ============================================================

elif page == "Insights":

    st.title("Insights")

    st.markdown(
        "Principales observations issues de l'analyse du catalogue."
    )

    st.divider()

    total = len(filtered_df)

    movies = len(
        filtered_df[filtered_df["type"] == "Movie"]
    )

    tv_shows = len(
        filtered_df[filtered_df["type"] == "TV Show"]
    )

    if total > 0:

        movie_percentage = (
            movies / total * 100
        )

        tv_percentage = (
            tv_shows / total * 100
        )

        st.markdown(
            f"""
            <div class="insight-box">
                <strong>Répartition des contenus</strong><br>
                Les films représentent environ
                {movie_percentage:.1f}% du catalogue,
                contre {tv_percentage:.1f}% pour les séries.
            </div>
            """,
            unsafe_allow_html=True
        )

        categories = (
            filtered_df["listed_in"]
            .dropna()
            .str.split(", ")
            .explode()
            .value_counts()
        )

        if len(categories) > 0:

            top_category = categories.index[0]
            top_category_count = categories.iloc[0]

            st.markdown(
                f"""
                <div class="insight-box">
                    <strong>Catégorie dominante</strong><br>
                    La catégorie la plus représentée est
                    <strong>{top_category}</strong>,
                    avec {top_category_count:,} contenus.
                </div>
                """.replace(",", " "),
                unsafe_allow_html=True
            )

        countries = (
            filtered_df["country"]
            .replace("Unknown", pd.NA)
            .dropna()
            .str.split(", ")
            .explode()
            .value_counts()
        )

        if len(countries) > 0:

            top_country = countries.index[0]
            top_country_count = countries.iloc[0]

            st.markdown(
                f"""
                <div class="insight-box">
                    <strong>Pays le plus représenté</strong><br>
                    {top_country} est le pays le plus représenté
                    avec {top_country_count:,} contenus.
                </div>
                """.replace(",", " "),
                unsafe_allow_html=True
            )

        st.markdown(
            """
            <div class="insight-box">
                <strong>Diversité du catalogue</strong><br>
                Le catalogue présente une forte diversité
                de catégories et de pays associés aux contenus.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "Projet Data Analysis - Content Analytics"
)
