import numpy as np
import pandas as pd

# Importation de nos 4 modules "cerveau"
from core.core_systeme import resoudre_systeme
from core.core_prog_lineaire import resoudre_prog_lineaire
from core.core_regression import charger_donnees_csv, calculer_regression
from core.core_markov import simuler_chaine_markov

def run_tests():
    """Fonction principale pour exécuter tous les tests."""
    
    print("========================================")
    print("🧪 TEST 1 : MODULE SYSTÈME LINÉAIRE 🧪")
    print("========================================")
    
    # Cas 1: Solution unique (Ex: 3x3)
    print("\n--- Cas 1 : Solution unique ---")
    # Exemple:
    # 1x + 2y + 1z = 2
    # 3x + 8y + 1z = 12
    # 0x + 4y + 1z = 2
    A1 = np.array([[1, 2, 1],
                   [3, 8, 1],
                   [0, 4, 1]])
    b1 = np.array([2, 12, 2])
    print(f"Matrice A:\n{A1}")
    print(f"Vecteur b:\n{b1}")
    solution, erreur = resoudre_systeme(A1, b1)
    if erreur:
        print(f"Résultat : ERREUR - {erreur}")
    else:
        print(f"Résultat (Solution X) : {solution}") # Devrait être [2. -1.  6.]

    # Cas 2: Matrice singulière (pas de solution unique)
    print("\n--- Cas 2 : Matrice singulière ---")
    A2 = np.array([[1, 1],
                   [1, 1]])
    b2 = np.array([1, 2])
    print(f"Matrice A:\n{A2}")
    print(f"Vecteur b:\n{b2}")
    solution, erreur = resoudre_systeme(A2, b2)
    if erreur:
        print(f"Résultat : ERREUR ATTENDUE - {erreur}")
    else:
        print(f"Résultat : {solution} (ERREUR - aurait dû échouer)")


    print("\n\n=============================================")
    print("🧪 TEST 2 : MODULE PROGRAMMATION LINÉAIRE 🧪")
    print("=============================================")
    # Exemple (du sujet): Max z = 3x + 2y
    # Je vais ajouter des contraintes pour le test :
    # 1: 2x + y <= 10
    # 2: x + 3y <= 15
    # (x, y >= 0 est géré par défaut dans notre fonction)
    
    direction_pl = "Maximiser"
    fonction_obj = {'x': 3, 'y': 2}
    contraintes = [
        {'coeffs': {'x': 2, 'y': 1}, 'type': '<=', 'rhs': 10},
        {'coeffs': {'x': 1, 'y': 3}, 'type': '<=', 'rhs': 15}
    ]
    
    print(f"Problème : {direction_pl} z = 3x + 2y")
    print("Contraintes :")
    print("  2x + y <= 10")
    print("  x + 3y <= 15")
    
    statut, valeur_obj, valeurs_vars = resoudre_prog_lineaire(direction_pl, fonction_obj, contraintes)
    
    print(f"\nStatut du résultat : {statut}")
    print(f"Valeur optimale de z : {valeur_obj}")
    print(f"Valeurs des variables : {valeurs_vars}")


    print("\n\n========================================")
    print("🧪 TEST 3 : MODULE RÉGRESSION LINÉAIRE 🧪")
    print("========================================")
    
    chemin_csv = "data/donnees_regression.csv"
    print(f"\n--- Cas 1 : Chargement du CSV ({chemin_csv}) ---")
    
    df, erreur = charger_donnees_csv(chemin_csv)
    
    if erreur:
        print(f"Résultat : ERREUR - {erreur}")
    else:
        print(f"Données chargées avec succès. {len(df)} lignes trouvées.")
        print(f"Colonnes disponibles : {list(df.columns)}")
        
        # --- Cas 2 : Calcul de la régression ---
        print("\n--- Cas 2 : Calcul de la régression (sur x, y) ---")
        if 'x' in df.columns and 'y' in df.columns:
            resultats, erreur_calc = calculer_regression(df['x'], df['y'])
            if erreur_calc:
                print(f"Résultat : ERREUR - {erreur_calc}")
            else:
                print("Calcul réussi :")
                print(f"  Équation : {resultats['equation']}")
                print(f"  Pente (m) : {resultats['pente']:.4f}")
                print(f"  Ordonnée (b) : {resultats['ordonnee_origine']:.4f}")
                print(f"  Score R² : {resultats['r_carre']:.4f}")
        else:
            print("ERREUR : Colonnes 'x' et 'y' non trouvées dans le CSV.")


    print("\n\n=================================================")
    print("🧪 TEST 4 : MODULE PROCESSUS STOCHASTIQUE (MARKOV) 🧪")
    print("=================================================")
    
    # Exemple: Matrice de transition 3x3 (ex: météo Soleil=0, Nuage=1, Pluie=2)
    # Demain | S   N   P  (Depuis Aujourd'hui)
    # S      | 0.7 0.2 0.1
    # N      | 0.3 0.5 0.2
    # P      | 0.2 0.3 0.5
    matrice_markov = np.array([[0.7, 0.2, 0.1],
                               [0.3, 0.5, 0.2],
                               [0.2, 0.3, 0.5]])
    
    etat_initial = 0 # On commence par "Soleil"
    nb_etapes = 15 # Simuler 15 jours
    
    print(f"Matrice de transition (3x3):\n{matrice_markov}")
    print(f"État initial : {etat_initial}")
    print(f"Nombre d'étapes : {nb_etapes}")
    
    trajectoire, erreur = simuler_chaine_markov(matrice_markov, etat_initial, nb_etapes)
    
    if erreur:
        print(f"Résultat : ERREUR - {erreur}")
    else:
        print(f"Trajectoire simulée (longueur {len(trajectoire)}) :")
        print(trajectoire)

    print("========================================")
    print("✅ FIN DES TESTS DU 'CORE' ✅")
    print("========================================")


if __name__ == "__main__":
    # On fixe la "graine" aléatoire pour que le test de Markov
    # donne toujours le même résultat à chaque exécution.
    np.random.seed(42)
    
    run_tests()