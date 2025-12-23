from PySide6 import QtWidgets, QtCore
from movie import Movie, get_movies

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ciné Club")
        self.setMinimumWidth(400)
        self.setMinimumHeight(500)
        self.setup_ui()
        self.setup_css()
        self.setup_connections()
        self.populate_movies()

    def setup_ui(self):
        """Crée les widgets de l'interface."""
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Champ de saisie
        self.le_movieTitle = QtWidgets.QLineEdit()
        self.le_movieTitle.setPlaceholderText("Entrez le nom d'un film...")
        
        # Bouton Ajouter
        self.btn_addMovie = QtWidgets.QPushButton("Ajouter un film")
        
        # Liste des films
        self.lw_movies = QtWidgets.QListWidget()
        self.lw_movies.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        
        # Bouton Supprimer
        self.btn_removeMovies = QtWidgets.QPushButton("Supprimer le(s) film(s)")
        self.btn_removeMovies.setObjectName("btn_remove") 

        # Ajout au layout
        self.main_layout.addWidget(self.le_movieTitle)
        self.main_layout.addWidget(self.btn_addMovie)
        self.main_layout.addWidget(self.lw_movies)
        self.main_layout.addWidget(self.btn_removeMovies)

    def setup_css(self):
        """Applique le style QSS (Type CSS)."""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            
            QLineEdit {
                background-color: #313244;
                border: 2px solid #45475a;
                border-radius: 6px;
                padding: 10px;
                color: white;
            }
            
            QLineEdit:focus {
                border: 2px solid #89b4fa;
            }
            
            QPushButton {
                background-color: #89b4fa;
                color: #11111b;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #b4befe;
            }
            
            QPushButton:pressed {
                background-color: #74c7ec;
            }
            
            QListWidget {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 6px;
                outline: none;
            }
            
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #45475a;
            }
            
            QListWidget::item:selected {
                background-color: #45475a;
                color: #f38ba8;
                border-left: 3px solid #f38ba8;
            }

            QPushButton#btn_remove {
                background-color: #f38ba8;
                margin-top: 10px;
            }
            
            QPushButton#btn_remove:hover {
                background-color: #eba0ac;
            }
        """)

    def setup_connections(self):
        self.le_movieTitle.returnPressed.connect(self.add_movie)
        self.btn_addMovie.clicked.connect(self.add_movie)
        self.btn_removeMovies.clicked.connect(self.remove_movie)

    def populate_movies(self):
        self.lw_movies.clear()
        movies = get_movies()
        for movie in movies:
            lw_item = QtWidgets.QListWidgetItem(movie.title)
            lw_item.setData(QtCore.Qt.UserRole, movie)
            self.lw_movies.addItem(lw_item)

    def add_movie(self):
        movie_title = self.le_movieTitle.text().strip()
        if not movie_title:
            return

        movie = Movie(movie_title)
        resultat = movie.add_to_movies()
        
        if resultat:
            lw_item = QtWidgets.QListWidgetItem(movie.title)
            lw_item.setData(QtCore.Qt.UserRole, movie)
            self.lw_movies.addItem(lw_item)
            self.le_movieTitle.clear()
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Le film '{movie_title}' est déjà dans la liste.")

    def remove_movie(self):
        for selected_item in self.lw_movies.selectedItems():
            movie = selected_item.data(QtCore.Qt.UserRole)
            if movie:
                movie.remove_from_movies()
            self.lw_movies.takeItem(self.lw_movies.row(selected_item))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = App()
    win.show()
    app.exec()