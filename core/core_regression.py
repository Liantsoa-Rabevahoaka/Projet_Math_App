import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression # [cite: 28]

def charger_donnees_csv(chemin_fichier: str) -> tuple[pd.DataFrame | None, str | None]:
    """
    Charge un fichier CSV et retourne un DataFrame pandas. 

    Args:
        chemin_fichier: Le chemin vers le fichier .csv.

    Returns:
        Un tuple (dataframe, erreur).
        - Si succès, retourne (df, None).
        - Si échec, retourne (None, message_erreur).
    """
    try:
        df = pd.read_csv(chemin_fichier)
        if df.empty:
            return None, "Erreur : Le fichier CSV est vide."
        return df, None
    except FileNotFoundError:
        return None, "Erreur : Fichier non trouvé. Vérifiez le chemin."
    except pd.errors.ParserError:
        return None, "Erreur : Impossible de lire le fichier. Est-ce un CSV valide ?"
    except Exception as e:
        return None, f"Une erreur inattendue est survenue : {e}"


def calculer_regression(x_data: pd.Series, y_data: pd.Series) -> tuple[dict, str | None]:
    """
    Calcule la régression linéaire simple.

    Args:
        x_data: La série (colonne) des données X.
        y_data: La série (colonne) des données Y.

    Returns:
        Un tuple (résultats, erreur).
        - Si succès, (dict_resultats, None).
        - Si échec, (None, message_erreur).
    """
    try:
        # sklearn a besoin que X soit un array 2D, d'où le .reshape(-1, 1)
        X = np.array(x_data).reshape(-1, 1)
        Y = np.array(y_data)

        # Créer et entraîner le modèle
        model = LinearRegression()
        model.fit(X, Y)

        # Extraire les résultats
        resultats = {
            "pente": model.coef_[0],
            "ordonnee_origine": model.intercept_,
            "r_carre": model.score(X, Y),
            "equation": f"y = {model.coef_[0]:.4f}x + {model.intercept_:.4f}"
        }
        
        return resultats, None
        
    except Exception as e:
        return None, f"Erreur lors du calcul de la régression : {e}"