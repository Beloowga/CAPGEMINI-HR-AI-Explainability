graph TD
    subgraph Data_Layer [Couche de Données]
        A[Données Brutes Kaggle]
    end
    subgraph Preprocessing [Prétraitement]
        B[Suppression Identifiants RGPD]
        C[Suppression Attributs Sensibles]
        D[Élimination Fuites de Données]
        E[Feature Engineering]
        A --> B --> C --> D --> E
    end
    subgraph Modeling [Modélisation]
        I[Régression Logistique — Baseline]
        K[XGBoost]
        L[Random Forest — Modèle Final]
        M[Évaluation — Accuracy, F1, Recall, ROC-AUC]
        E --> I
        E --> K
        E --> L
        I --> M
        K --> M
        L --> M
    end
    subgraph Fairness_Ethics [Éthique & Équité]
        F[Audit de Biais AIF360]
        G[Mitigation — Reweighing]
        H[Métriques — DI, SPD, EOD, AOD]
        M --> F --> G --> H
    end
    subgraph Explainability [Explicabilité SHAP]
        N[Importance Globale des Variables]
        O[Explications Locales Individuelles]
        M --> N
        M --> O
    end
    subgraph Output [Sortie]
        Q[Prédiction Binaire 0 / 1]
        R[Score de Probabilité]
        S[Rapport RH]
        H --> Q
        H --> R
        N --> S
        O --> S
        Q --> S
        R --> S
    end
