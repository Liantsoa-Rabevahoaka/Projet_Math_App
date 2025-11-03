# Fichier : Projet_Math_App/ui/ui_helpers.py

import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

# Assure que Matplotlib utilise le backend QtAgg
matplotlib.use('QtAgg')

class MplCanvas(QWidget):
    """
    Widget PySide6 pour intégrer un canevas Matplotlib.
    C'est la "toile" sur laquelle nous allons dessiner nos graphiques.
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(MplCanvas, self).__init__(parent)
        
        # 1. Créer la figure Matplotlib
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        # 2. Créer l'objet "axes" (la zone de traçage)
        self.axes = self.fig.add_subplot(111)
        
        # 3. Créer le canevas PySide6 qui affiche la figure
        self.canvas = FigureCanvas(self.fig)
        
        # 4. Définir une politique de taille pour que le widget s'adapte
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Expanding)
        self.canvas.updateGeometry()
        
        # 5. Mettre le canevas dans un layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)