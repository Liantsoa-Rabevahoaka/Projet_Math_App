# Fichier : Projet_Math_App/main.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# --- Thème Moderne (QSS) ---
# C'est ici que nous définissons le look "moderne et élégant" (NB1)
# C'est un mini-CSS pour les applications Qt.
DARK_THEME_QSS = """
QWidget {
    background-color: #2E2E2E;
    color: #F0F0F0;
    font-family: Arial, sans-serif;
    font-size: 11pt;
}
QTabWidget::pane {
    border-top: 2px solid #3A3A3A;
}
QTabBar::tab {
    background: #454545;
    color: #E0E0E0;
    padding: 10px 20px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
QTabBar::tab:selected {
    background: #0078D7; /* Bleu moderne pour l'onglet actif */
    color: #FFFFFF;
    font-weight: bold;
}
QTabBar::tab:!selected:hover {
    background: #5A5A5A;
}
QPushButton {
    background-color: #0078D7;
    color: #FFFFFF;
    border: none;
    padding: 10px 15px;
    border-radius: 4px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #005A9E;
}
QPushButton:pressed {
    background-color: #003A6A;
}
QLineEdit, QTextEdit {
    background-color: #3A3A3A;
    color: #F0F0F0;
    border: 1px solid #5A5A5A;
    border-radius: 4px;
    padding: 5px;
}
QLineEdit:focus, QTextEdit:focus {
    border-color: #0078D7;
}
QLabel {
    color: #E0E0E0;
}
QComboBox {
    background-color: #3A3A3A;
    border: 1px solid #5A5A5A;
    border-radius: 4px;
    padding: 5px;
}
QComboBox::drop-down {
    border: none;
}
QComboBox::down-arrow {
    /* (Vous pouvez ajouter une image d'icône flèche ici) */
}
QTextEdit#result_display {
    font-family: "Courier New", monospace;
    font-size: 10pt;
    background-color: #252525;
}
QGridLayout {
    margin: 0;
    padding: 0;
}
"""

# --- Importation de nos futurs onglets ---
# Ces fichiers n'existent pas encore, mais nous les coderons juste après.
# Mettez-les en commentaire pour l'instant si vous voulez tester.
from ui.ui_tab_systeme import TabSysteme
from ui.ui_tab_prog_lin import TabProgLin
from ui.ui_tab_regression import TabRegression
from ui.ui_tab_markov import TabMarkov


class MainWindow(QMainWindow):
    """
    Fenêtre principale de l'application.
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Projet de Modélisation Mathématique")
        self.setGeometry(100, 100, 900, 700) # (x, y, largeur, hauteur)

        # 1. Créer le conteneur d'onglets
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(True) # Permet de réorganiser les onglets
        
        # 2. Créer et ajouter chaque onglet
        self.tab_systeme = TabSysteme()
        self.tab_prog_lin = TabProgLin()
        self.tab_regression = TabRegression()
        self.tab_markov = TabMarkov()
        
        self.tabs.addTab(self.tab_systeme, "Système Linéaire")
        self.tabs.addTab(self.tab_prog_lin, "Programmation Linéaire")
        self.tabs.addTab(self.tab_regression, "Régression Linéaire")
        self.tabs.addTab(self.tab_markov, "Chaîne de Markov")
        
        # 3. Définir le widget central de la fenêtre
        self.setCentralWidget(self.tabs)


def main():
    app = QApplication(sys.argv)
    
    # Appliquer le style moderne !
    app.setStyleSheet(DARK_THEME_QSS)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()