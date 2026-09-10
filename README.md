
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
├── dashboard/
│   └── app.py
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
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── pipeline.py
│   └── generate_results.py
├── tests/
│   └── test_pipeline.py
├── results/
│   ├── figures/
│   └── summary/
├── requirements.txt
├── .gitignore
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
7. Génération automatisée des résultats

Les analyses sont réalisées principalement avec Python et les bibliothèques spécialisées en data science.

## Technologies

- Streamlit

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook
- Pytest
- Streamlit

## Dashboard interactif

Le projet comprend un dashboard développé avec **Streamlit** afin de rendre les analyses accessibles de manière interactive. Il propose des vues dédiées aux contenus, catégories, pays, classifications, durées et insights, ainsi qu’un filtre global par type de contenu.

Pour lancer le dashboard :

```sh
streamlit run dashboard/app.py
```

## Résultats principaux

L'analyse porte sur **8 807 contenus**.

| Indicateur | Résultat |
|---|---:|
| Contenus analysés | 8 807 |
| Films | 6 131 |
| Séries | 2 676 |
| Catégories uniques | 42 |
| Pays associés | 127 |
| Durée moyenne des films | 99,56 min |

Les films représentent environ **69,6 %** du catalogue, contre **30,4 %** pour les séries.

L'analyse met également en évidence une forte diversité des catégories et des pays associés aux contenus.

## Automatisation

Le projet dispose d'un pipeline permettant de reproduire le nettoyage, la validation et la génération des résultats.

### Nettoyage et validation

```sh
python src/pipeline.py
```

### Génération des résultats

```sh
python src/generate_results.py
```

### Tests

```sh
python -m pytest tests/
```

## Résultats générés

Les résultats automatisés sont disponibles dans :

```text
results/
├── figures/
│   ├── content_distribution.png
│   ├── release_years.png
│   ├── top_categories.png
│   ├── top_countries.png
│   └── ratings.png
└── summary/
    └── summary.csv
```

## Dataset

Le projet utilise un dataset public contenant des informations sur des films et séries : type de contenu, titre, réalisateur, distribution, pays, date d'ajout, année de sortie, classification, durée, catégories et description.

Les données brutes ne sont pas versionnées dans Git afin de conserver un dépôt léger.

## Qualité des données

Plusieurs contrôles ont été intégrés au projet :

- détection des doublons
- contrôle des valeurs manquantes
- conversion des dates
- validation des classifications
- détection des valeurs anormales
- tests automatisés du pipeline

Une anomalie présente dans le dataset original concernait trois durées de films enregistrées dans la colonne `rating` (`66 min`, `74 min` et `84 min`). Ces valeurs sont automatiquement corrigées par le pipeline.

## Limites

- Le dataset représente un catalogue et ne permet pas de mesurer directement l'audience ou la popularité réelle des contenus.
- Un contenu peut être associé à plusieurs pays ou catégories.
- Certaines informations sont manquantes dans les données originales.
- Les résultats dépendent du dataset utilisé et de sa structure.

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

Projet personnel réalisé dans le cadre de mon apprentissage.

