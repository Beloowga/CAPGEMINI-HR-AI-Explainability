# Data Card - Dataset RH

## Présentation du dataset

| | |
|---|---|
| **Source** | [Kaggle — Human Resources Data Set](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set) |
| **Auteurs** | Dr. Rich Huebner et Dr. Carla Patalano |
| **Type** | Synthétique, créé pour un but pédagogique |
| **Taille originelle** | 311 lignes × 36 colonnes |
| **Après nettoyage** | 311 lignes × 22 attributs + 1 variable cible |
| **Variable cible** | `Termd` - 0 = employé actif, 1 = employé ayant quitté l'enterprise |
| **Répartition des classes** | 207 employés actifs (67%) / 104 employés ayant quitté l’entreprise (33%) |

## Attributs sensibles - supprimés pour conformité légale

Sous la loi européenne (GDPR article 9 + AI Act EU), les colonnes suivantes ont été supprimées avant l'entraînelent car les utiliser afin de prendre des décisions concernant les recrutements/licenciement est illégal.

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
