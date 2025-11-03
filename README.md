# 🧰 Boîte à Outils de Modélisation Mathématique

Ce projet est une application de bureau Python (développée avec `ttkbootstrap`) qui fournit une interface graphique pour résoudre plusieurs problèmes de modélisation mathématique.

## Modules Inclus

* **Systèmes Linéaires :** Résolution de $AX=b$.
* **Programmation Linéaire :** Optimisation (Max/Min) via `PuLP`.
* **Régression Linéaire :** Ajustement de modèle sur des données CSV et visualisation.
* **Chaînes de Markov :** Simulation de trajectoires stochastiques.

---

## 🚀 Installation et Lancement

### 1. Prérequis

* [Python 3.10+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)

### 2. Installation Locale

1.  **Clonez le dépôt :**
    ```bash
    git clone [URL_DE_VOTRE_DEPOT]
    cd Projet_Math_App
    ```

2.  **Créez un environnement virtuel :**
    ```bash
    python -m venv venv
    ```

3.  **Activez l'environnement :**
    * Sur Windows : `.\venv\Scripts\activate`
    * Sur macOS/Linux : `source venv/bin/activate`

4.  **Installez les dépendances :**
    ```bash
    (venv) pip install -r requirements.txt
    ```

### 3. Lancement de l'Application

Assurez-vous que votre environnement est toujours actif (`(venv)`).

```bash
(venv) python main.py