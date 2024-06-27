import re
def adjust_not_expression(assert_message, end_message):
    end_message = end_message.replace("NOT", "").strip()
    # Compter le nombre d'occurrences de 'NOT'
    not_count = assert_message.count('NOT')

    # Déterminer si le nombre de 'NOT' est pair ou impair
    if not_count % 2 == 0:
        # Pair: Retourner seulement le message de fin
        return end_message
    else:
        # Impair: Ajouter 'NOT' devant le message de fin
        return f"NOT {end_message}"

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
def extract_messages(list_messages):
    assert_message = None
    position_messages = []  # Using a list to collect multiple position messages

    if not isinstance(list_messages, list):
        raise ValueError("The list_messages must be a list of strings or lists.")

    for item in list_messages:
        if isinstance(item, str):
            # Recherche du motif ASSERT
            assert_match = re.search(r'ASSERT\((.*?)\)', item)
            if assert_match:
                assert_message = assert_match.group(1)

            # Recherche du motif POSITION
            position_match = re.search(r'POSITION\((.*?)\)', item)
            if position_match:
                position_messages.append(position_match.group(1))  # Append to the list

        elif isinstance(item, list):
            # Appel récursif pour traiter la liste imbriquée
            nested_assert, nested_position = extract_messages(item)
            if nested_assert:
                assert_message = nested_assert
            if nested_position:
                position_messages.extend(nested_position)  # Extend the list with nested results

    return assert_message, position_messages
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
    def __init__(self, LF, LV, F, V, KB, name, messages):
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
        self.messages = []
        self.all_selected_positions = []
def select_positions(agent, LF, LV, F, V, KB):
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
        if arguments[position] and position not in agent.all_selected_positions:
            # Determine if this is the highest priority so far and collect all such positions
            if highest_priority is None or priorities[position] == highest_priority:
                highest_priority = priorities[position]
                selected_positions.append(position)
                chosen_positions[position] = True
    all_selected_positions = []
    for k in chosen_positions :
      if chosen_positions[k] and k not in agent.all_selected_positions:
        agent.all_selected_positions.append(k)
    return selected_positions


def select_argue(agent, p, KB):
    """
    Génère récursivement des arguments menant à la position 'p'.
    """
    results = []
    for (x, y) in KB:
        if y == p:
            sub_args = select_argue(agent, x, KB)

            if not sub_args:
                results.append(([x], x , p))
            else:
              for premises, last_target, final_target in sub_args:
                  new_premises = premises + [x]
                  results.append((new_premises,x, p))

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
    for q in F:
        if q != p and agent.LF[q] > agent.LF[p]:
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
    print("I. A1")
    liste_messages = []
    R = []
    for p in agent.V.union(agent.F):
      R.extend(select_argue(agent,p,agent.KB))




    A = filter_arguments(agent, R, phi)
    if A:
      p = select_positions(agent, LF1, LV1, F, V, KB)
      if p:
          send_message("A1", "A2", f"ASSERT({phi})")
          send_message("A1", "A2", f"POSITION({p})")
          liste_messages.append(f"ASSERT({phi})")
          liste_messages.append(f"POSITION({p[0]})")
          for arg in A:

              if arg[2] == p[0]:
                  formatted_arg = reformat_arguments([arg])
                  send_message("A1", "A2", formatted_arg)
                  liste_messages.append(formatted_arg)
          for i in p:
            if i in agent.F and is_best(agent, i):
                for v in agent.V:
                    if (i, v) in agent.KB:
                        send_message("A1", "A2", f"CONTRIBUTE({i}, {v})")
                        liste_messages.append(f"CONTRIBUTE({i}, {v})")
      else:
        print('No discussion')


      return liste_messages


def acceptable(p, LFi, LVi, gamma=0.9, epsilon=0.2):
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


def protocol(current_agent, previous_agent, phi,F,V, LF1, LF2, LV1, LV2, gamma=0.5, epsilon=1):


  list_agents = [agent1, agent2]
  def process_messages(current_agent, previous_agent, list_messages):
    current_agent, previous_agent = switch_agents(current_agent, previous_agent)
    assert_message, position_message = extract_messages(current_agent.messages)

    R = []
    for p in V.union(F):
      R.extend(select_argue(current_agent,p,current_agent.KB))

    A = filter_arguments(current_agent, R, phi)


    LF = current_agent.LF
    LV = current_agent.LV

    previous_agent.messages.append([])
    for message in current_agent.messages:
      if f"ASSERT({assert_message})" in message:
        if "NOT" in assert_message:
          ass_messages = assert_message.replace("NOT", "")
        else:
          ass_messages = f"ASSERT(NOT {assert_message})"
        send_message(current_agent.name, previous_agent.name, f"ASSERT({adjust_not_expression(ass_messages, assert_message)})")
        # send_message(current_agent.name, previous_agent.name, f"ASSERT(NOT { assert_message})")
        previous_agent.messages[-1].append(f"ASSERT({adjust_not_expression(ass_messages, assert_message)})")
        k = select_positions(current_agent, current_agent.LF, current_agent.LV, F, V, KB)
        for i in k:
          if i not in previous_agent.all_selected_positions:
            send_message(current_agent.name, previous_agent.name, f"POSITION({i})")
            previous_agent.messages[-1].append(f"POSITION({i})")
        for i in k:
          if i in F and is_best(current_agent, i):
            for v in V :
              if f"CONTRIBUTE({i,v})" in KB:
                send_message(current_agent.name, previous_agent.name, f"CONTRIBUTE({i,v})")
                previous_agent.messages[-1].append(f"CONTRIBUTE({i,v})")

        for i in k:
          if current_agent.name == "A1":
            R = select_argue(current_agent,f"{i}", current_agent.KB)
          else:
            R = select_argue(current_agent,f"not {i}", current_agent.KB)
            A = filter_arguments(current_agent, R, phi)
          for a in A :
            if a[2] == f"not {i}":
                send_message(current_agent.name, previous_agent.name, f"ARGUE({a})")
                previous_agent.messages[-1].append(f"ARGUE({a})")
      for i in position_message:
        if f"POSITION({i})" in message:
          if i in F:
            if acceptable(i, current_agent.LF, current_agent.LV):
              send_message(current_agent.name, previous_agent.name, f"CONCEDE({i})")
              previous_agent.messages[-1].append(f"CONCEDE{i}")
            else:
              for a in A :
                if a[2] == f"NOT {i}":
                    send_message(current_agent.name, previous_agent.name, f"ARGUE({a})")
                    previous_agent.messages[-1].append(f"ARGUE({a})")

          if i in V:
            if acceptable(i, LF, LV):
              send_message(current_agent.name, previous_agent.name, f"CONCEDE({i})")
              previous_agent.messages[-1].append(f"CONCEDE({i})")
      for k in position_message:

         R.extend(select_argue(current_agent, k, current_agent.KB))
         A = filter_arguments(current_agent, R, phi)

         for i in message:
            if "ARGUE" in i:
                for a in A :
                    if current_agent.name == "A1" :
                        if a[2] == k:
                              send_message(current_agent.name, previous_agent.name, f"ARGUE({a})")
                              A.remove(a)
                              previous_agent.messages[-1].append(f"ARGUE({a[0]})")

    current_agent.messages.clear()
    current_agent, previous_agent = switch_agents(current_agent, previous_agent)
    print(current_agent.name, previous_agent.name)
  positions = F.union(V)
  i = 0
  while positions != set(current_agent.all_selected_positions) and i <= 10:
    process_messages(current_agent, previous_agent, current_agent.messages)
    i += 1
def switch_agents(a1, a2):
  if a1.messages:
    return a1, a2
  else:
    return a2, a1

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
    ("mdtpF", "ecF"), ("min", "vep"),
    ("cout", "not ecF"), ("lmb", "not lbV"),
    ("vid", "cout"), ("prog", "adp"),
    ("bes", "vid"),("ZFE", "bes"),
    ("dev", "not fldF"), ("att", "fldF")
}
LF1 = {"QaF": 4, "mdtpF":2.5 , "ecF": 2, "fldF": 1}
LV1 = {"enV": 2, "snV": 2, "lbV": 2, "eqV": 1}
LF2 = {"ecF":2, "fldF":2, "QaF":2, "mdtpF":1}
LV2 = {"lbV":3, "eqV": 3, "enV":1, "snV":1}
F = {"QaF", "mdtpF", "fldF", "ecF"}
V = {"enV", "snV", "lbV", "eqV"}

agent1 = Agent(LF=LF1, LV=LV1, F=F, V=V, KB=KB, name = "A1", messages=[])
agent2 = Agent(LF=LF2, LV=LV2, F=F, V=V, KB=KB, name = "A2", messages=[])

agent2.messages.append(init_dialogue(agent1, 'ZFE'))
print("A2")
protocol(current_agent=agent1, previous_agent=agent2, phi="ZFE",F=F,V=V, LF1=LF1, LF2=LF2, LV1=LV1, LV2=LV2, gamma=0.5, epsilon=1)
