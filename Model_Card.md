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
