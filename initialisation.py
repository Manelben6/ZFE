class Agent:
    """
    Représente un agent avec une base de connaissances, des valeurs et des faits.

    Attributs :
        LF (dict): Dictionnaire représentant un ordre partiel sur les faits pour l'agent.
        LV (dict): Dictionnaire représentant un ordre partiel sur les valeurs pour l'agent.
        F (set): Ensemble de faits connus par l'agent.
        V (set): Ensemble de valeurs connus par l'agent.
        KB (set): Base de connaissances contenant.
    """
    def __init__(self, LF, LV, F, V, KB):
        """
        Initialise une instance de l'Agent.

        Args:
            LF (dict): Ordre partiel sur les faits.
            LV (dict): Ordre partiel sur les valeurs.
            F (set): Ensemble de faits.
            V (set): Ensemble de valeurs.
            KB (set): Base de connaissances.
        """
        self.LF = LF
        self.LV = LV
        self.F = F
        self.V = V
        self.KB = KB


def argue(agent, p,KB):
    """
    Génère récursivement des arguments menant à la position 'p'.

    Args:
        agent (Agent): L'instance de l'agent.
        p (str): La position choisie par l'agent.

    Returns:
        list: Liste d'arguments menant à la position 'p'.
    """
    results = []
    for (x, y) in agent.KB:
        if y == p:
            sub_args = argue(agent, x,KB)
            if not sub_args:
                results.append(([x], x, p))
            else:
                for arg in sub_args:
                    premises, _, _ = arg
                    results.append((premises + [x], x, p))
    return results


def format_argument(arg):
    """ Formatte l'argument pour le rendre lisible selon le format spécifié. """
    premises, _, conclusion = arg
    premises_str = ", ".join(premises)
    explanation = "Explication: " + " ainsi on peut conclure ".join(
        ["{} est vrai, or si {} alors {}".format(prem.split(" → ")[0], prem.split(" → ")[0], prem.split(" → ")[1])
         for prem in premises]) + f" ainsi on peut conclure {conclusion}"
    return f"({premises_str}, {conclusion}) : {explanation}"


def filter_arguments(agent, R, phi):
    """
    Filtre les arguments pour ne inclure que ceux impliquant le sujet phi.

    Args:
        agent (Agent): L'instance de l'agent.
        R (list): Liste des arguments.
        phi (str): Sujet à filtrer.

    Returns:
        list: Liste filtrée des arguments.
    """
    return [arg for arg in R if phi in arg[0] ]

def init_dialogue(agent, phi):
    """
    Initialise le dialogue basé sur le sujet phi et traite les arguments.

    Args:
        agent (Agent): L'instance de l'agent.
        phi (str): Le sujet pour initier le dialogue.
    """
    R = []
    for p in agent.V.union(agent.F):
        R.extend(argue(agent, p,agent.KB))

    A = filter_arguments(agent, R, phi)

    if A:
        p = select_position(agent, {arg[2] for arg in A})
        if p:
            send_message("A1", "A2", f"ASSERT({phi})")
            send_message("A1", "A2", f"POSITION({p})")
            for arg in A:
                if arg[2] == p:
                    send_message("A1", "A2", f"ARGUE ({arg})")

            if p in agent.F and is_best(agent, p):
                for v in agent.V:
                    if (p, v) in agent.KB:
                        send_message("A1", "A2", f"CONTRIBUTE({p}, {v})")

def select_position(agent, positions):
    """
    Sélectionne la position la mieux classée parmi les positions fournies.

    Args:
        agent (Agent): L'instance de l'agent.
        positions (set): Un ensemble de positions possibles.

    Returns:
        str: La position sélectionnée.
    """
    return max(positions, key=lambda x: agent.LF.get(x, -1), default=None)

def is_best(agent, p):
    """
    Détermine si la position 'p' est la meilleure parmi tous les faits dans LF de l'agent.

    Args:
        agent (Agent): L'instance de l'agent.
        p (str): La position à vérifier.

    Returns:
        bool: True si 'p' est la meilleure position, False sinon.
    """
    for q in agent.F:
        if q != p and agent.LF.get(q, -1) > agent.LF.get(p, -1):
            return False
    return True

def send_message(sender, recipient, message):
    """
    Simule l'envoi d'un message en l'affichant dans la console.

    Args:
        sender (str): L'identifiant de l'expéditeur.
        recipient (str): L'identifiant du destinataire.
        message (str): Le contenu du message.
    """
    print(f"Message de {sender} à {recipient} : {message}")



# Example d'utilisation
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
    ("vid", "cout"), ("prog", "adp"), ("bes", "vid"),
    ("dev", "emF"), ("att", "not emF")
}
LF1 = {"QaF": 4, "mdtpF": 3, "ecF": 2, "emF": 2}
LV1 = {"enV": 3, "snV": 3, "lbV": 1, "eqV": 1}
F = {"QaF", "mdtpF", "ZFE", "lvp"}
V = {"enV", "snV", "lbV", "eqV"}

# Creation d'une instance de la classe Agent
agent = Agent(LF1, LV1, F, V, KB)

# Initialisation du dialogue
init_dialogue(agent, "ZFE")