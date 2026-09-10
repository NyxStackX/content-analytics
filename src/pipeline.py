import pandas as pd

RAW_FILE = "data/raw/netflix_titles.csv"
PROCESSED_FILE = "data/processed/netflix_titles_clean.csv"


def load_data(path=RAW_FILE):
    """Charge le dataset brut."""
    return pd.read_csv(path)


def clean_data(df):
    """Nettoie et standardise les données."""
    df = df.copy()

    # Nettoyage des espaces dans les colonnes texte
    text_columns = df.select_dtypes(include="object").columns

    for column in text_columns:
        df[column] = df[column].str.strip()

    # Conversion de la date d'ajout
    df["date_added"] = pd.to_datetime(
        df["date_added"],
        errors="coerce"
    )

    # Valeurs manquantes explicites
    for column in ["director", "cast", "country"]:
        df[column] = df[column].fillna("Unknown")

    return df


def validate_data(df):
    """Effectue les contrôles principaux sur le dataset."""
    checks = {
        "Nombre de lignes": len(df),
        "Nombre de colonnes": len(df.columns),
        "Doublons": df.duplicated().sum(),
        "Dates invalides": df["date_added"].isna().sum(),
    }

    return checks


def save_data(df, path=PROCESSED_FILE):
    """Sauvegarde le dataset nettoyé."""
    df.to_csv(path, index=False)


def main():
    print("=== Content Analytics Pipeline ===")

    print("\n[1/4] Chargement des données...")
    df = load_data()

    print(f"Dataset initial : {df.shape[0]} lignes, {df.shape[1]} colonnes")

    print("\n[2/4] Nettoyage...")
    df_clean = clean_data(df)

    print("\n[3/4] Validation...")
    checks = validate_data(df_clean)

    for key, value in checks.items():
        print(f"{key} : {value}")

    print("\n[4/4] Sauvegarde...")
    save_data(df_clean)

    print(f"Dataset sauvegardé : {PROCESSED_FILE}")
    print("\nPipeline terminé avec succès.")


if __name__ == "__main__":
    main()
