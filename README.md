# ZFE
# Système de Dialogue Basé sur des Agents

Ce dépôt contient l'implémentation d'un système de dialogue basé sur des agents où les agents peuvent affirmer des positions, argumenter en fonction de connaissances, et contribuer avec des valeurs basées sur un ensemble donné de faits et de valeurs.

## Vue d'Ensemble du Projet

Le Système de Dialogue Basé sur des Agents est conçu pour simuler des conversations entre deux agents, où ils discutent d'un sujet donné en affirmant des faits, générant des arguments, et contribuant à des valeurs basées sur leur base de connaissances. Ce système peut servir de fondation pour des systèmes d'IA plus complexes dans des domaines tels que le raisonnement automatisé, l'IA dans les jeux, ou des outils éducatifs.

## Fonctionnalités


- **Génération d'Arguments**: Génération récursive d'arguments menant à des conclusions spécifiques basées sur une base de connaissances.
- **Initialisation du Dialogue** : Commencer des dialogues sur des sujets spécifiés, en traitant des arguments logiques et des contributions.
- **Sélection de Positions** : Sélection de positions et génération d'arguments basés sur les faits et valeurs disponibles.
- **Évaluation de l'Acceptabilité** : Évaluation de l'acceptabilité des arguments en fonction des priorités des agents.
- **Protocoles de Dialogue**: Implémentation de protocoles pour structurer les échanges entre agents.
## Installation

Clonez le dépôt sur votre machine locale :

```bash
git clone https://github.com/Manelben6/ZFE.git
cd ZFE

Utilisation
Pour utiliser le Système, vous devez créer une instance de la classe Agent et ensuite initier des dialogues basés sur des sujets spécifiques et éxécuter le protocol ensuite.

## Exemple :


### Définir la base de connaissances et les ordres
KB = {
      ("QaF", "snV"), ("QaF", "enV"),
    ("ZFE", "enV"), ("ZFE", "lvp"), ("ZFE", "mdtpF"),
    ("mdtpF", "QaF"), ("lvp", "QaF"),
    ("ZFE", "prog"), ("ZFE", "lmb"), ("ZFE", "vep"),
    ("ZFE", "dev"), ("ZFE", "innov"),
    ("vep", "eqV"), ("vep", "not eqV"),
    ("adp", "lbV"), ("lvp", "QaF"),
    ("mdtpF", "not vid"), ("mdtpF", "att"),
    ("mdtpF", "not ecF"), ("min", "vep"),
    ("cout", "not ecF"), ("lmb", "not lbV"),
    ("vid", "cout"), ("prog", "adp"),
    ("bes", "vid"),
    ("dev", "emF"), ("att", "not emF")
}
LF1 = {"QaF": 4, "mdtpF":3 , "ecF": 2, "emF": 1}
LV1 = {"enV": 2, "snV": 2, "lbV": 2, "eqV": 1}
LF2 = {"ecF":2, "emF":2, "QaF":2, "mdtpF":1}
LV2 = {"lbV":3, "eqV": 3, "enV":1, "snV":1}

F = {"QaF", "mdtpF", "ZFE", "lvp"}
V = {"enV", "snV", "lbV", "eqV"}

### Créer une instance d'Agent
agent1 = Agent(LF1, LV1, F, V, KB, "A1", [])
agent2 = Agent(LF2, LV2, F, V, KB, "A2", [])

# Initialiser le dialogue
phi = "ZFE"
init_dialogue(agent1, phi)

# Executer le protocol
protocol(agent1, agent2, phi, LF1, LF2, LV1, LV2,gamma=0.5, epsilon=1)


## Auteur : 
- Manel Bensalem
