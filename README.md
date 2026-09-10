
# Content Analytics

Projet d'analyse de données consacré à l'étude d'un catalogue de contenus audiovisuels.

L'objectif est d'explorer les caractéristiques des contenus, d'identifier des tendances et de produire des analyses et visualisations permettant de mieux comprendre le catalogue.

## Objectifs

- Explorer et comprendre les données
- Nettoyer et valider le dataset
- Analyser la répartition des contenus
- Étudier les catégories et genres
- Analyser les pays de production
- Étudier les classifications
- Analyser les durées
- Identifier des tendances et corrélations
- Produire des visualisations claires et pertinentes

## Structure du projet

```text
content-analytics/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_cleaning_validation.ipynb
│   ├── 03_content_analysis.ipynb
│   ├── 04_genre_analysis.ipynb
│   ├── 05_country_analysis.ipynb
│   ├── 06_ratings_analysis.ipynb
│   ├── 07_duration_analysis.ipynb
│   ├── 08_cross_analysis.ipynb
│   └── 09_final_insights.ipynb
├── src/
├── tests/
├── requirements.txt
└── README.md
```

## Méthodologie

Le projet suit plusieurs étapes :

1. Exploration des données
2. Nettoyage et validation
3. Analyse exploratoire
4. Analyses thématiques
5. Analyses croisées
6. Synthèse des résultats

Les analyses sont réalisées principalement avec Python et les bibliothèques spécialisées en data science.

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

## Dataset

Le projet utilise un dataset public contenant des informations sur des films et séries : type de contenu, titre, réalisateur, distribution, pays, date d'ajout, année de sortie, classification, durée, catégories et description.

Les données brutes ne sont pas versionnées dans Git afin de conserver un dépôt léger.

## Analyses

Les notebooks sont organisés progressivement afin de séparer les différentes étapes du projet :

- **01 - Exploration générale**
- **02 - Nettoyage et validation**
- **03 - Analyse des contenus**
- **04 - Analyse des genres et catégories**
- **05 - Analyse des pays**
- **06 - Analyse des classifications**
- **07 - Analyse des durées**
- **08 - Analyses croisées**
- **09 - Insights finaux**

## Auteur

Projet personnel réalisé dans le cadre de mon parcours d'apprentissage.
