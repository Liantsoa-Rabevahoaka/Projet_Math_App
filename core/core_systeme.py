import numpy as np

def resoudre_systeme(A: np.ndarray, b: np.ndarray) -> tuple[np.ndarray | None, str | None]:
    """
    Résout un système d'équations linéaires AX = b.

    Args:
        A: La matrice (N x N) des coefficients.
        b: Le vecteur (N x 1) des résultats.

    Returns:
        Un tuple (solution, erreur).
        - Si la solution existe, retourne (X, None).
        - En cas d'erreur (matrice singulière), retourne (None, message_erreur).
    """
    try:
        # Tente de résoudre le système en utilisant la fonction de NumPy [cite: 26]
        solution = np.linalg.solve(A, b)
        return solution, None
    except np.linalg.LinAlgError:
        # Gère le cas où la matrice A est singulière (pas de solution unique)
        return None, "Erreur : La matrice est singulière, le système n'admet pas de solution unique."
    except Exception as e:
        # Gère toute autre erreur potentielle
        return None, f"Une erreur inattendue est survenue : {e}"