# A3 — Contrats JSON sous stress

**Cours :** MSMIN5IN52 — IA générative et chatbots  
**Établissement :** EPF École d'ingénieurs  
**Année :** 2026-2027  
**Sujet :** A3 — Contrats JSON sous stress  
**Statut :** Projet finalisé — MVP implémenté, testé et évalué

---

## 1. Présentation

Les modèles de langage peuvent produire des réponses qui ressemblent à du JSON sans respecter complètement le contrat attendu : erreur de syntaxe, champ obligatoire absent, mauvais type, valeur invalide ou incohérence avec les règles métier.

Ce projet étudie la robustesse des sorties JSON générées par un LLM lorsque la complexité du JSON Schema augmente.

L'objectif est de mesurer :

- le taux de conformité au premier essai ;
- l'impact de la complexité du schéma ;
- l'efficacité d'une stratégie de validation et de reprise ;
- le nombre de tentatives nécessaires ;
- la latence ;
- le coût des appels au modèle.

Le projet compare deux stratégies :

- **baseline** : une seule génération, sans nouvelle tentative ;
- **retry** : validation de la réponse et nouvelle génération en cas d'erreur, avec feedback transmis au modèle.

---

## 2. Fonctionnalités

Le projet fournit :

- cinq JSON Schemas de difficulté croissante ;
- un validateur syntaxique et structurel ;
- un générateur simulé pour les tests hors ligne ;
- un générateur réel utilisant OpenRouter ;
- une stratégie de reprise avec feedback des erreurs ;
- une limite configurable du nombre de tentatives ;
- une gestion des limites de coût et de latence ;
- une interface en ligne de commande ;
- une campagne expérimentale baseline / retry ;
- l'enregistrement des résultats au format JSONL ;
- le calcul automatique des métriques ;
- la génération de tableaux CSV ;
- la génération de graphiques PNG ;
- un rapport Markdown ;
- des tests automatisés exécutables sans clé API ;
- un support de démonstration et de soutenance.

Le flux principal est le suivant :

```text
JSON Schema
    ↓
Génération
    ↓
Parsing JSON
    ↓
Validation
    ↓
Reprise éventuelle
    ↓
Enregistrement
    ↓
Évaluation
    ↓
Rapport
```

---

## 3. Architecture

```text
groupe-json-stress/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
├── results/
│   ├── experiment_final.jsonl
│   ├── experiment_summary.csv
│   ├── paired_results.csv
│   └── mock_results.jsonl
│
├── src/
│   ├── validator.py
│   │
│   ├── schemas/
│   │   ├── schema_01.json
│   │   ├── schema_02.json
│   │   ├── schema_03.json
│   │   ├── schema_04.json
│   │   └── schema_05.json
│   │
│   └── json_stress/
│       ├── __init__.py
│       ├── cli.py
│       ├── evaluation.py
│       ├── experiment.py
│       ├── generator.py
│       ├── openrouter_generator.py
│       ├── report.py
│       └── retry.py
│
└── tests/
    ├── test_cli.py
    ├── test_evaluation.py
    ├── test_report.py
    ├── test_retry.py
    └── test_validator.py
```

L'architecture sépare volontairement :

- la définition des contrats JSON ;
- la génération ;
- la validation ;
- la stratégie de reprise ;
- l'exécution des expériences ;
- l'analyse statistique ;
- la génération des rapports.

Cette séparation permet de tester chaque composant indépendamment et de remplacer le fournisseur de modèle sans modifier toute l'application.

---

## 4. JSON Schemas

Cinq schémas sont utilisés afin d'augmenter progressivement la difficulté.

### Schema 01

Objet simple comportant des types et des champs obligatoires.

### Schema 02

Ajout d'objets imbriqués et de tableaux.

### Schema 03

Ajout de contraintes plus fortes, d'énumérations et de règles conditionnelles.

### Schema 04

Structures imbriquées plus complexes et contraintes sur les éléments.

### Schema 05

Contraintes croisées et règles de cohérence supplémentaires.

Les fichiers se trouvent dans :

```text
src/schemas/
```

---

## 5. Validation

Le validateur est défini dans :

```text
src/validator.py
```

La validation comporte deux étapes principales :

1. vérifier que la sortie peut être interprétée comme du JSON ;
2. vérifier que les données respectent le JSON Schema demandé.

La bibliothèque `jsonschema` est utilisée pour vérifier les contraintes structurelles.

Lorsqu'une validation échoue, les erreurs sont conservées afin de pouvoir :

- identifier le type d'échec ;
- enregistrer les erreurs dans les résultats ;
- fournir un feedback lors d'une nouvelle tentative.

---

## 6. Générateurs

### 6.1. MockGenerator

Le `MockGenerator` permet d'utiliser le projet sans connexion réseau ni clé API.

Il est principalement utilisé pour :

- les tests automatisés ;
- les démonstrations reproductibles ;
- les scénarios d'erreur ;
- la validation de la stratégie de reprise.

Il fournit également un plan B en cas d'indisponibilité du service externe.

### 6.2. OpenRouter

Les expériences réelles utilisent un générateur compatible avec l'API OpenAI via OpenRouter.

Configuration utilisée pour la campagne finale :

```text
Provider    : OpenRouter
Model       : qwen/qwen3.5-9b
Temperature : 0.2
Max tokens  : 4096
```

Le système collecte également, lorsque les informations sont disponibles :

- les prompt tokens ;
- les completion tokens ;
- le coût ;
- le statut du coût.

Le coût peut être :

- fourni directement par l'API ;
- estimé à partir du nombre de tokens ;
- marqué comme inconnu lorsqu'aucune information fiable n'est disponible.

---

## 7. Stratégie de reprise

La logique de reprise est implémentée dans :

```text
src/json_stress/retry.py
```

Le fonctionnement général est :

```text
Génération
    ↓
Parsing
    ↓
Validation
    ↓
Valide ?
   /     \
 Oui     Non
  ↓       ↓
Succès   Analyse des erreurs
          ↓
        Feedback
          ↓
   Nouvelle tentative
```

Le système prend en charge :

- les erreurs de génération ;
- les erreurs de parsing JSON ;
- les erreurs de validation ;
- les réponses tronquées ;
- un nombre maximal de tentatives ;
- une limite optionnelle de coût ;
- une limite optionnelle de latence ;
- l'historique complet des tentatives.

Pour la campagne expérimentale finale :

```text
baseline : 1 tentative maximum
retry    : 3 tentatives maximum
```

---

## 8. Installation

### Prérequis

- Python 3.11 ou version compatible ;
- Git ;
- une connexion Internet pour les expériences réelles ;
- une clé OpenRouter uniquement pour lancer de nouvelles générations réelles.

### Cloner le dépôt

```bash
git clone https://github.com/TONGTONG0113/2026-MSMIN5IN52-GenAI.git
cd 2026-MSMIN5IN52-GenAI
git switch feature/json-stress
cd groupe-json-stress
```

### Environnement virtuel

Linux / macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell :

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

Les principales bibliothèques utilisées sont :

```text
pandas
matplotlib
pytest
tabulate
jsonschema
openai
python-dotenv
```

---

## 9. Configuration de l'API

Copier le fichier d'exemple :

Linux / macOS :

```bash
cp .env.example .env
```

Windows PowerShell :

```powershell
Copy-Item .env.example .env
```

Puis renseigner la clé localement :

```env
MODEL_API_KEY=your_api_key
MODEL_BASE_URL=https://openrouter.ai/api/v1
```

Les valeurs sensibles ne doivent jamais être ajoutées au dépôt.

Le fichier `.env` est ignoré par Git.

---

## 10. Utilisation

Le projet utilise une organisation Python basée sur le dossier `src`.

Avant les commandes suivantes, définir le `PYTHONPATH`.

### Windows PowerShell

```powershell
$env:PYTHONPATH="src"
```

### Linux / macOS

```bash
export PYTHONPATH=src
```

---

## 11. CLI

Trois commandes principales sont proposées :

```text
generate
evaluate
report
```

### 11.1. Génération simulée

```bash
python -m json_stress.cli generate --schema schema_01.json
```

Exemple avec trois tentatives maximum :

```bash
python -m json_stress.cli generate --schema schema_03.json --max-attempts 3
```

Cette commande utilise le `MockGenerator` et ne nécessite pas de clé API.

Le résultat est enregistré par défaut dans :

```text
results/generated_results.jsonl
```

### 11.2. Évaluation

Pour analyser les résultats de la campagne finale :

```bash
python -m json_stress.cli evaluate results/experiment_final.jsonl
```

La commande affiche notamment :

- le nombre de générations ;
- le taux de conformité initial ;
- le taux de conformité final ;
- le taux d'échec final ;
- le nombre moyen de tentatives ;
- la latence moyenne ;
- le coût total ;
- le coût moyen ;
- les résultats par schéma ;
- les résultats par stratégie.

### 11.3. Rapport

```bash
python -m json_stress.cli report results/experiment_final.jsonl --output-dir results/report
```

Le programme génère :

```text
results/report/
├── compliance_by_schema.png
├── cost_by_strategy.png
├── latency_by_schema.png
├── metrics_by_schema.csv
├── metrics_by_schema_strategy.csv
├── metrics_by_strategy.csv
├── report.md
└── strategy_comparison.png
```

Les fichiers de résultats UTF-8 classiques et les fichiers UTF-8 contenant un BOM sont pris en charge.

---

## 12. Expériences OpenRouter

Avant une campagne complète, la connexion au modèle peut être vérifiée avec :

```bash
python -m json_stress.experiment --check-only
```

Exemple de campagne :

```bash
python -m json_stress.experiment --runs-per-schema 40 --max-attempts 3 --output results/openrouter_experiment.jsonl
```

La campagne finale utilise :

```bash
python -m json_stress.experiment --runs-per-schema 200 --max-attempts 3 --output results/experiment_final.jsonl
```

Pour chaque schéma :

```text
200 échantillons
× 2 stratégies
= 400 résultats
```

Pour l'ensemble des cinq schémas :

```text
5 schémas
× 200 échantillons
× 2 stratégies
= 2000 résultats
```

Chaque échantillon possède un `sample_id` permettant d'associer les résultats des deux stratégies.

---

## 13. Protocole expérimental

### Configuration

```text
Provider            : OpenRouter
Model               : qwen/qwen3.5-9b
Temperature         : 0.2
Max output tokens   : 4096
Retry max attempts  : 3
```

### Taille

```text
Nombre de schémas          : 5
Échantillons par schéma    : 200
Stratégies                 : 2
Résultats enregistrés      : 2000
```

### Stratégies

#### Baseline

Une seule génération est autorisée.

Elle mesure la capacité du modèle à respecter directement le contrat JSON.

#### Retry

En cas d'échec, une nouvelle génération peut être demandée.

Le système fournit les erreurs précédentes au générateur afin qu'il tente de produire une réponse corrigée.

---

## 14. Métriques

Les principales métriques sont :

### Taux de conformité initiale

Proportion des sorties valides dès la première tentative.

### Taux de conformité finale

Proportion des résultats valides à la fin de la stratégie.

### Taux d'échec définitif

Proportion des résultats restant invalides après toutes les tentatives autorisées.

### Nombre de tentatives

Nombre d'appels nécessaires pour obtenir le résultat final.

### Latence

Durée nécessaire pour effectuer la génération et les éventuelles reprises.

### Coût

Coût associé aux appels du modèle.

Les métriques sont calculées :

- globalement ;
- par schéma ;
- par stratégie ;
- par couple schéma / stratégie.

---

## 15. Résultats

La campagne finale contient :

```text
2000 enregistrements
```

soit :

```text
1000 résultats baseline
1000 résultats retry
```

### Résultats détaillés

| Schéma | Stratégie | Résultats | Conformité initiale | Conformité finale | Tentatives moyennes | Latence moyenne |
|---|---|---:|---:|---:|---:|---:|
| Schema 01 | Baseline | 200 | 100 % | 100 % | 1.00 | 1156.76 ms |
| Schema 01 | Retry | 200 | 100 % | 100 % | 1.00 | 1085.44 ms |
| Schema 02 | Baseline | 200 | 100 % | 100 % | 1.00 | 1761.37 ms |
| Schema 02 | Retry | 200 | 100 % | 100 % | 1.00 | 1569.83 ms |
| Schema 03 | Baseline | 200 | 95 % | 95 % | 1.00 | 2749.80 ms |
| Schema 03 | Retry | 200 | 96 % | **100 %** | 1.04 | 2759.96 ms |
| Schema 04 | Baseline | 200 | 99.5 % | 99.5 % | 1.00 | 3388.09 ms |
| Schema 04 | Retry | 200 | 100 % | 100 % | 1.00 | 4009.82 ms |
| Schema 05 | Baseline | 200 | 100 % | 100 % | 1.00 | 2459.98 ms |
| Schema 05 | Retry | 200 | 100 % | 100 % | 1.00 | 2312.17 ms |

---

## 16. Comparaison globale

### Baseline

```text
989 résultats valides / 1000
Conformité finale : 98.9 %
```

### Retry

```text
1000 résultats valides / 1000
Conformité finale : 100 %
```

La stratégie de reprise permet donc de faire passer le taux de conformité finale observé de :

```text
98.9 % → 100 %
```

---

## 17. Cas du Schema 03

Le `schema_03.json` met particulièrement en évidence l'intérêt de la stratégie de reprise.

### Baseline

```text
190 résultats valides / 200
Conformité finale : 95 %
```

### Retry

```text
Conformité au premier essai : 96 %
Conformité finale           : 100 %
Tentatives moyennes         : 1.04
```

Dans le groupe expérimental utilisant la stratégie `retry`, les sorties invalides au premier essai ont pu être récupérées par les nouvelles tentatives autorisées.

---

## 18. Coût

Coût total enregistré pour les 1000 résultats baseline :

```text
0.055469 USD
```

Coût total enregistré pour les 1000 résultats retry :

```text
0.056277 USD
```

Différence :

```text
+0.000808 USD
```

soit environ :

```text
+1.46 %
```

Dans cette campagne, le gain de fiabilité a donc été obtenu avec une augmentation limitée du coût total.

---

## 19. Latence

Latence moyenne approximative sur l'ensemble des cinq schémas :

```text
Baseline : 2303.20 ms
Retry    : 2347.44 ms
```

La stratégie de reprise entraîne une légère augmentation de la latence moyenne globale.

Cette différence reste limitée dans l'expérience réalisée.

---

## 20. Interprétation

Les résultats montrent que le modèle respecte déjà très bien les contrats JSON simples.

Les difficultés apparaissent principalement lorsque les contraintes deviennent plus complexes.

Le cas du troisième schéma illustre l'intérêt du mécanisme de reprise :

```text
Baseline : 95 %
Retry    : 100 %
```

La stratégie de reprise permet donc d'améliorer la robustesse des sorties structurées sans augmenter fortement le nombre moyen de tentatives.

Il faut cependant préciser que les générations `baseline` et `retry` correspondent à des appels distincts au modèle.

Les données sont comparées sur des `sample_id` appariés, mais un LLM reste probabiliste.

Les résultats doivent donc être interprétés comme une comparaison de deux stratégies et non comme la réparation directe de chaque sortie obtenue par la baseline.

---

## 21. Tests

Les tests peuvent être exécutés sans clé API :

```bash
python -m pytest -q
```

Résultat de la version finale :

```text
53 passed
```

Les tests couvrent notamment :

- les cinq schémas ;
- les sorties valides ;
- les sorties invalides ;
- les champs obligatoires manquants ;
- les types incorrects ;
- les erreurs de parsing ;
- les erreurs de validation ;
- les erreurs de génération ;
- les réponses tronquées ;
- les nouvelles tentatives ;
- le nombre maximal de tentatives ;
- les limites de coût ;
- les limites de latence ;
- la CLI ;
- l'évaluation ;
- la génération du rapport.

---

## 22. Reproductibilité

L'analyse finale peut être reproduite sans clé API à partir des résultats déjà présents dans le dépôt.

### Windows PowerShell

```powershell
python -m pip install -r requirements.txt

$env:PYTHONPATH="src"

python -m pytest -q

python -m json_stress.cli evaluate results\experiment_final.jsonl

python -m json_stress.cli report results\experiment_final.jsonl --output-dir results\report
```

### Linux / macOS

```bash
python -m pip install -r requirements.txt

export PYTHONPATH=src

python -m pytest -q

python -m json_stress.cli evaluate results/experiment_final.jsonl

python -m json_stress.cli report results/experiment_final.jsonl --output-dir results/report
```

Une clé OpenRouter n'est nécessaire que pour générer de nouveaux résultats réels.

---

## 23. Fichiers de résultats

### `results/experiment_final.jsonl`

Contient les 2000 résultats détaillés de la campagne finale.

Les enregistrements contiennent notamment :

```text
schema_id
strategy
sample_id
first_try_valid
final_valid
attempts
latency_ms
cost
error_type
provider
model
data
raw_output
errors
history
stop_reason
prompt_tokens
completion_tokens
cost_status
```

### `results/experiment_summary.csv`

Contient une synthèse des résultats par :

```text
schéma × stratégie
```

### `results/paired_results.csv`

Permet d'analyser les stratégies baseline et retry à partir des identifiants d'échantillons correspondants.

---

## 24. Limites

Plusieurs limites doivent être prises en compte :

- les réponses d'un LLM restent probabilistes ;
- les résultats dépendent du modèle choisi ;
- les résultats peuvent évoluer avec une autre température ;
- les résultats ne garantissent pas le même comportement avec un autre fournisseur ;
- certaines règles métier sont difficiles à représenter uniquement avec JSON Schema ;
- les nouvelles tentatives peuvent augmenter le coût et la latence ;
- les tarifs d'un fournisseur externe peuvent évoluer ;
- certains coûts peuvent être estimés lorsque l'API ne fournit pas directement la valeur réelle ;
- la campagne évalue une configuration précise et ne prétend pas représenter tous les LLM.

---

## 25. Plan B

Le projet peut fonctionner sans API externe grâce au `MockGenerator`.

Il permet :

- d'exécuter les tests ;
- de démontrer la génération ;
- de provoquer des erreurs contrôlées ;
- de tester la validation ;
- de démontrer la stratégie de reprise ;
- d'évaluer des fichiers de résultats ;
- de générer le rapport.

Le projet reste donc démontrable même en cas :

- d'indisponibilité d'OpenRouter ;
- de problème réseau ;
- de quota API épuisé ;
- de clé API indisponible.

---

## 26. Sécurité

Les clés API ne sont jamais stockées directement dans le code source.

Les secrets doivent uniquement être placés dans :

```text
.env
```

Le `.gitignore` exclut notamment :

```text
.env
.env.*
*.pem
*.key
*.p12
*.pfx
secrets.json
```

L'exception suivante permet uniquement de versionner le fichier modèle :

```text
!.env.example
```

Le fichier `.env.example` contient seulement les noms des variables et aucune valeur secrète.

---

## 27. Répartition du travail

Le projet est organisé autour de trois responsabilités principales.

### Schémas et validation

- conception des cinq JSON Schemas ;
- validation des données ;
- gestion des contraintes ;
- tests associés.

### Génération et reprise

- interface du générateur ;
- générateur simulé ;
- intégration OpenRouter ;
- gestion des erreurs ;
- stratégie de reprise ;
- exécution des expériences réelles.

### CLI, évaluation et rapport

- interface en ligne de commande ;
- chargement des résultats ;
- calcul des métriques ;
- comparaison baseline / retry ;
- génération des tableaux ;
- génération des graphiques ;
- génération du rapport ;
- prise en charge des fichiers UTF-8 et UTF-8 BOM.

Les membres participent également à :

- l'intégration ;
- la revue de code ;
- la validation finale ;
- les tests de bout en bout ;
- la préparation des slides ;
- la soutenance et la démonstration.

---

## 28. Livrables

Le projet final comprend :

- le code source ;
- cinq JSON Schemas ;
- les tests automatisés ;
- un fichier `.env.example` sans secret ;
- une interface de démonstration en ligne de commande ;
- les données de la campagne expérimentale ;
- les métriques ;
- les graphiques ;
- le rapport Markdown ;
- la documentation de reproduction ;
- les slides de soutenance ;
- l'historique Git du développement.

---

## 29. Références

- JSON Schema : https://json-schema.org/
- jsonschema : https://python-jsonschema.readthedocs.io/
- pytest : https://docs.pytest.org/
- pandas : https://pandas.pydata.org/
- matplotlib : https://matplotlib.org/
- OpenRouter : https://openrouter.ai/
- OpenAI Python SDK : https://github.com/openai/openai-python

---

## 30. Utilisation de l'intelligence artificielle

Des outils d'intelligence artificielle ont été utilisés comme assistance au cours du développement, notamment pour :

- l'aide à l'implémentation de certaines fonctionnalités ;
- l'interface en ligne de commande ;
- le débogage ;
- la rédaction et l'amélioration de tests ;
- la revue du code ;
- la documentation.

Les propositions produites avec assistance ont été relues, adaptées, exécutées et testées avant leur intégration au projet.

---

## Conclusion

Ce projet montre qu'une chaîne composée de :

```text
génération
+ parsing JSON
+ validation JSON Schema
+ feedback d'erreur
+ reprise bornée
```

peut améliorer la robustesse des sorties structurées produites par un modèle de langage.

La campagne finale comporte **2000 résultats expérimentaux**.

La stratégie baseline atteint :

```text
98.9 % de conformité finale
```

contre :

```text
100 % avec la stratégie retry
```

Dans l'expérience réalisée, cette amélioration est obtenue avec une augmentation limitée du coût et de la latence.

La validation et la reprise constituent donc un mécanisme utile lorsqu'une application dépend d'un contrat JSON strict et ne peut pas accepter directement une sortie invalide produite par un LLM.
