# MODEL CARD : Modèle de prédiction de turnover des employés

---

## 1. Objectif du modèle

### Cas d’usage visé
Prédiction des employés susceptibles de démissionner et identification des facteurs corrélés aux départs pour aider à la prise de décision RH.

Les relations identifiées sont **corrélationnelles et non causales**. Le modèle ne permet pas d’expliquer les causes réelles des départs.

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
- Dataset non européen → transférabilité limitée vers l’UE  

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

### Modèle baseline (Logistic Regression)

#### Validation croisée (5-fold)
- Accuracy : **0.657 ± 0.044**  
- F1-score : **0.554 ± 0.049**

#### Test set
- Accuracy : **0.65**

| Classe          | Precision | Recall | F1-score |
|-----------------|----------|--------|----------|
| Active (0)      | 0.79     | 0.64   | 0.71     |
| Terminated (1)  | 0.48     | 0.67   | 0.56     |

**Observation :**
- Bon rappel sur les démissions  
- Precision faible → nombreux faux positifs  

---

### Modèle XGBoost (optimisé)

#### Hyperparamètres optimaux
- subsample = 0.8  
- n_estimators = 400  
- min_child_weight = 3  
- max_depth = 5  
- learning_rate = 0.01  
- gamma = 0  
- colsample_bytree = 0.6  

#### Validation
- AUC CV : **0.651**

#### Test set
- Accuracy : **0.68**  
- ROC-AUC : **0.696**

| Classe          | Precision | Recall | F1-score |
|-----------------|----------|--------|----------|
| Active (0)      | 0.75     | 0.79   | 0.77     |
| Terminated (1)  | 0.53     | 0.48   | 0.50     |

#### Overfitting
- Train AUC : **0.991**  
- Test AUC : **0.696**  
- Gap : **0.295 → surapprentissage important**

---

### Modèle final (Random Forest)

#### Test set
- Accuracy : **0.76**  
- ROC-AUC : **0.778**

| Classe          | Precision | Recall | F1-score |
|-----------------|----------|--------|----------|
| Active (0)      | 0.80     | 0.86   | 0.83     |
| Terminated (1)  | 0.67     | 0.57   | 0.62     |

#### Overfitting
- Train AUC : **0.882**  
- Test AUC : **0.778**  
- Gap : **0.105 → bon compromis biais/variance**

---

### Interprétabilité (SHAP)

- SHAP utilisé pour expliquer les prédictions individuelles  

#### Exemple
- Probabilité prédite : **0.459 → Active**  
- Base value : **0.4977**

#### Variables influentes
- Sources de recrutement  
- ManagerID  
- Statut marital  
- Retards récents (DaysLateLast30)  
- Salaire  
- Nombre de projets  

---

### Analyse d’équité

- Déséquilibres observés selon certains groupes  
- Indices de biais potentiels (AIF360)

**Résultats principaux :**
- Disparate Impact : **0.954 → 1.000 (après mitigation)**  
- Statistical Parity Difference : **-0.032 → 0.000**  
- Equal Opportunity Difference : **-0.034 → -0.145**  
- Average Odds Difference : reste dans les seuils acceptables  

**Observation :**  
L’audit ne met pas en évidence de biais majeur selon l’âge, mais montre des compromis entre métriques de fairness. Une surveillance reste nécessaire.

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
- Supervision humaine obligatoire  
- Transparence des décisions  
- Documentation des biais  
- Audit régulier  

---

## 6. Énergie et frugalité

- Poids du modèle : **690kB**  
- Temps d’inférence : **78 μs (CPU)**  
- Énergie estimée (CodeCarbon) : **9,3 × 10⁻⁵ kWh/CO₂**

---

## 7. Cyber

- Sécurisation des entrées : Vérification d’âge  
- Secrets protégés : Non


