from spade import agent, behaviour

class MyAgent(agent):
    async def setup(self):
        print("Agent starting...")

        # Define behaviours
        self.add_behaviour(self.SendBehaviour())
        self.add_behaviour(self.ReceiveBehaviour())

    class SendBehaviour(behaviour):
        async def run(self):
            # Here you can put your logic to send messages to Agent 2
            await self.send("agent2@localhost", "Hello from Agent 1!")

    class ReceiveBehaviour(behaviour):
        async def run(self):
            # Here you can put your logic to receive messages from Agent 2
            msg = await self.receive(timeout=10)  # Timeout after 10 seconds
            if msg:
                print(f"Received message: {msg.body}")

# Agent 2
class MyAgent2(agent):
    async def setup(self):
        print("Agent starting...")

        # Define behaviours
        self.add_behaviour(self.ReceiveBehaviour())

    class ReceiveBehaviour(behaviour):
        async def run(self):
            # Here you can put your logic to receive messages from Agent 1
            msg = await self.receive(timeout=10)  # Timeout after 10 seconds
            if msg:
                print(f"Received message: {msg.body}")

# Example usage
if __name__ == "__main__":
    agent1 = MyAgent("agent1@localhost", "password1")
    agent2 = MyAgent2("agent2@localhost", "password2")

    future1 = agent1.start(auto_register=True)
    future2 = agent2.start(auto_register=True)

    future1.result()
    future2.result()