from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json

class KnowledgeAgent(Agent):
    def __init__(self, jid, password, LF, LV, F, V, KB):
        super().__init__(jid, password)
        self.LF = LF
        self.LV = LV
        self.F = F
        self.V = V
        self.KB = KB

    async def setup(self):
        print("Agent starting...")
        dialogue_behaviour = self.InitiateDialogueBehaviour()
        self.add_behaviour(dialogue_behaviour, None)

    class InitiateDialogueBehaviour(CyclicBehaviour):
        async def run(self):
            # Here, we initialize the dialogue based on a chosen subject
            subject = "ZFE"  # Example subject
            R = []
            for p in self.agent.V.union(self.agent.F):
                R.extend(self.argue(p, self.agent.KB))

            A = self.filter_arguments(R, subject)
            if A:
                p = self.select_position({arg[2] for arg in A})
                if p:
                    await self.send_message("A2", f"ASSERT({subject})")
                    await self.send_message("A2", f"POSITION({p})")
                    for arg in A:
                        if arg[2] == p:
                            await self.send_message("A2", f"ARGUE ({arg})")

                    if p in self.agent.F and self.is_best(p):
                        for v in self.agent.V:
                            if (p, v) in self.agent.KB:
                                await self.send_message("A2", f"CONTRIBUTE({p}, {v})")

        def argue(self, p, KB):
            results = []
            for (x, y) in KB:
                if y == p:
                    sub_args = self.argue(x, KB)
                    if not sub_args:
                        results.append(([f"{x} → {p}"], x, p))
                    else:
                        for arg in sub_args:
                            premises, _, _ = arg
                            results.append((premises + [f"{x} → {p}"], x, p))
            return results

        def filter_arguments(self, R, phi):
            return [arg for arg in R if phi in arg[0] or phi == arg[2]]

        def select_position(self, positions):
            return max(positions, key=lambda x: self.agent.LF.get(x, -1), default=None)

        def is_best(self, p):
            for q in self.agent.F:
                if q != p and self.agent.LF.get(q, -1) > self.agent.LF.get(p, -1):
                    return False
            return True

        async def send_message(self, recipient, message):
            msg = Message(to=f"{recipient}@jabber.server")  # Correct recipient JID
            msg.set_metadata("performative", "inform")
            msg.body = message
            await self.send(msg)

# Define agent specific parameters
LF = {"QaF": 4, "mdtpF": 3, "ecF": 2, "emF": 2}
LV = {"enV": 3, "snV": 3, "lbV": 1, "eqV": 1}
F = {"QaF", "mdtpF", "ZFE", "lvp"}
V = {"enV", "snV", "lbV", "eqV"}
KB = {
    # Define the knowledge base as needed
}

# Create and start an instance of the agent
agent = KnowledgeAgent("manel@anonym.im", "Ighzer2000", LF, LV, F, V, KB)
agent.start()

# To keep the script running
import asyncio
asyncio.get_event_loop().run_forever()