# 📐 Projet de Modélisation Mathématique

Ceci est une application Python de bureau conçue pour un projet de Modélisation Mathématique. Elle fournit une interface graphique moderne et intuitive pour effectuer des calculs et des simulations dans quatre domaines clés :

  * Systèmes linéaires
  * Programmation linéaire
  * Régression linéaire
  * Chaînes de Markov

L'interface est construite avec **PySide6** (Qt for Python) et tous les calculs sont séparés de l'interface pour une maintenabilité maximale.

*(Il est recommandé d'ajouter ici une capture d'écran de l'application lancée, montrant l'interface principale.)*

-----

## 🧭 Fonctionnalités

L'application est organisée en quatre onglets, chacun correspondant à un module mathématique :

1.  **📈 Système Linéaire :** Permet de résoudre un système d'équations linéaires de type $AX=b$ pour une matrice $A$ ($3 \times 3$) et un vecteur $b$.
2.  **⚖️ Programmation Linéaire :** Permet de maximiser ou minimiser une fonction objectif linéaire à 2 variables, soumise à 3 contraintes.
3.  **📊 Régression Linéaire :** Permet de charger un fichier `.csv`, de sélectionner les colonnes $X$ et $Y$, et de calculer le modèle de régression linéaire simple ($y = mx + b$). Affiche le $R^2$, l'équation, et trace le nuage de points avec la droite de régression.
4.  **🎲 Chaîne de Markov :** Permet de simuler la trajectoire d'une chaîne de Markov à 3 états en fournissant la matrice de transition, l'état initial et le nombre d'étapes. Affiche la trajectoire de l'état dans le temps.

-----

## 🛠️ Technologies Utilisées

  * **Python 3.7+**
  * **PySide6 :** Pour l'interface graphique moderne.
  * **NumPy :** Pour tous les calculs matriciels et l'algèbre linéaire.
  * **PuLP :** Pour la modélisation et la résolution du problème de programmation linéaire.
  * **Scikit-learn :** Pour le calcul du modèle de régression linéaire.
  * **Pandas :** Pour le chargement et la manipulation des données du fichier `.csv`.
  * **Matplotlib :** Pour l'intégration des graphiques (régression et Markov) dans l'interface.

-----

## 🚀 Instructions d'Installation et de Lancement

Suivez ces étapes **précisément** pour installer et lancer l'application sans erreur.

### Prérequis

  * **Python 3.7 ou plus récent** doit être installé sur votre système. Assurez-vous qu'il est ajouté à votre `PATH` (vous pouvez le vérifier en tapant `python --version` dans un terminal).

-----

### Étape 1 : Obtenir les Fichiers

Assurez-vous que vous disposez de l'intégralité du projet avec la structure de dossiers correcte :

```
Projet_Math_App/
|-- core/
|-- ui/
|-- data/
|-- main.py
|-- requirements.txt
|-- ... (autres fichiers)
```

-----

### Étape 2 : Ouvrir un Terminal

Ouvrez votre terminal (par exemple, **PowerShell** ou **CMD** sur Windows, ou le terminal intégré de VS Code).

Naviguez jusqu'au dossier racine de votre projet (là où se trouve `main.py`) :

```bash
# Exemple :
cd D:\Chemin\Vers\Votre\Projet_Math_App
```

-----

### Étape 3 : Créer l'Environnement Virtuel

C'est une étape **cruciale** pour isoler les dépendances de votre projet.

```bash
python -m venv venv
```

Cela va créer un nouveau dossier `venv/` dans votre projet.

-----

### Étape 4 : Activer l'Environnement Virtuel

Vous devez "activer" cet environnement avant d'installer quoi que ce soit.

#### Sur Windows (PowerShell) :

C'est le terminal par défaut dans VS Code.

```powershell
.\venv\Scripts\Activate.ps1
```

**ATTENTION :** Si vous obtenez une **erreur en rouge** mentionnant que "l'exécution des scripts est désactivée sur ce système", vous devez d'abord exécuter cette commande (juste une fois) :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Appuyez sur `O` (pour Oui) si on vous le demande, puis relancez la commande `.\venv\Scripts\Activate.ps1`.

#### Sur Windows (CMD - Command Prompt) :

Une alternative plus simple si PowerShell pose problème.

```cmd
.\venv\Scripts\activate.bat
```

#### Sur macOS / Linux :

```bash
source venv/bin/activate
```

**Vérification :** Une fois l'environnement activé, le nom `(venv)` doit apparaître au début de votre ligne de commande.

-----

### Étape 5 : Installer les Dépendances

Maintenant que vous êtes dans l'environnement virtuel `(venv)`, installez toutes les bibliothèques nécessaires en une seule commande :

```bash
pip install -r requirements.txt
```

Cela va prendre une minute ou deux pour tout télécharger et installer (NumPy, PySide6, PuLP, etc.).

-----

### Étape 6 : Lancer l'Application

Une fois l'installation terminée, vous pouvez lancer l'application :

```bash
python main.py
```

La fenêtre de l'application devrait s'ouvrir. Vous pouvez commencer à tester les différents onglets.

-----

## 📁 Structure du Projet

  * `main.py` : Point d'entrée principal. Crée la fenêtre, assemble les onglets et applique le style.
  * `requirements.txt` : Liste de toutes les bibliothèques Python requises.
  * `data/` : Contient les fichiers de données (ex: `donnees_regression.csv`).
  * `core/` : Le "cerveau" de l'application. Contient toute la logique mathématique pure, sans aucun code d'interface.
  * `ui/` : Le "visage" de l'application. Contient les fichiers PySide6 qui définissent chaque onglet et l'interaction utilisateur.
  * `venv/` : (Dossier généré) L'environnement virtuel contenant les bibliothèques installées.