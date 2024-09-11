import tkinter as tk
import sys
from total import Agent, init_dialogue, protocol  
import time

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

    def flush(self):
        pass

def start_protocol():
    # Initialisation des agents
    LF1 = {"QaF": 4, "mdtpF": 2.5, "ecF": 2, "fldF": 1}
    LV1 = {"enV": 2, "snV": 2, "lbV": 2, "eqV": 1}
    LF2 = {"ecF": 2, "fldF": 2, "QaF": 2, "mdtpF": 1}
    LV2 = {"lbV": 3, "eqV": 3, "enV": 1, "snV": 1}
    F = {"QaF", "mdtpF", "fldF", "ecF"}
    V = {"enV", "snV", "lbV", "eqV"}
    KB = {
        ("QaF", "snV"), ("QaF", "enV"),
        ("ZFE", "enV"), ("ZFE", "lvp"), ("ZFE", "mdtpF"),
        ("mdtpF", "QaF"), ("lvp", "QaF"),
        ("ZFE", "prog"), ("ZFE", "lmb"), ("ZFE", "vep"),
        ("ZFE", "dev"), ("ZFE", "innov"),
        ("vep", "eqV"), ("vep", "not eqV"),
        ("adp", "lbV"), ("lvp", "QaF"),
        ("mdtpF", "not vid"), ("mdtpF", "att"),
        ("mdtpF", "ecF"), ("min", "vep"),
        ("cout", "not ecF"), ("lmb", "not lbV"),
        ("vid", "cout"), ("prog", "adp"),
        ("bes", "vid"), ("ZFE", "bes"),
        ("dev", "not fldF"), ("att", "fldF")
    }
    
    # Création des instances des agents
    global agent1, agent2
    agent1 = Agent(LF=LF1, LV=LV1, F=F, V=V, KB=KB, name="A1", messages=[])
    agent2 = Agent(LF=LF2, LV=LV2, F=F, V=V, KB=KB, name="A2", messages=[])

    # Démarrage du dialogue et du protocole
    agent2.messages.append(init_dialogue(agent1, 'ZFE'))
    print ("A2 A1")
    protocol(current_agent=agent1, previous_agent=agent2, phi="ZFE", F=F, V=V, LF1=LF1, LF2=LF2, LV1=LV1, LV2=LV2, gamma=0.5, epsilon=1)

def create_gui():
    root = tk.Tk()
    root.title("Simulation de dialogue entre 2 agents")

    # Bouton pour démarrer le protocole
    start_button = tk.Button(root, text="Démarrer la démonstration", command=start_protocol)
    start_button.pack(pady=20)

    # Zone de texte pour afficher les résultats
    global output_text
    output_text = tk.Text(root, height=20, width=110)
    output_text.pack(padx=20, pady=20)

    # Rediriger la sortie standard vers la zone de texte
    sys.stdout = TextRedirector(output_text)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
