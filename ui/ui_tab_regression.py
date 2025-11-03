# Fichier : Projet_Math_App/ui/ui_tab_regression.py

import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTextEdit, QComboBox, QFileDialog)
from PySide6.QtCore import Qt

# Importation de l'assistant graphique et de la logique
from ui.ui_helpers import MplCanvas
from core.core_regression import charger_donnees_csv, calculer_regression

class TabRegression(QWidget):
    """
    Onglet pour la régression linéaire à partir d'un fichier CSV.
    """
    def __init__(self):
        super().__init__()
        self.dataframe = None # Pour stocker les données chargées
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self) # Layout principal: Contrôles | Graphique
        
        # --- Colonne de gauche (Contrôles) ---
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(10)
        
        # 1. Chargement Fichier
        self.btn_load_csv = QPushButton("1. Charger un fichier CSV")
        controls_layout.addWidget(self.btn_load_csv)
        
        self.lbl_file_status = QLabel("Aucun fichier chargé.")
        self.lbl_file_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.lbl_file_status)
        
        # 2. Sélection des Colonnes
        columns_layout = QHBoxLayout()
        self.combo_x = QComboBox()
        self.combo_y = QComboBox()
        columns_layout.addWidget(QLabel("Variable X :"))
        columns_layout.addWidget(self.combo_x)
        columns_layout.addWidget(QLabel("Variable Y :"))
        columns_layout.addWidget(self.combo_y)
        controls_layout.addLayout(columns_layout)
        
        # 3. Bouton de Calcul
        self.btn_calculate = QPushButton("2. Calculer la Régression")
        self.btn_calculate.setEnabled(False) # Désactivé au début
        controls_layout.addWidget(self.btn_calculate)
        
        # 4. Zone de Résultats
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setObjectName("result_display")
        self.result_display.setMinimumHeight(100)
        controls_layout.addWidget(QLabel("Résultats du modèle :"))
        controls_layout.addWidget(self.result_display)
        controls_layout.addStretch()
        
        # --- Colonne de droite (Graphique) ---
        self.plot_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.plot_canvas.axes.set_title("Nuage de points et Droite de Régression")
        
        # Assemblage final
        left_widget = QWidget()
        left_widget.setLayout(controls_layout)
        left_widget.setMaximumWidth(400) # Limiter la taille de la colonne de contrôle
        
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.plot_canvas)

        # --- Connexions ---
        self.btn_load_csv.clicked.connect(self.on_load_csv_click)
        self.btn_calculate.clicked.connect(self.on_calculate_click)
        
    def on_load_csv_click(self):
        """
        Ouvre une boîte de dialogue pour choisir un fichier CSV.
        """
        # Note: data/donnees_regression.csv
        file_path, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier CSV", "data/", "Fichiers CSV (*.csv)")
        
        if not file_path:
            return # L'utilisateur a annulé

        df, erreur = charger_donnees_csv(file_path)
        
        if erreur:
            self.lbl_file_status.setText(erreur)
            self.lbl_file_status.setStyleSheet("color: #FF6B6B;")
            self.dataframe = None
            self.btn_calculate.setEnabled(False)
            self.combo_x.clear()
            self.combo_y.clear()
        else:
            self.dataframe = df
            self.lbl_file_status.setText(f"Fichier chargé : {file_path.split('/')[-1]}")
            self.lbl_file_status.setStyleSheet("color: #6BFF6B;")
            
            # Remplir les ComboBox avec les noms de colonnes
            columns = list(self.dataframe.columns)
            self.combo_x.clear()
            self.combo_y.clear()
            self.combo_x.addItems(columns)
            self.combo_y.addItems(columns)
            
            # Tenter de pré-sélectionner 'x' et 'y'
            if 'x' in columns:
                self.combo_x.setCurrentText('x')
            if 'y' in columns:
                self.combo_y.setCurrentText('y')
            
            self.btn_calculate.setEnabled(True)
            self.result_display.clear()
            self.plot_canvas.axes.clear()
            self.plot_canvas.axes.set_title("Chargez les données et cliquez sur 'Calculer'")
            self.plot_canvas.canvas.draw()

    def on_calculate_click(self):
        """
        Exécute la régression et affiche le graphique.
        """
        if self.dataframe is None:
            self.result_display.setText("Veuillez d'abord charger un fichier CSV.")
            return

        col_x_name = self.combo_x.currentText()
        col_y_name = self.combo_y.currentText()
        
        if not col_x_name or not col_y_name:
            self.result_display.setText("Veuillez sélectionner les colonnes X et Y.")
            return

        x_data = self.dataframe[col_x_name]
        y_data = self.dataframe[col_y_name]

        resultats, erreur = calculer_regression(x_data, y_data)
        
        if erreur:
            self.result_display.setStyleSheet("color: #FF6B6B;")
            self.result_display.setText(erreur)
        else:
            # Afficher les résultats textuels
            self.result_display.setStyleSheet("color: #6BFF6B;")
            result_str = f"Équation de la droite :\n{resultats['equation']}\n\n"
            result_str += f"Pente (m) : {resultats['pente']:.4f}\n"
            result_str += f"Ordonnée (b) : {resultats['ordonnee_origine']:.4f}\n"
            result_str += f"Score R² : {resultats['r_carre']:.4f}\n"
            self.result_display.setText(result_str)
            
            # Afficher le graphique
            self.plot_canvas.axes.clear() # Effacer l'ancien graphique
            self.plot_canvas.axes.scatter(x_data, y_data, label="Données réelles") # Nuage de points
            
            # Calculer la ligne de régression
            x_line = pd.Series([x_data.min(), x_data.max()])
            y_line = resultats['pente'] * x_line + resultats['ordonnee_origine']
            
            self.plot_canvas.axes.plot(x_line, y_line, color='red', label=f"Régression ({resultats['equation']})")
            
            self.plot_canvas.axes.set_title("Régression Linéaire")
            self.plot_canvas.axes.set_xlabel(col_x_name)
            self.plot_canvas.axes.set_ylabel(col_y_name)
            self.plot_canvas.axes.legend()
            self.plot_canvas.axes.grid(True, linestyle='--', alpha=0.6)
            self.plot_canvas.fig.tight_layout() # Optimise la mise en page
            self.plot_canvas.canvas.draw() # Redessiner le canevas