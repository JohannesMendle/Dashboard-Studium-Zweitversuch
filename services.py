from datetime import date
from domain import Studiengang, KursStatus

# Service-Klasse "Fortschritt" definieren
class Fortschritt:
    def __init__(self, studiengang: Studiengang):
        self.studiengang = studiengang

    # Berechnen der verdienten ECTS
    def berechne_verdiente_ects(self) -> int:
        erfolgreich = [KursStatus.BESTANDEN, KursStatus.ANERKANNT]
        verdient = sum(k.ects for k in self.studiengang.kurse if k.status in erfolgreich)
        return int(verdient)

    # Berechnen der ECTS, die zum heutigen Datum verdient sein sollten
    def berechne_soll_ects_heute(self) -> int:
        jetzt = date.today()
        gesamtdauer_tage = (self.studiengang.geplantes_enddatum - self.studiengang.startdatum).days
        tage_seit_start = (jetzt - self.studiengang.startdatum).days

        if tage_seit_start < 0:
            return 0
        elif tage_seit_start > gesamtdauer_tage:
            return self.studiengang.ects_gesamt
        else:
            fortschritt_zeit_faktor = tage_seit_start / gesamtdauer_tage
            return int(self.studiengang.ects_gesamt * fortschritt_zeit_faktor)

    # Berechnen der Differenz zwischen verdienten und Soll-ECTS
    def berechne_differenz_zum_soll(self) -> float:
        return float(self.berechne_verdiente_ects() - self.berechne_soll_ects_heute())

    # Berechnen des erlangten Fortschritts in Prozent
    def berechne_fortschritt_prozent(self) -> float:
        if self.studiengang.ects_gesamt == 0:
            return 0.0
        return (self.berechne_verdiente_ects() / self.studiengang.ects_gesamt) * 100.0

    # Berechnen des aktuellen Semesters
    def berechne_semester(self) -> int:
        jetzt = date.today()
        tage_vergangen = (jetzt - self.studiengang.startdatum).days
        if tage_vergangen < 0:
            return 0
        return (tage_vergangen // 182) + 1

# Service-Klasse "Notendurchschnitt" definieren
class Notendurchschnitt:
    def __init__(self, studiengang: Studiengang):
        self.studiengang = studiengang

    # Berechnen des gesamten Notensurchschnitts
    def berechne_notendurchschnitt(self) -> float:
        erfolgreich = [KursStatus.BESTANDEN, KursStatus.ANERKANNT]
        noten = [
            k.pruefungsleistung.note
            for k in self.studiengang.kurse
            if k.status in erfolgreich and k.pruefungsleistung and k.pruefungsleistung.note > 0
        ]
        if not noten:
            return 0.0
        return float(sum(noten) / len(noten))