# Fichier : Projet_Math_App/ui/ui_tab_markov.py

import numpy as np
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QLineEdit, QPushButton, QSpinBox)
from PySide6.QtCore import Qt

# Importation de l'assistant graphique et de la logique
from ui.ui_helpers import MplCanvas
from core.core_markov import simuler_chaine_markov

class TabMarkov(QWidget):
    """
    Onglet pour la simulation d'une chaîne de Markov.
    Nous codons en dur une matrice 3x3 pour cet exemple.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self) # Layout: Contrôles | Graphique
        
        # --- Colonne de gauche (Contrôles) ---
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(10)
        
        # 1. Grille pour la Matrice de Transition (3x3)
        controls_layout.addWidget(QLabel("Matrice de Transition P (Lignes doivent sommer à 1) :"))
        grid_P = QGridLayout()
        grid_P.setSpacing(5)
        self.entries_P = [] # Pour stocker les QLineEdit
        for i in range(3):
            row = []
            for j in range(3):
                entry = QLineEdit()
                entry.setPlaceholderText(f"P({i} -> {j})")
                entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
                entry.setFixedWidth(60)
                grid_P.addWidget(entry, i, j)
                row.append(entry)
            self.entries_P.append(row)
            
        controls_layout.addLayout(grid_P)
        
        # 2. Paramètres de simulation
        params_layout = QHBoxLayout()
        params_layout.addWidget(QLabel("État initial (0, 1 ou 2):"))
        self.spin_etat_initial = QSpinBox()
        self.spin_etat_initial.setRange(0, 2)
        params_layout.addWidget(self.spin_etat_initial)
        
        params_layout.addWidget(QLabel("Nombre d'étapes:"))
        self.spin_nb_etapes = QSpinBox()
        self.spin_nb_etapes.setRange(1, 1000)
        self.spin_nb_etapes.setValue(50)
        params_layout.addWidget(self.spin_nb_etapes)
        params_layout.addStretch()
        
        controls_layout.addLayout(params_layout)
        
        # 3. Bouton de Simulation
        self.btn_simuler = QPushButton("Simuler la trajectoire")
        controls_layout.addWidget(self.btn_simuler)
        
        # 4. Zone d'erreur (pas de résultat textuel, juste le graphe)
        self.lbl_erreur = QLabel("")
        self.lbl_erreur.setStyleSheet("color: #FF6B6B;")
        controls_layout.addWidget(self.lbl_erreur)
        controls_layout.addStretch()
        
        # --- Colonne de droite (Graphique) ---
        self.plot_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.plot_canvas.axes.set_title("Trajectoire de la Chaîne de Markov")
        
        # Assemblage final
        left_widget = QWidget()
        left_widget.setLayout(controls_layout)
        left_widget.setMaximumWidth(400)
        
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.plot_canvas)

        # --- Connexions ---
        self.btn_simuler.clicked.connect(self.on_simuler_click)
        
        # Pré-remplir avec l'exemple du test
        self.pre_remplir_exemple()

    def pre_remplir_exemple(self):
        # Matrice du test:
        P_exemple = [["0.7", "0.2", "0.1"],
                     ["0.3", "0.5", "0.2"],
                     ["0.2", "0.3", "0.5"]]
        
        for i in range(3):
            for j in range(3):
                self.entries_P[i][j].setText(P_exemple[i][j])
        
        self.spin_etat_initial.setValue(0)
        self.spin_nb_etapes.setValue(50)

    def on_simuler_click(self):
        self.lbl_erreur.setText("") # Effacer l'ancienne erreur
        try:
            # 1. Lire la Matrice P
            P_list = []
            for i in range(3):
                row_list = []
                for j in range(3):
                    val = float(self.entries_P[i][j].text().replace(",", "."))
                    row_list.append(val)
                P_list.append(row_list)
            matrice_transition = np.array(P_list)
            
            # 2. Lire les paramètres
            etat_initial = self.spin_etat_initial.value()
            nb_etapes = self.spin_nb_etapes.value()

            # 3. Appeler la fonction "cerveau"
            trajectoire, erreur = simuler_chaine_markov(matrice_transition, etat_initial, nb_etapes)
            
            # 4. Afficher le résultat
            if erreur:
                self.lbl_erreur.setText(f"Erreur : {erreur}")
            else:
                # Afficher le graphique
                self.plot_canvas.axes.clear()
                
                # Utiliser 'steps-post' est idéal pour les états discrets
                self.plot_canvas.axes.plot(range(nb_etapes), trajectoire, drawstyle='steps-post')
                
                self.plot_canvas.axes.set_title("Trajectoire de la Chaîne de Markov")
                self.plot_canvas.axes.set_xlabel("Étape (Temps)")
                self.plot_canvas.axes.set_ylabel("État")
                self.plot_canvas.axes.set_yticks([0, 1, 2]) # Forcer les ticks pour les états
                self.plot_canvas.axes.grid(True, linestyle='--', alpha=0.6, axis='y')
                self.plot_canvas.fig.tight_layout()
                self.plot_canvas.canvas.draw()
                
        except ValueError:
            self.lbl_erreur.setText("Erreur de saisie : Veuillez entrer des nombres valides dans la matrice.")
        except Exception as e:
            self.lbl_erreur.setText(f"Une erreur inattendue est survenue : {e}")