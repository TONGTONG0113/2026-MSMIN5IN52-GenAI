# Nom du projet

## Groupe 200OK

| Membre | Contribution principale |
|---|---|
| À compléter | À compléter |

## Sujet

- **Identifiant du catalogue :** A3
- **Titre :** Contrats JSON sous stress
- **Problématique :** Comment évaluer la capacité d'un modèle de langage à produire des sorties JSON conformes à un schéma défini, y compris dans des conditions d'échec, et mesurer l'efficacité des stratégies de validation et de reprise.
- **MVP :** Définir cinq JSON Schemas de difficulté croissante, générer des sorties avec un modèle de langage, valider les résultats, appliquer une stratégie de reprise en cas d'échec et mesurer les taux de conformité, le coût et la latence sur au moins 200 générations.

## Architecture

Le système comprend les composants suivants :

Schemas : cinq JSON Schemas de difficulté croissante.

Générateur : envoie les instructions et les contraintes au modèle de langage.

Validateur : vérifie la syntaxe JSON et la conformité au schéma.

Gestionnaire de reprise : traite les erreurs de validation et limite le nombre de nouvelles tentatives.

Évaluateur : mesure la conformité initiale et finale, la latence et le coût.

Rapport : présente les résultats sous forme de tableaux et de visualisations.

L'architecture définitive, les modèles utilisés et les services externes seront documentés après leur implémentation.

## Installation

```bash
# Commandes reproductibles à compléter
```

Figez les versions dans un fichier de dépendances ou un lockfile adapté à votre écosystème. Copiez `.env.example` vers `.env`, puis renseignez localement les valeurs. Ne commitez jamais `.env`.

## Utilisation

```bash
# Commande de lancement à compléter
```

## Tests

```bash
# Commande de test non interactive à compléter
```

Indiquez les résultats obtenus et les cas d'échec couverts.

## Résultats et évaluation

L'évaluation portera sur au moins 200 générations. Les métriques comprendront :

le taux de conformité au premier essai ;

le taux de conformité final après reprise ;

le nombre moyen de tentatives ;

la latence ;

le coût estimé.

Une baseline simple sera comparée à la stratégie avec reprise. Le protocole, les paramètres et les résultats réels seront documentés afin de rendre l'expérience reproductible.

## Limites et plan B

Les limites possibles comprennent les erreurs de génération, les réponses tronquées, les indisponibilités de l'API, les délais d'attente, les coûts et les limites des schémas utilisés.

Un mode de démonstration de secours utilisant des réponses simulées sera préparé. Un modèle local compatible pourra être évalué comme solution alternative.

## Répartition du travail

Expliquez la contribution de chaque membre et le mode de collaboration.

## Licence et références

Listez les licences du code, des modèles et des données, puis les ressources utilisées.
