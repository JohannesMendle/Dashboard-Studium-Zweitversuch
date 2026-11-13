import json
from typing import List
from domain import Kurse, KursStatus, Kategorie, Pruefungsleistung

# Repository-Klasse definieren
class KurseRepository:
    def __init__(self, dateipfad: str):
        self.dateipfad = dateipfad

    # Generieren der Kursliste
    def kursliste_generieren(self) -> List[Kurse]:
        # try-except-Block, falls Daten nicht geladen werden können
        try:
            with open(self.dateipfad, "r", encoding="utf-8") as f:
                kurse_daten = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            kurse_daten = [
                {"kurs": "Demo Einführung", "status": "bestanden", "ects": 5.0, "note": 1.3, "kategorie": "IT"},
                {"kurs": "Demo Programmieren", "status": "bestanden", "ects": 6.0, "note": 1.7, "kategorie": "Organisatorisch"},
                {"kurs": "Demo Netzwerke", "status": "belegt", "ects": 5.0, "note": 0.0, "kategorie": "Cyber Security"},
                {"kurs": "Demo Recht", "status": "belegt", "ects": 5.0, "note": 0.0, "kategorie": "IT"}
            ]

        # Definieren der möglichen Status
        status_map = {
            "bestanden": KursStatus.BESTANDEN,
            "anerkannt": KursStatus.ANERKANNT,
            "belegt": KursStatus.BELEGT,
            "offen": KursStatus.OFFEN,
        }

        # Definieren der Kursliste
        kurs_liste = []
        for eintrag in kurse_daten:
            status_str = str(eintrag.get("status", "")).lower()
            status_obj = status_map.get(status_str, KursStatus.OFFEN)

            def _to_float(wert) -> float:
                if isinstance(wert, str):
                    wert = wert.replace(",", ".").strip()
                try:
                    return float(wert)
                except (ValueError, TypeError):
                    return 0.0

            note_val = _to_float(eintrag.get("note", 0.0))
            ects_val = _to_float(eintrag.get("ects", 0.0))

            leistung = Pruefungsleistung(note=note_val) if note_val > 0 else None
            kategorie_obj = Kategorie(name=eintrag.get("kategorie", "Allgemein"))

            kurs_obj = Kurse(
                kursname=eintrag.get("kurs", "Unbenannt"),
                status=status_obj,
                ects=ects_val,
                kategorie=kategorie_obj,
                pruefungsleistung=leistung
            )
            kurs_liste.append(kurs_obj)

        return kurs_liste