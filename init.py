from spade import agent, behaviour
from spade.message import Message
import asyncio


class ArgumentationAgent(agent.Agent):
    """
    Représente un agent avec une base de connaissances, des valeurs et des faits.

    Attributs :
        LF (dict): Dictionnaire représentant un ordre partiel sur les faits pour l'agent.
        LV (dict): Dictionnaire représentant un ordre partiel sur les valeurs pour l'agent.
        F (set): Ensemble de faits connus par l'agent.
        V (set): Ensemble de valeurs connus par l'agent.
        KB (set): Base de connaissances contenant les relations de faits et valeurs.
    """

    def __init__(self, jid, password, LF, LV, F, V, KB):
        super().__init__(jid, password)
        self.LF = LF
        self.LV = LV
        self.F = F
        self.V = V
        self.KB = KB


class ArgumentationBehaviour(behaviour.CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)  # attendre un message pendant 10 secondes
        if msg:
            print(f"Message reçu par {self.agent.name}: {msg.body}")
            # Traiter le message et générer une réponse
            response = self.agent.process_message(msg.body)
            if response:
                reply = msg.make_reply()
                reply.body = response
                await self.send(reply)
        else:
            print(f"{self.agent.name} n'a pas reçu de message")


def process_message(self, message):
    # Cette méthode devrait être implémentée avec la logique d'argumentation réelle
    return f"Message traité: {message}"


async def setup(self):
    print(f"Agent {self.name} démarrage . . .")
    b = self.ArgumentationBehaviour()
    self.add_behaviour(b)


def argue(agent, p):
    """
    Génère récursivement des arguments menant à la position 'p'.

    Args:
        agent (ArgumentationAgent): L'instance de l'agent.
        p (str): La position choisie par l'agent.

    Returns:
        list: Liste d'arguments menant à la position 'p'.
    """
    results = []
    for (x, y) in agent.KB:
        if y == p:
            sub_args = argue(agent, x)
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
    Filtre les arguments pour inclure seulement ceux impliquant le sujet phi.

    Args:
        agent (ArgumentationAgent): L'instance de l'agent.
        R (list): Liste des arguments.
        phi (str): Sujet à filtrer.

    Returns:
        list: Liste filtrée des arguments.
    """
    return [arg for arg in R if phi in arg[0]]


async def init_dialogue(agent, phi):
    """
    Initialise le dialogue basé sur le sujet phi et traite les arguments.

    Args:
        agent (ArgumentationAgent): L'instance de l'agent.
        phi (str): Le sujet pour initier le dialogue.
    """
    R = []
    for p in agent.V.union(agent.F):
        R.extend(argue(agent, p))

    A = filter_arguments(agent, R, phi)

    if A:
        p = select_position(agent, {arg[2] for arg in A})
        if p:
            await send_message(agent, "ma@anonym.im", f"ASSERT({phi})")
            await send_message(agent, "ma@anonym.im", f"POSITION({p})")
            for arg in A:
                if arg[2] == p:
                    await send_message(agent, "ma@anonym.im", f"ARGUE ({arg})")

            if p in agent.F and is_best(agent, p):
                for v in agent.V:
                    if (p, v) in agent.KB:
                        await send_message(agent, "ma@anonym.im", f"CONTRIBUTE({p}, {v})")


def select_position(agent, positions):
    """
    Sélectionne la position la mieux classée parmi les positions fournies.

    Args:
        agent (ArgumentationAgent): L'instance de l'agent.
        positions (set): Un ensemble de positions possibles.

    Returns:
        str: La position sélectionnée.
    """
    return max(positions, key=lambda x: agent.LF.get(x, -1), default=None)


def is_best(agent, p):
    """
    Détermine si la position 'p' est la meilleure parmi tous les faits dans LF de l'agent.

    Args:
        agent (ArgumentationAgent): L'instance de l'agent.
        p (str): La position à vérifier.

    Returns:
        bool: True si 'p' est la meilleure position, False sinon.
    """
    for q in agent.F:
        if q != p and agent.LF.get(q, -1) > agent.LF.get(p, -1):
            return False
    return True


async def send_message(sender, recipient, message):
    """
    Simule l'envoi d'un message en l'affichant dans la console.

    Args:
        agent (ArgumentationAgent): L'instance de l'agent.
        recipient (str): L'identifiant du destinataire.
        message (str): Le contenu du message.
    """
    print(f"Message de {sender} à {recipient} : {message}")

async def setup(self):
        await super().setup()

        @self.CyclicBehaviour
        async def receive_messages(msg):
            """
            Récupère les messages reçus par l'agent.

            Args:
                msg (spade.ACLMessage.ACLMessage): Le message reçu.
            """
            content = msg.getContent()
            print(f"Message reçu de {msg.getSender().getName()}: {content}")

            # Appliquer l'algorithme de protocole
            await self.apply_protocol(content)

        self.add_behaviour(receive_messages)


async def main():
    # Configuration des bases
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
        ("innov", "QaF"), ("bes", "vid"),
        ("dev", "emF"), ("att", "not emF")
    }
    # Configuration des ordres partiels sur les faits et les valeurs
    LF1 = {"QaF": 4, "mdtpF": 3, "ecF": 2, "emF": 2}
    LV1 = {"enV": 3, "snV": 3, "lbV": 1, "eqV": 1}

    # Création des ensembles de faits et de valeurs
    F = {"QaF", "mdtpF", "ZFE", "lvp"}
    V = {"enV", "snV", "lbV", "eqV"}

    # Création de l'agent avec les bases de connaissances et les ordres partiels
    agent = ArgumentationAgent(LF1, LV1, F, V, KB)

    # Démarrage de l'agent
    await agent.start()

    # Initialisation du dialogue avec le sujet "ZFE"
    await agent.send_message("A1", "A2", "ASSERT(ZFE)")
