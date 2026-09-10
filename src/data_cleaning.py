import pandas as pd

RAW_FILE = "data/raw/netflix_titles.csv"
PROCESSED_FILE = "data/processed/netflix_titles_clean.csv"


def load_data():
    return pd.read_csv(RAW_FILE)


def clean_data(df):
    df = df.copy()

    # Suppression des espaces inutiles dans les colonnes texte
    text_columns = df.select_dtypes(include="object").columns

    for column in text_columns:
        df[column] = df[column].str.strip()

    # Conversion de la date d'ajout
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

    # Valeurs manquantes : conserver l'information mais les rendre explicites
    missing_columns = ["director", "cast", "country"]

    for column in missing_columns:
        df[column] = df[column].fillna("Unknown")

    return df


def save_data(df):
    df.to_csv(PROCESSED_FILE, index=False)


def main():
    df = load_data()

    print(f"Dataset initial : {df.shape[0]} lignes, {df.shape[1]} colonnes")

    df_clean = clean_data(df)

    save_data(df_clean)

    print(
        f"Dataset nettoyé : "
        f"{df_clean.shape[0]} lignes, {df_clean.shape[1]} colonnes"
    )


if __name__ == "__main__":
    main()