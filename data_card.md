# Data Card - Dataset RH

## Informations générales

| | |
|---|---|
| **Source** | [Kaggle — Human Resources Data Set](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set) |
| **Auteurs** | Dr. Rich Huebner et Dr. Carla Patalano |
| **Type** | Données synthétiques,  créées à des fins pédagogiques |
| **Taille initiale** | 311 lignes × 36 colonnes |
| **Variable cible** | `Termd` - 0 = employé actif, 1 = parti |
| **Répartition des classes** | 207 employés actifs (67%) / 104 partis (33%) |

## Attributs sensibles - supprimés pour conformité légale

Conformément au droit europééen (GDPR article 9 + AI Act EU), les colonnes suivantes ont été supprimées avant l’entraînement du modèle, car leur utilisation dans des décisions liées à l’emploi est illégale.

| Colonne |  Raison de la suppression |
|---|---|
| `GenderID` / `Sex` | La discrimination basée sur le genre est illégale |
| `RaceDesc_*` | La discrimination raciale est illégale |
| `HispanicLatino` | La discrimination liée à l’origine ethnique est illégale  |
| `CitizenDesc_*` | La discrimination liée à la nationalité est illégale |

---

## Colonnes supprimées - fuite de données (data leakage)

Ces colonnes ont été supprimées car elles révèlent directement la réponse (Termd) et permettraient au modèle de "tricher" :

| Colonne |Pourquoi c'est une fuite de données |
|---|---|
| `DateofTermination` | Existe uniquement si l’employé a quitté → révèle directement Termd = 1 |
| `TermReason` | La raison du départ → existe uniquement si Termd = 1 |
| `EmploymentStatus` | "Voluntarily Terminated" → révèle directement le résultat |
| `EmpStatusID` | Version numérique de EmploymentStatus |

---

## Colonnes supprimées - identifiants (RGPD)

Les identifiants personnels ont été supprimés afin d’anonymiser le dataset :

| Colonne | Raison |
|---|---|
| `Employee_Name` | Identifiant personnel direct |
| `EmpID` | Identifiant personnel direct |
| `ManagerName` | Identifiant personnel direct |
| `Zip` | Localisation du domicile |
| `State` | Localisation du domicile |

---

## Colonnes supprimées - redondance

Colonnes textuelles dupliquant des colonnes numériques déjà présentes dans le dataset :

| Colonne supprimée | Remplacée par |
|---|---|
| `Position` | `PositionID` |
| `MaritalDesc` | `MaritalStatusID` |
| `Sex` | `GenderID` |
| `PerformanceScore` | `PerfScoreID` |

---

## Feature engineering

| Transformation | Détail |
|---|---|
| **Âge calculé à partir de la date de naissance (DOB)** | `Age = (aujourd’hui - DOB).days / 365.25` |
| **HispanicLatino encoded** | `"yes" → 1`, `"no" → 0` |
| **One-Hot Encoding** | Appliqué à `CitizenDesc`, `RaceDesc`, `RecruitmentSource` avec `pd.get_dummies(drop_first=True)` |
| **DateofHire removed** | Une fois les variables liées à l’ancienneté calculées, cette colonne n’est plus nécessaire |
| **LastPerformanceReview_Date removed** | La date en elle-même n’est pas utile ; PerfScoreID montre déjà l’information de performance |

---

## Statistiques clés

| Variable | Moyenne | Min | Max | Notes |
|---|---|---|---|---|
| Salary | ~69k USD | 45k | 250k | Distribution asymétrique (queue à droite) |
| EngagementSurvey | 4.1 | 1.12 | 5.0 | Plus élevé = plus engagé |
| EmpSatisfaction | 3.9 | 1 | 5 | Plus élevé = plus satisfait |
| Absences | 10.2 | 1 | 20 | Par an |
| DaysLateLast30 | 0.4 | 0 | 14 | Globalement faible |
| Age | 44 | 27 | 71 | Distribution normale |

---

## Limites connues

- **Dataset synthétique** : les distributions peuvent ne pas refléter la réalité d’une entreprise
- **Contexte américain** : certaines variables (CitizenDesc, State) sont spécifiques aux États-Unis
- **Taille réduite** : 311 lignes est très faible pour du machine learning, les modèles peuvent être instables (forte variance)
- **Données issues d’une seule entreprise** : sans historique dans le temps ni possibilité de comparaison avec d’autres entreprises
---
