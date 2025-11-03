# Fichier : Projet_Math_App/ui/ui_tab_prog_lin.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox)
from PySide6.QtCore import Qt

# Importation de la logique "cerveau"
from core.core_prog_lineaire import resoudre_prog_lineaire

class TabProgLin(QWidget):
    """
    Onglet pour la programmation linéaire.
    Simplifié à 2 variables (x, y) et 3 contraintes.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # --- Section Fonction Objectif ---
        obj_layout = QHBoxLayout()
        obj_layout.addWidget(QLabel("Fonction Objectif (z) ="))
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["Maximiser", "Minimiser"])
        obj_layout.addWidget(self.direction_combo)
        
        self.obj_x_coeff = QLineEdit()
        self.obj_x_coeff.setPlaceholderText("Coeff. x")
        self.obj_x_coeff.setFixedWidth(60)
        obj_layout.addWidget(self.obj_x_coeff)
        obj_layout.addWidget(QLabel("x +"))
        
        self.obj_y_coeff = QLineEdit()
        self.obj_y_coeff.setPlaceholderText("Coeff. y")
        self.obj_y_coeff.setFixedWidth(60)
        obj_layout.addWidget(self.obj_y_coeff)
        obj_layout.addWidget(QLabel("y"))
        obj_layout.addStretch()
        
        main_layout.addLayout(obj_layout)
        main_layout.addSpacing(15)
        
        # --- Section Contraintes ---
        main_layout.addWidget(QLabel("Contraintes (sous la forme ax + by <= c) :"))
        constraints_layout = QGridLayout()
        self.contraintes_widgets = [] # Liste pour garder une trace des widgets

        for i in range(3): # 3 contraintes statiques
            row_widgets = {}
            
            row_widgets['x_coeff'] = QLineEdit()
            row_widgets['x_coeff'].setPlaceholderText("Coeff. x")
            row_widgets['x_coeff'].setFixedWidth(60)
            
            row_widgets['y_coeff'] = QLineEdit()
            row_widgets['y_coeff'].setPlaceholderText("Coeff. y")
            row_widgets['y_coeff'].setFixedWidth(60)
            
            row_widgets['op_combo'] = QComboBox()
            row_widgets['op_combo'].addItems(["<=", ">=", "=="])
            row_widgets['op_combo'].setFixedWidth(60)
            
            row_widgets['rhs'] = QLineEdit() # Right-Hand Side
            row_widgets['rhs'].setPlaceholderText("Valeur (c)")
            row_widgets['rhs'].setFixedWidth(80)

            constraints_layout.addWidget(row_widgets['x_coeff'], i, 0)
            constraints_layout.addWidget(QLabel("x +"), i, 1)
            constraints_layout.addWidget(row_widgets['y_coeff'], i, 2)
            constraints_layout.addWidget(QLabel("y"), i, 3)
            constraints_layout.addWidget(row_widgets['op_combo'], i, 4)
            constraints_layout.addWidget(row_widgets['rhs'], i, 5)
            
            self.contraintes_widgets.append(row_widgets)
            
        main_layout.addLayout(constraints_layout)
        
        # --- Bouton de Résolution ---
        self.btn_resoudre = QPushButton("Résoudre le problème")
        main_layout.addWidget(self.btn_resoudre)

        # --- Zone de Résultats ---
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setObjectName("result_display")
        main_layout.addWidget(self.result_display)
        main_layout.addStretch()

        # --- Connexion ---
        self.btn_resoudre.clicked.connect(self.on_resoudre_click)
        
        # Pré-remplir avec l'exemple du test
        self.pre_remplir_exemple()

    def pre_remplir_exemple(self):
        # Max z = 3x + 2y
        self.direction_combo.setCurrentIndex(0) # Maximiser
        self.obj_x_coeff.setText("3")
        self.obj_y_coeff.setText("2")
        
        # 2x + y <= 10
        self.contraintes_widgets[0]['x_coeff'].setText("2")
        self.contraintes_widgets[0]['y_coeff'].setText("1")
        self.contraintes_widgets[0]['op_combo'].setCurrentIndex(0) # <=
        self.contraintes_widgets[0]['rhs'].setText("10")
        
        # x + 3y <= 15
        self.contraintes_widgets[1]['x_coeff'].setText("1")
        self.contraintes_widgets[1]['y_coeff'].setText("3")
        self.contraintes_widgets[1]['op_combo'].setCurrentIndex(0) # <=
        self.contraintes_widgets[1]['rhs'].setText("15")
        
        # La 3ème contrainte reste vide

    def on_resoudre_click(self):
        try:
            # 1. Lire la direction
            direction = self.direction_combo.currentText()
            
            # 2. Lire la fonction objectif
            obj_x = float(self.obj_x_coeff.text() or 0)
            obj_y = float(self.obj_y_coeff.text() or 0)
            fonction_obj = {'x': obj_x, 'y': obj_y}
            
            # 3. Lire les contraintes
            contraintes = []
            for row in self.contraintes_widgets:
                x_coeff_str = row['x_coeff'].text()
                rhs_str = row['rhs'].text()
                
                # Si les deux champs (coeff x et rhs) sont remplis
                if x_coeff_str and rhs_str:
                    x_coeff = float(x_coeff_str)
                    y_coeff = float(row['y_coeff'].text() or 0)
                    op = row['op_combo'].currentText()
                    rhs = float(rhs_str)
                    
                    contraintes.append({
                        'coeffs': {'x': x_coeff, 'y': y_coeff},
                        'type': op,
                        'rhs': rhs
                    })
            
            if not contraintes:
                raise ValueError("Veuillez définir au moins une contrainte.")

            # 4. Appeler la fonction "cerveau"
            statut, valeur_obj, valeurs_vars = resoudre_prog_lineaire(direction, fonction_obj, contraintes)

            # 5. Afficher les résultats
            self.result_display.setStyleSheet("color: #F0F0F0;")
            result_str = f"--- RÉSULTATS DE L'OPTIMISATION ---\n\n"
            result_str += f"Statut : {statut}\n"
            
            if statut == "Optimal":
                self.result_display.setStyleSheet("color: #6BFF6B;")
                result_str += f"\nValeur {direction.lower().replace('r', 'le')} de z = {valeur_obj:.4f}\n"
                result_str += "\nValeurs des variables :\n"
                for var, val in valeurs_vars.items():
                    if val > 1e-6: # N'afficher que les variables non nulles
                        result_str += f"  {var.replace('Var_', '')} = {val:.4f}\n"
            else:
                 self.result_display.setStyleSheet("color: #FF6B6B;")
            
            self.result_display.setText(result_str)

        except ValueError as e:
            self.result_display.setStyleSheet("color: #FF6B6B;")
            self.result_display.setText(f"Erreur de saisie : {e}")
        except Exception as e:
            self.result_display.setStyleSheet("color: #FF6B6B;")
            self.result_display.setText(f"Une erreur inattendue est survenue : {e}")