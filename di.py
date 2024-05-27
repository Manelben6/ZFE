import asyncio
from spade import agent, behaviour


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

    async def send_message(self, sender, recipient, message):
        """
        Simule l'envoi d'un message en l'affichant dans la console.

        Args:
            sender (str): L'identifiant de l'expéditeur.
            recipient (str): L'identifiant du destinataire.
            message (str): Le contenu du message.
        """
        print(f"Message de {sender} à {recipient} : {message}")


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
    agent = ArgumentationAgent("manel@anonym.im", "Ighzer2000", LF1, LV1, F, V, KB)

    # Démarrage de l'agent
    agent.start()

    # Initialisation du dialogue avec le sujet "ZFE"
    await agent.send_message("A1", "A2", "ASSERT(ZFE)")

# Exécuter le programme principal
if __name__ == "__main__":
    asyncio.run(main())