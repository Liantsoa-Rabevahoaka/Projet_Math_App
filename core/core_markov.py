import numpy as np

def simuler_chaine_markov(matrice_transition: np.ndarray, 
                          etat_initial: int, 
                          nb_etapes: int) -> tuple[list[int] | None, str | None]:
    """
    Simule une trajectoire de chaîne de Markov.

    Args:
        matrice_transition: Matrice (N x N) des probabilités de transition.
        etat_initial: L'indice de l'état de départ (ex: 0, 1, ...).
        nb_etapes: Le nombre total d'étapes à simuler.

    Returns:
        Un tuple (trajectoire, erreur).
        - Si succès, (liste_etats, None).
        - Si échec, (None, message_erreur).
    """
    try:
        # Validation simple
        n_etats = matrice_transition.shape[0]
        if n_etats != matrice_transition.shape[1]:
            return None, "Erreur : La matrice de transition doit être carrée."
        if not np.allclose(np.sum(matrice_transition, axis=1), 1):
            return None, "Erreur : Les lignes de la matrice ne somment pas à 1."
        if etat_initial >= n_etats or etat_initial < 0:
            return None, "Erreur : L'état initial est en dehors des bornes."

        etats = np.arange(n_etats) # Liste des états possibles [0, 1, ..., N-1]
        trajectoire = [etat_initial]
        etat_actuel = etat_initial

        for _ in range(nb_etapes - 1): # -1 car l'état initial est déjà inclus
            # Probabilités de transition depuis l'état actuel
            probabilites = matrice_transition[etat_actuel]
            
            # Choisir le prochain état basé sur les probabilités [cite: 29]
            etat_actuel = np.random.choice(etats, p=probabilites)
            trajectoire.append(etat_actuel)
            
        return trajectoire, None
        
    except Exception as e:
        return None, f"Une erreur de simulation est survenue : {e}"