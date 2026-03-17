# MODEL CARD : Modèle de prédiction de turnover des employés

---

## 1. Objectif du modèle

### Cas d’usage visé
Prédiction des employés susceptibles de démissionner et identification des facteurs corrélés aux départs pour aider à la prise de décision RH.

### Entrées
Tableau structuré de variables décrivant les employés :
- Données démographiques  
- Performance  
- Satisfaction  
- Engagement  
- Historique RH  

### Sorties
- Variable binaire :
  - 1 = Employé susceptible de démissionner  
  - 0 = Employé susceptible de rester  
- Scores de probabilité  
- Explications locales (via SHAP)

---

## 2. Données d’entraînement

### Dataset utilisé
Human Resources dataset – Dr Rich Huebner, Dr Carla Patalano

### Taille / diversité

- Nombre total d’échantillons : **311**

#### Répartition des classes
- Démission (Termd = 1) : ~30 %  
- Pas de démission (Termd = 0) : ~70 %

#### Diversité
- Âge : distribution large (20 à 60 ans)  
- Genre : représenté (GenderID)  
- Origine ethnique : RaceDesc_*  
- Postes : DeptID, PositionID  

#### Autres facteurs
- Satisfaction (EmpSatisfaction)  
- Engagement (EngagementSurvey)  
- Performance (PerfScoreID)  
- Absences et retards  
- Salaire  

### Limites connues
- Surreprésentation de certaines populations  
- Déséquilibre des classes  
- Variables sensibles présentes (non utilisées directement)  
- Taille faible du dataset → risque de surapprentissage  

---

## 3. Performances

### Métriques utilisées
- Accuracy  
- Precision  
- Recall  
- F1-score  
- ROC-AUC  
- SHAP  
- Métriques d’équité (AIF360)  

---

### Modèle baseline

#### Validation croisée (5-fold)
- Accuracy : **0.637 ± 0.059**  
- F1-score : **0.534 ± 0.071**

#### Test set
- Accuracy : **0.68**

| Classe          | Precision | Recall | F1-score |
|-----------------|----------|--------|----------|
| Active (0)      | 0.81     | 0.69   | 0.74     |
| Terminated (1)  | 0.52     | 0.67   | 0.58     |

**Observation :**
- Bon rappel sur les démissions  
- Precision faible → faux positifs  

---

### Modèle XGBoost (optimisé)

#### Hyperparamètres
max_depth=3

learning_rate=0.1

n_estimators=100

gamma=0.3

colsample_bytree=0.6

subsample=1.0


#### Validation
- AUC CV : **0.657**

#### Test set
- Accuracy : **0.70**  
- ROC-AUC : **0.684**

| Classe          | Precision | Recall | F1-score |
|-----------------|----------|--------|----------|
| Active (0)      | 0.77     | 0.79   | 0.78     |
| Terminated (1)  | 0.55     | 0.52   | 0.54     |

#### Overfitting
- Train AUC : **0.996**  
- Test AUC : **0.684**  
- Gap : **0.312 → surapprentissage important**

---

### Modèle final (Random Forest)

#### Test set
- Accuracy : **0.76**  
- ROC-AUC : **0.782**

| Classe          | Precision | Recall | F1-score |
|-----------------|----------|--------|----------|
| Active (0)      | 0.80     | 0.86   | 0.83     |
| Terminated (1)  | 0.67     | 0.57   | 0.62     |

#### Overfitting
- Train AUC : **0.801**  
- Test AUC : **0.782**  
- Gap : **0.018 → très bon équilibre**

---

### Interprétabilité (SHAP)

- SHAP utilisé pour expliquer les prédictions individuelles  

#### Exemple
- Probabilité prédite : **0.460 → Active**  
- Base value : **0.4977**

#### Variables influentes
- Sources de recrutement (Website, Referral, LinkedIn…)  
- Retards récents (DaysLateLast30)  
- Salaire  
- Nombre de projets  
- Statut marital  

---

### Analyse d’équité

- Déséquilibres observés selon certains groupes  
- Indices de biais potentiels (AIF360) :
  - Différences de taux de prédiction  
  - Impact de variables corrélées  

**Observation :**  
Le modèle présente des variations de performance selon certains groupes, nécessitant une vigilance avant déploiement.

---

## 4. Limites

### Risques d’erreur
- Mauvaise détection des cas rares  
- Sensibilité aux données bruitées  
- Risque de surapprentissage  

### Situations non couvertes
- Données hors distribution  
- Changements organisationnels majeurs  
- Facteurs externes non modélisés  

### Risques de biais
- Déséquilibre des classes  
- Variables corrélées à des attributs sensibles  
- Sous-représentation de certaines populations  
- Biais historiques RH  

### Limites projet
- Projet exploratoire (2 jours) :
  - Optimisation limitée  
  - Peu de validation externe  
  - Robustesse limitée  

- Dataset non européen → transférabilité limitée vers l’UE  

---

## 5. Risques & mitigation

### Risques de mauvaise utilisation
- Surinterprétation des prédictions  
- Décisions automatisées critiques  
- Discrimination indirecte  

### Contrôles mis en place
- SHAP pour explicabilité  
- Analyse de biais (AIF360)  
- Validation humaine recommandée  
- Seuils ajustables  
- Documentation des limites  
- Contrôle des variables sensibles  
- Monitoring en production  

### Conformité réglementaire
Le modèle est considéré comme **à haut risque** selon l’AI Act (emploi).

Exigences :
- Supervision humaine  
- Transparence  
- Documentation des biais  
- Audit régulier  

---

## 6. Énergie et frugalité

- Poids du modèle : **340 kB**  
- Temps d’inférence : **78 μs (CPU)**  
- Énergie estimée : **6,0 × 10⁻⁵ kWh/CO₂**

---

## 7. Cyber

- Sécurisation des entrées : Vérification d’âge  
- Secrets protégés : Non


