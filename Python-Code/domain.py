from datetime import date
from typing import List, Optional

# Domain-Klasse "KursStatus" definieren
class KursStatus:
    def __init__(self, name: str, beschreibung: Optional[str] = None):
        self.name = name
        self.beschreibung = beschreibung

    @property
    def value(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"KursStatus('{self.name}')"

KursStatus.BESTANDEN = KursStatus("bestanden", "Kurs wurde erfolgreich absolviert")
KursStatus.ANERKANNT = KursStatus("anerkannt", "Kurs wurde von anderer Institution anerkannt")
KursStatus.BELEGT = KursStatus("belegt", "Kurs ist aktuell belegt")
KursStatus.OFFEN = KursStatus("offen", "Kurs steht noch aus")

# Domain-Klasse "Kategorie" definieren
class Kategorie:
    def __init__(self, name: str, beschreibung: Optional[str] = None):
        self.name = name
        self.beschreibung = beschreibung

    def __repr__(self) -> str:
        return f"Kategorie('{self.name}')"

    def __eq__(self, other) -> bool:
        if isinstance(other, Kategorie):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return False

    def __hash__(self) -> int:
        return hash(self.name)

# Domain-Klasse "Pruefungsleistung" definieren
class Pruefungsleistung:
    def __init__(self, note: float):
        self.note = note

# Domain-Klasse "Kurse" definieren
class Kurse:
    def __init__(
        self,
        kursname: str,
        status: KursStatus,
        ects: float,
        kategorie: Kategorie,
        pruefungsleistung: Optional[Pruefungsleistung] = None
    ):
        self.kursname = kursname
        self.status = status
        self.ects = ects
        self.kategorie = kategorie
        self.pruefungsleistung = pruefungsleistung

# Domain-Klasse "Studiengang" definieren
class Studiengang:
    def __init__(
        self,
        startdatum: date,
        geplantes_enddatum: date,
        ects_gesamt: int,
        kurse: Optional[List[Kurse]] = None
    ):
        self.startdatum = startdatum
        self.geplantes_enddatum = geplantes_enddatum
        self.ects_gesamt = ects_gesamt
        self.kurse = kurse if kurse is not None else []