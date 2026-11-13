from tkinter import ttk
from datetime import date
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from domain import Studiengang
from matplotlib.lines import Line2D

# View-Klasse "Netzwerkstruktur" definieren
class Netzwerkstruktur:
    def __init__(self, studiengang: Studiengang, master):
        self.studiengang = studiengang
        self.master = master

    # View erzeugen
    def netzwerk_darstellen(self):
        G = nx.Graph()
        root = "Cyber Security"
        G.add_node(root, color="#2790D2", size=3000, s_color="#2c3e50")

        # Knotenfarben definieren
        status_farben_map = {
            "bestanden": "#2ecc71",
            "anerkannt": "#2ecc71",
            "belegt": "#f1c40f",
            "offen": "#bdc3c7"
        }

        # Knoten erzeugen
        for kurs in self.studiengang.kurse:
            node_color = status_farben_map.get(kurs.status.value, "#bdc3c7")
            G.add_node(kurs.kursname, color=node_color, category=kurs.kategorie)

        # Knotenränder erzeugen
        for kurs in self.studiengang.kurse:
            G.add_edge(root, kurs.kursname, weight=0.1)
            selbe_kat = [k.kursname for k in self.studiengang.kurse if k.kategorie == kurs.kategorie]
            for nachbar in selbe_kat:
                if nachbar != kurs.kursname:
                    G.add_edge(kurs.kursname, nachbar, weight=5.0)

        # Matplotlib-Figur und Achsen initialisieren
        fig, ax = plt.subplots(figsize=(12, 10), facecolor="none")
        # Knoten-Positionen berechnen
        pos = nx.spring_layout(G, k=1.5, weight="weight", iterations=100, seed=42)
        # Verbindungen des Graphen zeichnen
        nx.draw_networkx_edges(G, pos, alpha=0.1, edge_color="grey", ax=ax)

        # Knoten zeichnen
        for node in G.nodes:
            n_size = 3000 if node == root else 1200
            n_color = G.nodes[node].get("color", "#bdc3c7")
            nx.draw_networkx_nodes(
                G, pos,
                nodelist=[node],
                node_color=n_color,
                node_size=n_size,
                linewidths=0,
                edgecolors="none",
                ax=ax
            )

        nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)
        ax.set_axis_off()

        # Legende erstellen
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label=': Studiengang / Root', markerfacecolor='#2790D2', markersize=10),
            Line2D([0], [0], marker='o', color='w', label=': Bestanden / Anerkannt', markerfacecolor='#2ecc71', markersize=10),
            Line2D([0], [0], marker='o', color='w', label=': Belegt', markerfacecolor='#f1c40f', markersize=10),
            Line2D([0], [0], marker='o', color='w', label=': Offen', markerfacecolor='#bdc3c7', markersize=10)
        ]

        # Legende platzieren
        ax.legend(
            handles=legend_elements,
            loc='lower center',
            bbox_to_anchor=(0.5, -0.05),
            ncol=4,
            frameon=False,
            fontsize=9
        )

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        widget = canvas.get_tk_widget()
        widget.config(bg="#f0f0f0", highlightthickness=0)
        return widget

# View-Klasse "Ringdiagramm" definieren
class Ringdiagramm:
    def __init__(self, master):
        self.master = master

    def ringdiagramm_darstellen(self, verdiente_ects: float, offene_ects: float, ects_soll_heute: float, gesamt_ects_ziel: float, differenz_zum_soll: float):
        # Diagramm 1: IST-Stand erstellen
        hauptfarbe_ist = "#2ecc71" if differenz_zum_soll >= 0 else "#e74c3c"
        chart_daten = [verdiente_ects, max(0, offene_ects)]
        chart_farben = [hauptfarbe_ist, "#ffffff"]

        fig, ax = plt.subplots(figsize=(3, 3), dpi=100, facecolor="none")
        ax.pie(chart_daten, colors=chart_farben, startangle=90, counterclock=False,
               wedgeprops={'edgecolor': hauptfarbe_ist, 'linewidth': 1} if offene_ects > 0 else {})

        # Inneren Kreis hinzufügen, um Kreis in Donut umzuwandeln
        centre_circle = plt.Circle((0, 0), 0.70, fc="#f0f0f0")
        fig.gca().add_artist(centre_circle)
        ax.set_title("Aktueller Stand", fontdict={"fontsize": 10, "fontweight": "bold"})
        ax.axis('equal')
        plt.tight_layout()

        canvas_ist = FigureCanvasTkAgg(fig, master=self.master)
        widget_ist = canvas_ist.get_tk_widget()
        widget_ist.config(bg="#f0f0f0", highlightthickness=0)

        # Diagramm 2: SOLL-Zeitplan erstellen
        soll_offen = max(0, gesamt_ects_ziel - ects_soll_heute)
        chart_daten_soll = [ects_soll_heute, soll_offen]
        chart_farben_soll = ["#3498db", "#ffffff"]

        fig_soll, ax_soll = plt.subplots(figsize=(3, 3), dpi=100, facecolor="none")
        ax_soll.pie(chart_daten_soll, colors=chart_farben_soll, startangle=90, counterclock=False,
                    wedgeprops={'edgecolor': '#3498db', 'linewidth': 1})

        # Inneren Kreis hinzufügen, um Kreis in Donut umzuwandeln
        centre_circle_soll = plt.Circle((0, 0), 0.70, fc="#f0f0f0")
        fig_soll.gca().add_artist(centre_circle_soll)
        ax_soll.set_title("Soll-Zeitplan", fontdict={"fontsize": 10, "fontweight": "bold"})
        ax_soll.axis('equal')
        plt.tight_layout()

        canvas_soll = FigureCanvasTkAgg(fig_soll, master=self.master)
        widget_soll = canvas_soll.get_tk_widget()
        widget_soll.config(bg="#f0f0f0", highlightthickness=0)

        return widget_ist, widget_soll

# View-Klasse "Kennzahlen" definieren
class Kennzahlen:
    def __init__(self, master):
        self.master = master

    def kennzahlen_darstellen(self, semester, startdatum, geplantes_enddatum, verdiente_ects, gesamt_ects, ects_soll_heute, differenz_zum_soll, fortschritt_prozent, note_schnitt):
        # Datumsangaben ins Format TT.MM.JJJJ konvertieren
        jetzt = date.today()
        heute_str = jetzt.strftime("%d.%m.%Y")
        studienbeginn_str = startdatum.strftime("%d.%m.%Y")
        studienende_str = geplantes_enddatum.strftime("%d.%m.%Y")

        # Visuellen Status anhand des Soll-Abgleichs bestimmen
        status_symbol = "✅" if differenz_zum_soll >= 0 else "⚠️"
        semester_str = semester if semester != 0 else "Noch nicht gestartet"

        # Fortschritts-Textbox erstellen
        fortschritt_titel = ttk.Label(self.master, text="Fortschritt", font=("Arial", 12, "bold"))
        fortschritt_text = (
            f"Aktuelles Semester: {semester_str}\n"
            f"Studiumsbeginn: {studienbeginn_str}\n"
            f"Stand: {heute_str}\n"
            f"Geplantes Ende: {studienende_str}\n\n"
            f"Verdiente ECTS: {verdiente_ects} / {gesamt_ects}\n"
            f"Soll ECTS: {ects_soll_heute:.1f}\n"
            f"{status_symbol} ({differenz_zum_soll:+.1f} ECTS)\n"
            f"Fortschritt: {fortschritt_prozent:.1f} %"
        )
        fortschritt_inhalte = ttk.Label(self.master, text=fortschritt_text, justify="center", font=("Arial", 10))

        # Notendurchschnitt-Anzeige erstellen
        notendurchschnitt_titel = ttk.Label(self.master, text="Notenschnitt", font=("Arial", 12, "bold"))
        farbe = "#2ecc71" if 0 < note_schnitt <= 1.5 else "#e74c3c"
        notendurchschnitt_label = ttk.Label(self.master, text=f"{note_schnitt:.2f}", justify="center",
                                            font=("Arial", 36, "bold"), foreground=farbe)

        return fortschritt_titel, fortschritt_inhalte, notendurchschnitt_titel, notendurchschnitt_label