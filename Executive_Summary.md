# Executive Summary

## Prédiction du turnover RH - IA Explicable & IA Éthique

---

## Le problème

Notre client, une entreprise fictive, fait face à un taux de démission élevé et ne comprend pas pourquoi ses employés partent. Les RH ont besoin d'un outil capable de :
1. Anticiper quels employés risquent de quitter l'entreprise
2. Expliquer la raison des départs
3. Garantir que les prédictions sont équitables et non discriminatoires

---

## Notre solution

Nous avons construit un pipeline IA complet de prédiction du turnover, avec deux couches d'IA responsable :

### IA Explicable - SHAP
Nous utilisons SHAP (Shapley Additive explanations) pour rendre chaque prédiction transparente :
- Vue globale : quels facteurs influencent le plus le turnover sur l'ensemble des employés
- Vue individuelle : pour chaque employé à risque, identifier les facteurs qui expliquent la prédiction afin d’aider les RH à agir concrètement

### IA Éthique - AI Fairness 360
Nous auditons le modèle pour détecter tout biais discriminatoire :
- Les attributs sensibles (genre, origine ethnique) sont supprimés du modèle car ils sont illégaux en vertu du RGPD européen (Article 9)
- Nous auditons le biais lié à l'âge, seul attribut sensible légalement auditable dans ce contexte
- Nous appliquons le Reweighing pour corriger les biais détectés
- Nous mesurons l'équité avec quatre métriques standard : Disparate Impact, SPD, EOD, AOD

---

## Résultats clés

| Métrique | Valeur |
|---|---|
| Modèle retenu | Random Forest |
| Précision | 76% |
| ROC-AUC | 78% |
| Biais d'âge détecté (avant mitigation) | DI = 0.954 — faible |
| Biais d'âge après Reweighing | DI = 1.000 — corrigé |

**Top 5 des facteurs de turnover** (d'après SHAP) :
1. Manager
2. Salaire
3. Age
4. Absences
5. Poste

---

## Conformité IA Responsable

| Exigence | Statut |
|---|---|
| RGPD - données sensibles supprimées | Genre, race, ethnie retirés |
| AI Act - transparence | Explications SHAP pour chaque prédiction |
| AI Act - détection des biais | Audit aif360 sur l'âge |
| AI Act - supervision humaine | Outil d'aide à la décision, non autonome |
| Non-discrimination | Reweighing appliqué, métriques vérifiées |

---

## Limites

- Dataset de taille modeste : les performances s'amélioreraient avec plus de données
- L'âge est le seul attribut audité : un audit plus complet nécessiterait des données supplémentaires
- Le modèle doit être ré-entraîné régulièrement pour rester pertinent
- L'EOD se dégrade légèrement après Reweighing (-0.034 → -0.145) : compromis entre métriques de fairness
  
---

*Hackathon Capgemini × ESILV — IA & RH | Mars 2026*
*Équipe : Noé, Othman, Mathis, Isabella, Yasmine*
