# Système de Dialogue Basé sur des Agents

Ce dépôt contient l'implémentation d'un système de dialogue basé sur des agents où les agents peuvent affirmer des positions, argumenter en fonction de connaissances, et contribuer avec des valeurs basées sur un ensemble donné de faits et de valeurs.

## Vue d'Ensemble du Projet

Le Système de Dialogue Basé sur des Agents est conçu pour simuler des conversations entre deux agents, où ils discutent d'un sujet donné en affirmant des faits, générant des arguments, et contribuant à des valeurs basées sur leur base de connaissances. Ce système peut servir de fondation pour des systèmes d'IA plus complexes dans des domaines tels que le raisonnement automatisé, l'IA dans les jeux, ou des outils éducatifs.

## Fonctionnalités

- **Génération d'Arguments** : Générer récursivement des arguments menant à des conclusions spécifiques basées sur une base de connaissances.
- **Initialisation du Dialogue** : Commencer des dialogues sur des sujets spécifiés, en traitant des arguments logiques et des contributions.

## Installation

Clonez le dépôt sur votre machine locale :

```bash
git clone https://github.com/Manelben6/ZFE.git
cd ZFE

Utilisation
Pour utiliser le Système de Dialogue Basé sur des Agents, vous devez créer une instance de la classe Agent et ensuite initier des dialogues basés sur des sujets spécifiques.

## Exemple :


### Définir la base de connaissances et les ordres
KB = {
    ("QaF", "snV"), ("QaF", "enV"),
    ...
}
LF1 = {"QaF": 4, "mdtpF": 3, "ZFE": 5, ...}
LV1 = {"enV": 3, "snV": 3, "lbV": 1, ...}
F = {"QaF", "mdtpF", "ZFE", "lvp"}
V = {"enV", "snV", "lbV", "eqV"}

### Créer une instance d'Agent
agent = Agent(LF1, LV1, F, V, KB)

### Initier un dialogue sur un sujet
init_dialogue(agent, "ZFE")


## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à forker le dépôt, apporter des modifications, et soumettre des pull requests. Vous pouvez également ouvrir des issues si vous trouvez des bugs ou avez des suggestions de fonctionnalités.

## Auteur
Manel Bensalem - Manelben6
