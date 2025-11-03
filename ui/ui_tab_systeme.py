# Fichier : Projet_Math_App/ui/ui_tab_systeme.py

import numpy as np
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QSizePolicy)
from PySide6.QtCore import Qt

# Importation de la logique "cerveau"
from core.core_systeme import resoudre_systeme

class TabSysteme(QWidget):
    """
    Onglet pour la résolution de systèmes linéaires AX = b.
    Nous codons en dur un système 3x3 pour cet exemple.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # --- Section de Saisie (Matrice A et Vecteur b) ---
        input_layout = QHBoxLayout()
        
        # Grille pour la Matrice A (3x3)
        grid_A = QGridLayout()
        grid_A.setSpacing(5)
        self.entries_A = [] # Pour stocker les QLineEdit
        for i in range(3):
            row = []
            for j in range(3):
                entry = QLineEdit()
                entry.setPlaceholderText(f"A[{i+1},{j+1}]")
                entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
                entry.setFixedWidth(50)
                grid_A.addWidget(entry, i, j)
                row.append(entry)
            self.entries_A.append(row)
            
        # Grille pour le Vecteur b (3x1)
        grid_b = QGridLayout()
        grid_b.setSpacing(5)
        self.entries_b = [] # Pour stocker les QLineEdit
        for i in range(3):
            entry = QLineEdit()
            entry.setPlaceholderText(f"b[{i+1}]")
            entry.setFixedWidth(50)
            entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid_b.addWidget(entry, i, 0)
            self.entries_b.append(entry)

        # Ajout des grilles au layout de saisie
        input_layout.addWidget(QLabel("Matrice A :"))
        input_layout.addLayout(grid_A)
        input_layout.addSpacing(20)
        input_layout.addWidget(QLabel("Vecteur b :"))
        input_layout.addLayout(grid_b)
        input_layout.addStretch() # Pousse tout à gauche
        
        main_layout.addLayout(input_layout)
        
        # --- Bouton de Résolution ---
        self.btn_resoudre = QPushButton("Résoudre le système (3x3)")
        main_layout.addWidget(self.btn_resoudre)
        
        # --- Zone de Résultats ---
        main_layout.addWidget(QLabel("Résultats (Vecteur X) :"))
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setObjectName("result_display") # Pour le style QSS
        self.result_display.setMinimumHeight(100)
        main_layout.addWidget(self.result_display)
        main_layout.addStretch() # Pousse tout en haut

        # --- Connexion du signal ---
        self.btn_resoudre.clicked.connect(self.on_resoudre_click)
        
        # Pré-remplir avec l'exemple du test
        self.pre_remplir_exemple()

    def pre_remplir_exemple(self):
        # Exemple: [[1, 2, 1], [3, 8, 1], [0, 4, 1]] et b = [2, 12, 2]
        # Solution: [2, 1, -2]
        A_exemple = [["1", "2", "1"], ["3", "8", "1"], ["0", "4", "1"]]
        b_exemple = ["2", "12", "2"]
        
        for i in range(3):
            for j in range(3):
                self.entries_A[i][j].setText(A_exemple[i][j])
            self.entries_b[i].setText(b_exemple[i])

    def on_resoudre_click(self):
        """
        Slot exécuté lors du clic sur le bouton "Résoudre".
        """
        try:
            # 1. Lire les valeurs de la Matrice A
            A_list = []
            for i in range(3):
                row_list = []
                for j in range(3):
                    val = float(self.entries_A[i][j].text().replace(",", "."))
                    row_list.append(val)
                A_list.append(row_list)
            A = np.array(A_list)
            
            # 2. Lire les valeurs du Vecteur b
            b_list = []
            for i in range(3):
                val = float(self.entries_b[i].text().replace(",", "."))
                b_list.append(val)
            b = np.array(b_list)

            # 3. Appeler la fonction "cerveau"
            solution, erreur = resoudre_systeme(A, b)
            
            # 4. Afficher le résultat
            if erreur:
                self.result_display.setStyleSheet("color: #FF6B6B;") # Rouge erreur
                self.result_display.setText(erreur)
            else:
                self.result_display.setStyleSheet("color: #6BFF6B;") # Vert succès
                result_str = f"Solution trouvée :\n"
                result_str += f"X1 = {solution[0]:.4f}\n"
                result_str += f"X2 = {solution[1]:.4f}\n"
                result_str += f"X3 = {solution[2]:.4f}\n"
                self.result_display.setText(result_str)
                
        except ValueError:
            self.result_display.setStyleSheet("color: #FF6B6B;")
            self.result_display.setText("Erreur de saisie : Veuillez entrer des nombres valides dans tous les champs.")
        except Exception as e:
            self.result_display.setStyleSheet("color: #FF6B6B;")
            self.result_display.setText(f"Une erreur inattendue est survenue : {e}")