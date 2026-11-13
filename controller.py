from datetime import date
from domain import Studiengang
from repository import KurseRepository
from services import Fortschritt, Notendurchschnitt
from views import Netzwerkstruktur, Ringdiagramm, Kennzahlen

# Controller-Klasse definieren
class DashboardController:
    def __init__(self, root_window):
        self.root_window = root_window
        self.repository = KurseRepository("kurse_cyber_security.json")
        self.studiengang = None
        self.fortschritt_service = None
        self.notendurchschnitt_service = None

    # Anfordern der Daten aus dem Repository
    def daten_aus_repository_anfordern(self) -> list:
        return self.repository.kursliste_generieren()

    # Übergeben der Daten an die Service-Klassen zur Berechnung
    def daten_an_services_uebergeben(self) -> None:
        kurse = self.daten_aus_repository_anfordern()
        self.studiengang = Studiengang(
            startdatum=date(2025, 3, 1),
            geplantes_enddatum=date(2028, 2, 28),
            ects_gesamt=180,
            kurse=kurse
        )
        self.fortschritt_service = Fortschritt(self.studiengang)
        self.notendurchschnitt_service = Notendurchschnitt(self.studiengang)

    # Abholen der berechneten Ergebnisse von den Service-Klassen
    def ergebnisse_von_services_anfordern(self) -> None:
        pass

    # Views von den View-Klassen anfordern
    def views_anfordern(self) -> None:
        self.daten_an_services_uebergeben()

        # Berechnungen
        verdiente_ects = self.fortschritt_service.berechne_verdiente_ects()
        soll_ects = self.fortschritt_service.berechne_soll_ects_heute()
        diff = self.fortschritt_service.berechne_differenz_zum_soll()
        prozent = self.fortschritt_service.berechne_fortschritt_prozent()
        semester = self.fortschritt_service.berechne_semester()
        notenschnitt = self.notendurchschnitt_service.berechne_notendurchschnitt()
        offene_ects = self.studiengang.ects_gesamt - verdiente_ects

        # View-Erzeugung
        netzwerk_view = Netzwerkstruktur(self.studiengang, self.root_window)
        canvas_map = netzwerk_view.netzwerk_darstellen()

        ring_view = Ringdiagramm(self.root_window)
        canvas_ist, canvas_soll = ring_view.ringdiagramm_darstellen(
            verdiente_ects, offene_ects, soll_ects, self.studiengang.ects_gesamt, diff
        )

        kennzahlen_view = Kennzahlen(self.root_window)
        f_titel, f_inhalte, n_titel, n_label = kennzahlen_view.kennzahlen_darstellen(
            semester, self.studiengang.startdatum, self.studiengang.geplantes_enddatum,
            verdiente_ects, self.studiengang.ects_gesamt, soll_ects, diff, prozent, notenschnitt
        )

        # Konfiguration Layout-Raster
        self.root_window.columnconfigure(0, weight=3, uniform="a")
        self.root_window.columnconfigure((1, 2), weight=1, uniform="a")
        self.root_window.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="a")
        self.root_window.rowconfigure(6, minsize=20)

        # Platzierung der Elemente im Raster
        canvas_map.grid(row=0, column=0, rowspan=4, sticky="nwes", padx=10, pady=10)
        f_titel.grid(row=0, column=1, sticky="s", pady=(10, 0))
        f_inhalte.grid(row=1, rowspan=2, column=1, sticky="n")
        n_titel.grid(row=1, column=2, sticky="n")
        n_label.grid(row=1, column=2)
        canvas_ist.grid(row=2, column=1, rowspan=2, sticky="nwes", padx=20, pady=20)
        canvas_soll.grid(row=2, column=2, rowspan=2, sticky="nwes", padx=20, pady=20)