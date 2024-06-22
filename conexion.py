from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from connexion import Ui_MainWindow
import sys
import sqlite3


class ConnexionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.pushButton.clicked.connect(self.connexion)

    def create_table(self):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def connexion(self):
        username = self.ui.lineEdit_2.text()
        password = self.ui.lineEdit.text()

        if len(username) == 0 or len(password) == 0:
            QMessageBox.information(self, "Erreur de saisie", "Veuillez remplir tous les champs.")
        else:
            self.create_table()

            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            query = 'SELECT password FROM users WHERE username = ?'
            cur.execute(query, (username,))
            result_pass = cur.fetchone()

            if result_pass and result_pass[0] == password:
                QMessageBox.information(self, "Connexion réussie", "Connexion réussie !")
            else:
                QMessageBox.warning(self, "Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")

            conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    conn_app = ConnexionApp()
    sys.exit(app.exec_())
