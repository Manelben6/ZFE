def reformat_arguments(args):
    formatted_args = []
    for premises, last_arg, final_target in args:
        # Gérer l'élément initial comme une liste et construire les transitions
        transitions = []
        previous = None
        fact = "ZFE"
        first_rule = f"→ {fact}"
        for elem in premises:
            if previous is not None:
                transitions.append(f'"{previous}" → "{elem}"')
            previous = elem
        if previous is not None:

            transitions.append(f'"{previous}" → "{final_target}"')

        # Formater la nouvelle chaîne ARGUE

        transition_str = ", ".join(transitions)
        new_argue = f'ARGUE({{{first_rule}, {transition_str}}}, "{final_target}")'
        formatted_args.append(new_argue)

    return formatted_args

import re
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
    def __init__(self, LF, LV, F, V, KB, name):
        """
        Initialise une instance de l'Agent.

        Args:
            LF (dict): Ordre partiel sur les faits.
            LV (dict): Ordre partiel sur les valeurs.
            F (set): Ensemble de faits.
            V (set): Ensemble de valeurs.
            KB (set): Base de connaissances.
        """
        self.name = name
        self.LF = LF
        self.LV = LV
        self.F = F
        self.V = V
        self.KB = KB

def select_positions(LF, LV, F, V, KB):
    # Combine LF and LV for complete priority mapping, defaulting to a low priority for undefined items
    priorities = {**{k: 0 for k in F.union(V)}, **LF, **LV}

    # Create a dictionary to track whether a position has been chosen
    chosen_positions = {key: False for key in priorities.keys()}

    # Combine F and V for iteration
    positions = list(F.union(V))

    # Sort positions by their priority (descending)
    positions.sort(key=lambda x: priorities.get(x, 0), reverse=True)

    # Convert KB into a dictionary where each position points to its arguments/conclusions
    arguments = {position: set() for position in positions}
    for pred, concl in KB:
        if concl in arguments:
            arguments[concl].add(pred)

    # Find the highest priority position(s) that can be concluded and not chosen yet
    selected_positions = []
    highest_priority = None

    for position in positions:
        # Check if the position can be concluded based on arguments and not already chosen
        if arguments[position] and not chosen_positions[position]:
            # Determine if this is the highest priority so far and collect all such positions
            if highest_priority is None or priorities[position] == highest_priority:
                highest_priority = priorities[position]
                selected_positions.append(position)
                chosen_positions[position] = True
            elif priorities[position] > highest_priority:
                # Reset the list if a higher priority position is found
                highest_priority = priorities[position]
                selected_positions = [position]
                chosen_positions = {key: False for key in chosen_positions.keys()}
                chosen_positions[position] = True

    return selected_positions


def argue(agent, p, KB):
    """
    Génère récursivement des arguments menant à la position 'p'.
    """
    results = []
    for (x, y) in KB:
        if y == p:
            sub_args = argue(agent, x, KB)
            if not sub_args:
                results.append(([x], x, p))
            else:
              for premises, last_arg, final_target in sub_args:
                  new_premises = premises + [x]
                  results.append((new_premises, x, p))

    return results

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
    res = [arg for arg in R if phi in arg[0] ]
    return res


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

def init_dialogue(agent, phi):
    """
    Initialise le dialogue basé sur le sujet phi et traite les arguments.

    Args:
        agent (Agent): L'instance de l'agent.
        phi (str): Le sujet pour initier le dialogue.
    """
    liste_messages = []
    R = []
    for p in agent.V.union(agent.F):
        R.extend(argue(agent,p,agent.KB))


    A = filter_arguments(agent, R, phi)
    if A:
        p = select_positions(LF1, LV1, F, V, KB)
        if p:
            send_message("A1", "A2", f"ASSERT({phi})")
            send_message("A1", "A2", f"POSITION({p})")
            liste_messages.append(f"ASSERT({phi})")
            liste_messages.append(f"POSITION({p})")
            for arg in A:
                if arg[2] == p[0]:
                    formatted_arg = reformat_arguments([arg])
                    send_message("A1", "A2", formatted_arg)
                    liste_messages.append(formatted_arg)

            if p[0] in agent.F and is_best(agent, p[0]):
                for v in agent.V:
                    if (p[0], v) in agent.KB:
                        send_message("A1", "A2", f"CONTRIBUTE({p[0]}, {v})")
                        liste_messages.append(f"CONTRIBUTE({p[0]}, {v})")
    return liste_messages



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
    ("vid", "cout"), ("prog", "adp"),
    ("innov", "QaF"), ("bes", "vid"),
    ("dev", "emF"), ("att", "not emF")
}
LF1 = {"QaF": 4, "mdtpF":3 , "ecF": 2, "emF": 1}
LV1 = {"enV": 3, "snV": 3, "lbV": 1, "eqV": 1}
F = {"QaF", "mdtpF", "ZFE", "lvp"}
V = {"enV", "snV", "lbV", "eqV"}

# Creation d'une instance de la classe Agent
agent1 = Agent(LF1, LV1, F, V, KB, "A1")

# Initialisation du dialogue
init_dialogue(agent1, "ZFE")


def acceptable(p, LFi, LVi, gamma=0.7, epsilon=0.2):
    """
    Détermine si le rang de 'p' dans les ordres partiels 'LFi' ou 'LVi' est dans la fraction supérieure 'gamma',
    modifiée par 'epsilon' selon que 'p' soit un fait ou une valeur.

    Args:
        p (str): La proposition (fait ou valeur) à évaluer.
        LFi (dict): Dictionnaire représentant un ordre partiel sur les faits pour un agent.
        LVi (dict): Dictionnaire représentant un ordre partiel sur les valeurs pour un agent.
        gamma (float): Seuil ratio (entre 0 et 1) définissant la fraction supérieure de la liste.
        epsilon (int): La concession qui modifie le rang de 'p'.

    Returns:
        bool: Vrai si 'p' est dans la plage acceptable, sinon Faux.
    """
    total_facts = len(LFi)
    total_values = len(LVi)

    if p in LFi:
        # Get current rank and adjust for epsilon (assuming higher value is a higher rank)
        current_rank = LFi[p]
        modified_rank = current_rank - epsilon
        # Check if the modified rank is within the top gamma portion
        return modified_rank / total_facts >= (1 - gamma)
    elif p in LVi:
        # Get current rank and adjust for epsilon (assuming higher value is a higher rank)
        current_rank = LVi[p]
        modified_rank = current_rank + epsilon
        # Check if the modified rank is within the top gamma portion
        return modified_rank / total_values >= (1 - gamma)

    return False  # If 'p' is neither in LFi nor LVi

def protocol(current_agent, previous_agent, phi, LF1, LF2, LV1, LV2, gamma=0.5, epsilon=1):
  def extract_messages(list_messages):
    assert_message = None
    position_message = None

    # Check if the provided list_messages is a list of strings or contains nested lists
    if not isinstance(list_messages, list):
        raise ValueError("The list_messages must be a list.")

    for item in list_messages:
        # Check if the item is a list, if so, recurse or process differently
        if isinstance(item, list):
            nested_assert, nested_position = extract_messages(item)
            if nested_assert:
                assert_message = nested_assert
            if nested_position:
                position_message = nested_position
        elif isinstance(item, str):
            # Search for ASSERT pattern
            match = re.search(r'ASSERT\((.*?)\)', item)
            if match:
                assert_message = match.group(1)
            # Search for POSITION pattern
            match = re.search(r'POSITION\((.*?)\)', item)
            if match:
                position_message = match.group(1)

    return assert_message, position_message

  agent1 = Agent(LF=LF1, LV=LV1, F=F, V=V, KB=KB, name = "A1")
  agent2 = Agent(LF=LF2, LV=LV2, F=F, V=V, KB=KB, name = "A2")

  list_agents = [agent1, agent2]
  list_messages = []
  list_messages.append(init_dialogue(current_agent, phi))
  assert_message, position_message = extract_messages(list_messages)
  current_agent = list_agents[-1]
  previous_agent = list_agents[0]

  R = argue(current_agent,"QaF", current_agent.KB)
  A = filter_arguments(current_agent, R, phi)
  LF = current_agent.LF
  LV = current_agent.LV


  print("Liste Message", list_messages)
  print("Dernier Message", list_messages[-1])
  for message in list_messages[-1]:
    if f"ASSERT({assert_message})" in message:
      if len(A) > 0:
        send_message(current_agent.name, previous_agent.name, f"ASSERT(NOT { assert_message})")
        p = select_positions(LF2, LV2, F, V, KB)
        send_message(current_agent.name, previous_agent.name, f"POSITION({p})")
        if p[0] in F and is_best(p[0],LF):
          for v in V :
            if f"CONTRIBUTE({v,p[0]})" in KB:
              send_message(current_agent.name, previous_agent.name, f"CONTRIBUTE({v,p[0]})")
          for a in A :
            if a[2] == p[0]:
                send_message(current_agent.name, previous_agent.name, f"ARGUE({a})")
      else :
          send_message(current_agent.name, previous_agent.name, f"ACCEPT({phi})")
    p = position_message
    if f"POSITION(['QaF'])" in message:
      if 'QaF' in F:
        if acceptable("QaF", LF2, LV2):
          send_message(current_agent.name, previous_agent.name, f"CONCEDE('QaF')")
        else:
          for a in A :
            if a[2] == "QaF":
                send_message(current_agent.name, previous_agent.name, f"ARGUE({a})")

      if p[0] in V:
        if acceptable(p[0], LF, LV):
          send_message(current_agent.name, previous_agent.name, f"CONCEDE({p[0]})")

    if "ARGUE" in message:
      for a in A :
            if a[2] == f"NOT lbV":
                send_message(current_agent.name, previous_agent.name, f"ARGUE({a[0]})")

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
LF1 = {"QaF": 4, "mdtpF": 3, "ecF": 2, "emF": 1}
LV1 = {"enV": 3, "snV": 3, "lbV": 1, "eqV": 1}
LF2 = {"ecF":3, "emF":3, "QaF":2, "mdtpF":1}
LV2 = {"lbV":3, "eqV": 3, "enV":2, "snV":2}
F = {"QaF", "mdtpF", "ZFE", "lvp"}
V = {"enV", "snV", "lbV", "eqV"}

agent1 = Agent(LF=LF1, LV=LV1, F=F, V=V, KB=KB, name="A1")
agent2 = Agent(LF=LF2, LV=LV2, F=F, V=V, KB=KB, name="A2")

protocol(current_agent=agent1, previous_agent=agent2, phi="ZFE", LF1=LF1, LF2=LF2, LV1=LV1, LV2=LV2, gamma=0.5, epsilon=1)