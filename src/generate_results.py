import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


INPUT_FILE = "data/processed/netflix_titles_clean.csv"
FIGURES_DIR = "results/figures"
SUMMARY_DIR = "results/summary"


def load_data():
    df = pd.read_csv(INPUT_FILE)
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    return df


def generate_content_distribution(df):
    counts = df["type"].value_counts()

    plt.figure(figsize=(8, 5))
    sns.barplot(x=counts.index, y=counts.values)
    plt.title("Content Distribution")
    plt.xlabel("Content Type")
    plt.ylabel("Number of Titles")
    plt.tight_layout()
    plt.savefig(
        f"{FIGURES_DIR}/content_distribution.png",
        dpi=150
    )
    plt.close()


def generate_release_years(df):
    counts = df["release_year"].value_counts().sort_index()

    plt.figure(figsize=(12, 5))
    plt.plot(counts.index, counts.values)
    plt.title("Content by Release Year")
    plt.xlabel("Release Year")
    plt.ylabel("Number of Titles")
    plt.tight_layout()
    plt.savefig(
        f"{FIGURES_DIR}/release_years.png",
        dpi=150
    )
    plt.close()


def generate_top_categories(df):
    categories = (
        df["listed_in"]
        .dropna()
        .str.split(", ")
        .explode()
    )

    counts = categories.value_counts().head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=counts.values, y=counts.index)
    plt.title("Top 10 Categories")
    plt.xlabel("Number of Titles")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(
        f"{FIGURES_DIR}/top_categories.png",
        dpi=150
    )
    plt.close()


def generate_top_countries(df):
    countries = (
        df["country"]
        .replace("Unknown", pd.NA)
        .dropna()
        .str.split(", ")
        .explode()
    )

    counts = countries.value_counts().head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=counts.values, y=counts.index)
    plt.title("Top 10 Countries")
    plt.xlabel("Number of Associated Titles")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.savefig(
        f"{FIGURES_DIR}/top_countries.png",
        dpi=150
    )
    plt.close()


def generate_ratings(df):
    counts = df["rating"].dropna().value_counts().head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=counts.values, y=counts.index)
    plt.title("Top Content Ratings")
    plt.xlabel("Number of Titles")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.savefig(
        f"{FIGURES_DIR}/ratings.png",
        dpi=150
    )
    plt.close()


def generate_summary(df):
    movies = df[df["type"] == "Movie"].copy()

    movies["duration_minutes"] = pd.to_numeric(
        movies["duration"].str.extract(r"(\d+)")[0],
        errors="coerce"
    )

    categories = (
        df["listed_in"]
        .dropna()
        .str.split(", ")
        .explode()
    )

    countries = (
        df["country"]
        .replace("Unknown", pd.NA)
        .dropna()
        .str.split(", ")
        .explode()
    )

    summary = pd.DataFrame({
        "Metric": [
            "Total titles",
            "Movies",
            "TV Shows",
            "Unique categories",
            "Unique countries",
            "Average movie duration (minutes)"
        ],
        "Value": [
            len(df),
            (df["type"] == "Movie").sum(),
            (df["type"] == "TV Show").sum(),
            categories.nunique(),
            countries.nunique(),
            round(movies["duration_minutes"].mean(), 2)
        ]
    })

    summary.to_csv(
        f"{SUMMARY_DIR}/summary.csv",
        index=False
    )


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(SUMMARY_DIR, exist_ok=True)

    print("=== Results Generation ===")

    df = load_data()

    print("[1/6] Content distribution...")
    generate_content_distribution(df)

    print("[2/6] Release years...")
    generate_release_years(df)

    print("[3/6] Categories...")
    generate_top_categories(df)

    print("[4/6] Countries...")
    generate_top_countries(df)

    print("[5/6] Ratings...")
    generate_ratings(df)

    print("[6/6] Summary...")
    generate_summary(df)

    print("\nResults generated successfully.")


if __name__ == "__main__":
    main()
