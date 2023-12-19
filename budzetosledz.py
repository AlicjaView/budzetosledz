import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTextEdit
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QDateTime, QSettings

class AplikacjaSledzeniaWydatkow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.inicjalizacja_interfejsu()

    def inicjalizacja_interfejsu(self):
        # Inicjalizacja komponentów GUI
        self.etykieta_kwota = QLabel('Kwota:', self)
        self.pole_kwota = QLineEdit(self)
        self.etykieta_kategoria = QLabel('Kategoria:', self)
        self.pole_kategoria = QLineEdit(self)
        self.etykieta_przedmiot = QLabel('Przedmiot:', self)
        self.pole_przedmiot = QLineEdit(self)
        self.przycisk_dodaj = QPushButton('Dodaj Transakcję', self)
        self.tekst_transakcje = QTextEdit(self)
        self.tekst_statystyki_kategorii = QTextEdit(self)

        # Ustawienia aplikacji
        self.ustawienia = QSettings("AplikacjaSledzeniaWydatkow", "Ustawienia")

        # Utworzenie głównego układu
        układ = QVBoxLayout()

        # Dodanie komponentów do układu
        układ.addWidget(self.etykieta_kwota)
        układ.addWidget(self.pole_kwota)
        układ.addWidget(self.etykieta_kategoria)
        układ.addWidget(self.pole_kategoria)
        układ.addWidget(self.etykieta_przedmiot)
        układ.addWidget(self.pole_przedmiot)
        układ.addWidget(self.przycisk_dodaj)
        układ.addWidget(self.tekst_transakcje)
        układ.addWidget(self.tekst_statystyki_kategorii)

        # Utworzenie widgetu centralnego i przypisanie układu
        centralny_widget = QWidget(self)
        centralny_widget.setLayout(układ)
        self.setCentralWidget(centralny_widget)

        # Ustawienia kolorów
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
        palette.setColor(QPalette.Button, QColor(0, 0, 0))
        palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))
        palette.setColor(QPalette.Base, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(0, 255, 0))
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)

        # Przypisanie funkcji obsługi zdarzeń
        self.przycisk_dodaj.clicked.connect(self.dodaj_transakcje)
        self.pole_kwota.returnPressed.connect(self.przejdz_do_kolejnego_pola)
        self.pole_kategoria.returnPressed.connect(self.przejdz_do_kolejnego_pola)
        self.pole_przedmiot.returnPressed.connect(self.przejdz_do_kolejnego_pola)

        # Inicjalizacja tracker'a wydatków
        self.tracker = TrackerWydatkow()

    def dodaj_transakcje(self):
        kwota_text = self.pole_kwota.text().replace(',', '.')
        try:
            kwota = float(kwota_text)
        except ValueError:
            # Obsługa błędu konwersji
            print("Błąd: Nie można przekonwertować kwoty na liczbę zmiennoprzecinkową.")
            return

        kategoria = self.pole_kategoria.text()
        przedmiot = self.pole_przedmiot.text()

        self.tracker.dodaj_transakcje(kwota, kategoria, przedmiot)
        self.aktualizuj_wyswietlanie_transakcji()
        self.wyczysc_pola_wejsciowe()

    def przejdz_do_kolejnego_pola(self):
        # Znajdź bieżący widget w fokusie
        current_widget = self.focusWidget()

        # Znajdź indeks bieżącego widgetu wśród wszystkich dzieci
        index = self.centralWidget().layout().indexOf(current_widget)

        # Przejdź do kolejnego widgetu w kolejności
        next_index = (index + 1) % self.centralWidget().layout().count()

        # Ustaw fokus na kolejnym widżecie
        next_widget = self.centralWidget().layout().itemAt(next_index).widget()
        next_widget.setFocus()

    def aktualizuj_wyswietlanie_transakcji(self):
        self.tekst_transakcje.clear()
        for transakcja in self.tracker.transakcje:
            sformatowana_data = transakcja['data'].toString(Qt.DefaultLocaleShortDate)
            sformatowana_godzina = transakcja['data'].toString("HH:mm")
            sformatowana_kwota = f"{transakcja['kwota']:.2f}"
            sformatowana_kategoria = transakcja['kategoria']
            sformatowany_przedmiot = transakcja['przedmiot']

            tekst_transakcji = f"{sformatowana_data} {sformatowana_godzina} - {sformatowana_kwota} ({sformatowana_kategoria}): {sformatowany_przedmiot}"
            self.tekst_transakcje.append(tekst_transakcji)

        self.aktualizuj_wyswietlanie_statystyk_kategorii()

    def aktualizuj_wyswietlanie_statystyk_kategorii(self):
        self.tekst_statystyki_kategorii.clear()
        self.tekst_statystyki_kategorii.append("Statystyki Kategorii:")
        for kategoria, suma_kwoty in self.tracker.kategorie.items():
            self.tekst_statystyki_kategorii.append(f"{kategoria}: {suma_kwoty}")

    def wyczysc_pola_wejsciowe(self):
        self.pole_kwota.clear()
        self.pole_kategoria.clear()
        self.pole_przedmiot.clear()

class TrackerWydatkow:
    def __init__(self):
        self.transakcje = []
        self.kategorie = {}

    def dodaj_transakcje(self, kwota, kategoria, przedmiot):
        transakcja = {
            'data': QDateTime.currentDateTime(),
            'kwota': kwota,
            'kategoria': kategoria,
            'przedmiot': przedmiot
        }
        self.transakcje.append(transakcja)
        self.aktualizuj_statystyki_kategorii(kategoria, kwota)

    def aktualizuj_statystyki_kategorii(self, kategoria, kwota):
        if kategoria in self.kategorie:
            self.kategorie[kategoria] += kwota
        else:
            self.kategorie[kategoria] = kwota

if __name__ == '__main__':
    app = QApplication(sys.argv)

    okno = AplikacjaSledzeniaWydatkow()
    okno.setGeometry(100, 100, 800, 600)
    okno.show()
    sys.exit(app.exec_())
