import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QMessageBox, QDialog, QDialogButtonBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QDateTime, QSettings, QPropertyAnimation, QRect

class OknoDodawaniaTransakcji(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Dodawanie transakcji")
        self.setWindowModality(Qt.WindowModal)

        layout = QVBoxLayout()

        button_dodaj_wydatek = QPushButton("Dodać transakcję?")
        button_dodaj_zarobek = QPushButton("Dodać zarobek?")
        button_anuluj = QPushButton("Anuluj")

        layout.addWidget(button_dodaj_wydatek)
        layout.addWidget(button_dodaj_zarobek)
        layout.addWidget(button_anuluj)

        button_dodaj_wydatek.clicked.connect(self.accept_wydatek)
        button_dodaj_zarobek.clicked.connect(self.accept_zarobek)
        button_anuluj.clicked.connect(self.reject)

        self.setLayout(layout)

    def accept_wydatek(self):
        self.accept("wydatek")

    def accept_zarobek(self):
        self.accept("zarobek")
        
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
        self.etykieta_data = QLabel('Data (RRRR-MM-DD):', self)
        self.pole_data = QLineEdit(self)
        self.przycisk_dodaj_wydatek = QPushButton('Dodaj Wydatek', self)
        self.przycisk_dodaj_zarobek = QPushButton('Dodaj Zarobek', self)
        self.tekst_transakcje_wydatki = QTextEdit(self)
        self.tekst_transakcje_zarobki = QTextEdit(self)
        self.tekst_statystyki_kategorii = QTextEdit(self)

        # Dodanie stylu CSS do pól tekstowych
        css_style = "background-color: black; color: white; border: 1px solid white;"
        self.pole_kwota.setStyleSheet(css_style)
        self.pole_kategoria.setStyleSheet(css_style)
        self.pole_przedmiot.setStyleSheet(css_style)
        self.pole_data.setStyleSheet(css_style)
        self.tekst_transakcje_wydatki.setStyleSheet(css_style)
        self.tekst_transakcje_zarobki.setStyleSheet(css_style)
        self.tekst_statystyki_kategorii.setStyleSheet(css_style)

        # Ukrycie paska pośrodku aplikacji
        self.setStatusBar(None)

        # Ustawienia aplikacji
        self.ustawienia = QSettings("AplikacjaSledzeniaWydatkow", "Ustawienia")

        # Utworzenie układu dla przycisków
        uklad_przyciski = QVBoxLayout()
        uklad_przyciski.addWidget(self.etykieta_kwota)
        uklad_przyciski.addWidget(self.pole_kwota)
        uklad_przyciski.addWidget(self.etykieta_kategoria)
        uklad_przyciski.addWidget(self.pole_kategoria)
        uklad_przyciski.addWidget(self.etykieta_przedmiot)
        uklad_przyciski.addWidget(self.pole_przedmiot)
        uklad_przyciski.addWidget(self.etykieta_data)
        uklad_przyciski.addWidget(self.pole_data)
        uklad_przyciski.addWidget(self.przycisk_dodaj_wydatek)
        uklad_przyciski.addWidget(self.przycisk_dodaj_zarobek)

        # Zmniejszenie rozmiaru okienka
        self.setGeometry(100, 100, 800, 600)

        # Utworzenie układu dla transakcji i zarobków
        uklad_transakcje_zarobki = QHBoxLayout()
        uklad_transakcje_zarobki.addWidget(self.tekst_transakcje_wydatki)
        uklad_transakcje_zarobki.addWidget(self.tekst_transakcje_zarobki)

        # Utworzenie głównego układu
        uklad_glowny = QVBoxLayout()
        uklad_glowny.addLayout(uklad_przyciski)
        uklad_glowny.addLayout(uklad_transakcje_zarobki)

        # Dodanie tekstu statystyk do układu głównego
        uklad_glowny.addWidget(self.tekst_statystyki_kategorii) 

        # Utworzenie widgetu centralnego i przypisanie układu
        centralny_widget = QWidget(self)
        centralny_widget.setLayout(uklad_glowny)
        self.setCentralWidget(centralny_widget)

        # Ustawienia kolorów
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(0, 0, 0))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        self.setPalette(palette)

        # Dodanie stylu CSS do przycisków
        css_przycisk = "background-color: black; color: white; border: 1px solid white;"
        self.przycisk_dodaj_wydatek.setStyleSheet(css_przycisk)
        self.przycisk_dodaj_zarobek.setStyleSheet(css_przycisk)

        # Przypisanie funkcji obsługi zdarzeń
        self.przycisk_dodaj_wydatek.clicked.connect(self.dodaj_wydatek)
        self.przycisk_dodaj_zarobek.clicked.connect(self.dodaj_zarobek)
        self.pole_kwota.returnPressed.connect(self.przejdz_do_kolejnego_pola)
        self.pole_kategoria.returnPressed.connect(self.przejdz_do_kolejnego_pola)
        self.pole_przedmiot.returnPressed.connect(self.przejdz_do_kolejnego_pola)
        self.pole_data.returnPressed.connect(self.przejdz_do_kolejnego_pola)

        # Inicjalizacja tracker'ów
        self.tracker_wydatki = TrackerWydatkow()
        self.tracker_zarobki = TrackerZarobkow()

        # Inicjalizacja animacji
        self.animacja_wydatki = QPropertyAnimation(self.tekst_transakcje_wydatki, b"geometry")
        self.animacja_zarobki = QPropertyAnimation(self.tekst_transakcje_zarobki, b"geometry")

    def dodaj_wydatek(self):
        self.dodaj_transakcje(self.tracker_wydatki, self.tekst_transakcje_wydatki, True)

    def dodaj_zarobek(self):
        self.dodaj_transakcje(self.tracker_zarobki, self.tekst_transakcje_zarobki, False)

    def dodaj_transakcje(self, tracker, tekst_transakcje, is_wydatek):
        kwota_text = self.pole_kwota.text().replace(',', '.')
        try:
            kwota = float(kwota_text)
        except ValueError:
            # Obsługa błędu konwersji
            print("Błąd: Nie można przekonwertować kwoty na liczbę zmiennoprzecinkową.")
            return

        kategoria = self.pole_kategoria.text()
        przedmiot = self.pole_przedmiot.text()
        data_text = self.pole_data.text()

        # Pobieranie daty
        try:
            data = QDateTime.fromString(data_text, 'yyyy-MM-dd')
        except ValueError:
            print("Błąd: Nieprawidłowy format daty.")
            return

        transakcja = {
            'data': data,
            'kwota': kwota,
            'kategoria': kategoria,
            'przedmiot': przedmiot
        }
        tracker.dodaj_transakcje(transakcja)
        self.aktualizuj_wyswietlanie_transakcji(tekst_transakcje, tracker)  

        # Animacja
        self.przygotuj_animacje(is_wydatek)
        if is_wydatek:
            self.animacja_wydatki.start()
        else:
            self.animacja_zarobki.start()
    
        self.wyczysc_pola_wejsciowe()
    
    def przygotuj_animacje(self, is_wydatek):
        if is_wydatek:
            tracker = self.tracker_wydatki
            tekst_transakcje = self.tekst_transakcje_wydatki
        else:
            tracker = self.tracker_zarobki
            tekst_transakcje = self.tekst_transakcje_zarobki

        self.aktualizuj_wyswietlanie_transakcji(tekst_transakcje, tracker)
        self.aktualizuj_wyswietlanie_statystyk_kategorii()
        self.wyczysc_pola_wejsciowe()
        
    def przejdz_do_kolejnego_pola(self):
        # Znajdź bieżący widget w fokusie
        current_widget = self.focusWidget()

        # Znajdź indeks bieżącego widgetu wśród wszystkich potomków
        index = self.centralWidget().layout().indexOf(current_widget)

        # Przejdź do kolejnego widgetu w kolejności
        next_index = (index + 1) % self.centralWidget().layout().count()

        # Ustaw fokus na kolejnym widgecie, jeśli istnieje
        next_widget_item = self.centralWidget().layout().itemAt(next_index)
        if next_widget_item is not None:
            next_widget = next_widget_item.widget()
            if next_widget is not None:
                next_widget.setFocus()

                # Jeśli jest to ostatnie pole, wywołaj okno dialogowe z pytaniem
                if next_index == 0:
                    result = self.wyswietl_okno_dialogowe()

                    if result == "wydatek":
                        self.dodaj_wydatek()
                    elif result == "zarobek":
                        self.dodaj_zarobek()

                    return

    def wyswietl_okno_dialogowe(self):
        okno_dialogowe = OknoDodawaniaTransakcji(self)
        result = okno_dialogowe.exec_()

        if result == QDialog.Accepted:
            return okno_dialogowe.result()
        else:
            return None
            
    def aktualizuj_wyswietlanie_transakcji(self, tekst_transakcje, tracker):
        tekst_transakcje.clear()
        for transakcja in tracker.transakcje:
            sformatowana_data = transakcja['data'].toString(Qt.DefaultLocaleShortDate)
            sformatowana_godzina = transakcja['data'].toString("HH:mm")
            sformatowana_kwota = f"{transakcja['kwota']:.2f}"
            sformatowana_kategoria = transakcja['kategoria']
            sformatowany_przedmiot = transakcja['przedmiot']

            tekst_transakcji = f"{sformatowana_data} {sformatowana_godzina} - {sformatowana_kwota} ({sformatowana_kategoria}): {sformatowany_przedmiot}"
            tekst_transakcje.append(tekst_transakcji)

    def aktualizuj_wyswietlanie_statystyk_kategorii(self):
        self.tekst_statystyki_kategorii.clear()
        self.tekst_statystyki_kategorii.append("Statystyki Kategorii Wydatków:")
        for kategoria, suma_kwoty in self.tracker_wydatki.kategorie.items():
            self.tekst_statystyki_kategorii.append(f"{kategoria}: {suma_kwoty}")

        # Dodaj statystyki zarobków
        self.tekst_statystyki_kategorii.append("\nStatystyki Kategorii Zarobków:")
        for kategoria, suma_kwoty in self.tracker_zarobki.kategorie.items():
            self.tekst_statystyki_kategorii.append(f"{kategoria}: {suma_kwoty}")

    def wyczysc_pola_wejsciowe(self):
        self.pole_kwota.clear()
        self.pole_kategoria.clear()
        self.pole_przedmiot.clear()
        self.pole_data.clear()

class TrackerWydatkow:
    def __init__(self):
        self.transakcje = []
        self.kategorie = {}

    def dodaj_transakcje(self, transakcja):
        self.transakcje.append(transakcja)
        self.aktualizuj_statystyki_kategorii(transakcja['kategoria'], transakcja['kwota'])

    def aktualizuj_statystyki_kategorii(self, kategoria, kwota):
        if kategoria in self.kategorie:
            self.kategorie[kategoria] += kwota
        else:
            self.kategorie[kategoria] = kwota

class TrackerZarobkow(TrackerWydatkow):
    pass

if __name__ == '__main__':
    app = QApplication(sys.argv)

    okno = AplikacjaSledzeniaWydatkow()
    okno.setGeometry(100, 100, 1200, 600)
    okno.show()
    sys.exit(app.exec_())
