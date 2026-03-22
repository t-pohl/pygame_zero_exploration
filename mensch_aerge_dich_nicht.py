import pgzrun
import random
import math

# --- KONSTANTEN UND EINSTELLUNGEN ---
WIDTH = 600
HEIGHT = 700
CELL_SIZE = 50
OFFSET = 25 # Um die Mitte einer Zelle zu treffen

# Farben (RGB)
FARBEN = {
    "ROT": (220, 50, 50),
    "BLAU": (50, 50, 220),
    "GELB": (220, 220, 50),
    "GRUEN": (50, 220, 50),
    "WEISS": (255, 255, 255),
    "SCHWARZ": (0, 0, 0)
}

# Koordinaten der 40 Lauffelder im 11x11 Raster
LAUFFELDER = [
    (0,4), (1,4), (2,4), (3,4), (4,4), (4,3), (4,2), (4,1), (4,0), (5,0),
    (6,0), (6,1), (6,2), (6,3), (6,4), (7,4), (8,4), (9,4), (10,4), (10,5),
    (10,6), (9,6), (8,6), (7,6), (6,6), (6,7), (6,8), (6,9), (6,10), (5,10),
    (4,10), (4,9), (4,8), (4,7), (4,6), (3,6), (2,6), (1,6), (0,6), (0,5)
]

# Startbereiche (X, Y) im Raster für jede Farbe
START_FELDER = {
    "ROT": [(0,0), (1,0), (0,1), (1,1)],
    "BLAU": [(9,0), (10,0), (9,1), (10,1)],
    "GELB": [(9,9), (10,9), (9,10), (10,10)],
    "GRUEN": [(0,9), (1,9), (0,10), (1,10)]
}

# Koordinaten der 4 Zielfelder (Häuschen) für jede Farbe
ZIEL_FELDER = {
    "ROT": [(1,5), (2,5), (3,5), (4,5)],
    "BLAU": [(5,1), (5,2), (5,3), (5,4)],
    "GELB": [(9,5), (8,5), (7,5), (6,5)],
    "GRUEN": [(5,9), (5,8), (5,7), (5,6)]
}

# Einstiegspunkte auf dem Lauffeld (Index in der LAUFFELDER Liste)
START_INDEX = {"ROT": 0, "BLAU": 10, "GELB": 20, "GRUEN": 30}


# --- KLASSEN ---

class Wuerfel:
    def __init__(self):
        self.wert = 6
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.ist_am_rollen = False  # Speichert, ob die Animation gerade läuft
        
    def rollen(self):
        self.wert = random.randint(1, 6)
        
    def zeichnen(self):
        rect = Rect((self.x - 20, self.y - 20), (40, 40))
        screen.draw.filled_rect(rect, FARBEN["WEISS"])
        screen.draw.rect(rect, FARBEN["SCHWARZ"])
        screen.draw.text(str(self.wert), center=(self.x, self.y), color=FARBEN["SCHWARZ"], fontsize=30)

class Spielfigur:
    def __init__(self, farbe, id):
        self.farbe = farbe
        self.id = id
        self.status = "START" # "START", "LAUFFELD", "ZIEL"
        self.position = -1 
        self.start_x = START_FELDER[farbe][id][0]
        self.start_y = START_FELDER[farbe][id][1]
        
        # Gedächtnis für das Ziel
        self.schritte = 0 
        self.ziel_position = -1 # Index 0 bis 3 im Häuschen
        
    def zeichnen(self):
        if self.status == "START":
            px = self.start_x * CELL_SIZE + OFFSET
            py = self.start_y * CELL_SIZE + OFFSET
        elif self.status == "LAUFFELD":
            px = LAUFFELDER[self.position][0] * CELL_SIZE + OFFSET
            py = LAUFFELDER[self.position][1] * CELL_SIZE + OFFSET
        elif self.status == "ZIEL": # Zeichnen im Häuschen
            zx, zy = ZIEL_FELDER[self.farbe][self.ziel_position]
            px = zx * CELL_SIZE + OFFSET
            py = zy * CELL_SIZE + OFFSET
            
        screen.draw.filled_circle((px, py), 15, FARBEN[self.farbe])
        screen.draw.circle((px, py), 15, FARBEN["SCHWARZ"])

class Spieler:
    def __init__(self, farbe):
        self.farbe = farbe
        self.start_index = START_INDEX[farbe]
        # Erstellt genau 4 Figuren für diesen Spieler
        self.figuren = [Spielfigur(farbe, i) for i in range(4)]

class Spiel:
    def __init__(self):
        self.spieler_liste = [Spieler("ROT"), Spieler("BLAU"), Spieler("GELB"), Spieler("GRUEN")]
        self.wuerfel = Wuerfel()
        self.aktueller_spieler_idx = 0
        self.gewuerfelt = False
        self.wuerfe_uebrig = 3 # Zu Beginn des Spiels hat Rot direkt 3 Versuche
        
    def get_aktueller_spieler(self):
        return self.spieler_liste[self.aktueller_spieler_idx]
        
    def keine_figur_auf_dem_brett(self):
        # Prüft, ob der aktuelle Spieler alle Figuren im Haus hat
        aktueller_spieler = self.get_aktueller_spieler()
        for figur in aktueller_spieler.figuren:
            if figur.status == "LAUFFELD":
                return False
        return True
        
    def naechster_spieler(self):
        self.aktueller_spieler_idx = (self.aktueller_spieler_idx + 1) % 4
        self.gewuerfelt = False
        
        # Überprüfen, wie oft der neue Spieler würfeln darf
        if self.keine_figur_auf_dem_brett():
            self.wuerfe_uebrig = 3
        else:
            self.wuerfe_uebrig = 1
        
    def figur_bewegen(self, figur):
        aktueller_spieler = self.get_aktueller_spieler()
        
        # ZWANGSZÜGE BEI EINER 6 ÜBERPRÜFEN ---
        if self.wuerfel.wert == 6:
            # Prüfen, ob es Figuren im Start gibt
            hat_start_figuren = any(f.status == "START" for f in aktueller_spieler.figuren)
            
            # Prüfen, ob das eigene Startfeld durch eine eigene Figur blockiert ist
            start_idx = START_INDEX[aktueller_spieler.farbe]
            start_blockiert = any(f.status == "LAUFFELD" and f.position == start_idx for f in aktueller_spieler.figuren)
            
            # Zwang 1: Herausziehen! (Wenn Figuren im Start sind und das Startfeld frei ist)
            if hat_start_figuren and not start_blockiert and figur.status != "START":
                print("Zwangszug: Du musst eine Figur aus dem Haus ziehen!")
                return # Bricht die Funktion ab, der Spieler muss eine andere Figur anklicken
                
            # Zwang 2: Startfeld räumen! (Wenn eine eigene Figur den Start blockiert)
            # In diesem Fall MUSS die Figur bewegt werden, die auf dem Startfeld steht.
            if start_blockiert and figur.position != start_idx and figur.status != "START":
                print("Zwangszug: Du musst zuerst dein Startfeld räumen!")
                return # Bricht die Funktion ab
        # ----------------------------------------------

        # --- Die eigentliche Bewegungslogik ---
        if figur.status == "START" and self.wuerfel.wert == 6:
            figur.status = "LAUFFELD"
            figur.schritte = 0 # Schritte auf 0 setzen
            figur.position = START_INDEX[figur.farbe]
            self.gegner_schlagen(figur)
            
            # Bei einer 6 darf man nochmal!
            self.gewuerfelt = False 
            self.wuerfe_uebrig = 1
            
        elif figur.status == "LAUFFELD" or figur.status == "ZIEL":
            neue_schritte = figur.schritte + self.wuerfel.wert
            
            # Fall 1: Figur ist noch auf dem Lauffeld
            if neue_schritte < 40:
                figur.position = (START_INDEX[figur.farbe] + neue_schritte) % 40
                figur.schritte = neue_schritte
                self.gegner_schlagen(figur)
                
                # Überprüfen, ob eine 6 gewürfelt wurde
                if self.wuerfel.wert == 6:
                    self.gewuerfelt = False
                    self.wuerfe_uebrig = 1
                else:
                    self.naechster_spieler()
                
            # Fall 2: Figur geht ins Ziel oder bewegt sich im Ziel
            elif neue_schritte < 44:
                haus_index = neue_schritte - 40 # Wird zu 0, 1, 2 oder 3
                
                # Prüfen, ob das Feld im Häuschen schon besetzt ist
                feld_frei = True
                for f in aktueller_spieler.figuren:
                    if f.status == "ZIEL" and f.ziel_position == haus_index:
                        feld_frei = False
                        
                if feld_frei:
                    figur.status = "ZIEL"
                    figur.ziel_position = haus_index
                    figur.schritte = neue_schritte
                    
                    # Siegbedingung prüfen
                    if all(f.status == "ZIEL" for f in aktueller_spieler.figuren):
                        print(f"SPIELER {aktueller_spieler.farbe} HAT GEWONNEN!")
                        
                    # Auch im Häuschen gilt: Bei 6 darf man nochmal!
                    if self.wuerfel.wert == 6:
                        self.gewuerfelt = False
                        self.wuerfe_uebrig = 1
                    else:
                        self.naechster_spieler()
    
    def gegner_schlagen(self, aktive_figur):
        # Prüft alle Figuren aller Spieler
        for s in self.spieler_liste:
            if s.farbe != aktive_figur.farbe:
                for f in s.figuren:
                    # Wenn eine gegnerische Figur auf dem gleichen Lauffeld steht
                    if f.status == "LAUFFELD" and f.position == aktive_figur.position:
                        f.status = "START" # Gegner wird zurück auf den Start geschickt!
    
    def zug_moeglich(self):
        aktueller_spieler = self.get_aktueller_spieler()
        for figur in aktueller_spieler.figuren:
            if figur.status == "START" and self.wuerfel.wert == 6:
                return True
            if figur.status == "LAUFFELD" or figur.status == "ZIEL":
                neue_schritte = figur.schritte + self.wuerfel.wert
                if neue_schritte < 40:
                    return True # Zug auf dem Lauffeld
                elif neue_schritte < 44:
                    haus_index = neue_schritte - 40
                    # Prüfen, ob das Zielfeld frei ist
                    if not any(f.status == "ZIEL" and f.ziel_position == haus_index for f in aktueller_spieler.figuren):
                        return True
        return False


# --- HAUPTPROGRAMM (PYGAME ZERO) ---

mein_spiel = Spiel()

def draw():
    screen.fill((200, 200, 200)) # Grauer Hintergrund
    
    # Text: Wer ist am Zug?
    aktuelle_farbe = mein_spiel.get_aktueller_spieler().farbe
    screen.draw.text(f"Am Zug: {aktuelle_farbe}", topleft=(10, 610), color=FARBEN[aktuelle_farbe], fontsize=30)
    
    if not mein_spiel.gewuerfelt:
        text = f"Würfeln! (Versuche: {mein_spiel.wuerfe_uebrig})"
        screen.draw.text(text, topright=(WIDTH-10, 610), color=FARBEN["SCHWARZ"], fontsize=25)
    
    # Zeichne Lauffelder (als leere Kreise)
    for fx, fy in LAUFFELDER:
        px = fx * CELL_SIZE + OFFSET
        py = fy * CELL_SIZE + OFFSET
        screen.draw.circle((px, py), 20, FARBEN["SCHWARZ"])
        screen.draw.filled_circle((px, py), 18, FARBEN["WEISS"])
    
    # Zeichne Zielfelder (Häuschen) in der jeweiligen Spielerfarbe
    for farbe, felder in ZIEL_FELDER.items():
        for fx, fy in felder:
            px = fx * CELL_SIZE + OFFSET
            py = fy * CELL_SIZE + OFFSET
            # Farbig umrandet, innen weiß, damit man die Felder gut erkennt
            screen.draw.circle((px, py), 20, FARBEN[farbe])
            screen.draw.filled_circle((px, py), 18, FARBEN["WEISS"])
        
    # Zeichne Würfel
    mein_spiel.wuerfel.zeichnen()
    
    # Zeichne alle Figuren
    for spieler in mein_spiel.spieler_liste:
        for figur in spieler.figuren:
            figur.zeichnen()

def wuerfel_tick():
    # Wird während der Animation immer wieder aufgerufen und zeigt zufällige Zahlen
    mein_spiel.wuerfel.rollen()

def wuerfel_stop():
    # Stoppt das schnelle Wechseln
    clock.unschedule(wuerfel_tick)
    mein_spiel.wuerfel.ist_am_rollen = False
    
    # --- HIER passiert nun die eigentliche Spiellogik, die vorher im Klick war ---
    mein_spiel.wuerfe_uebrig -= 1
    
    if mein_spiel.zug_moeglich():
        mein_spiel.gewuerfelt = True # Ein Zug MUSS gemacht werden
    else:
        # Kein Zug möglich
        if mein_spiel.wuerfe_uebrig > 0:
            pass # Man darf nochmal klicken
        else:
            mein_spiel.gewuerfelt = True # Blockiert weiteres Klicken
            clock.schedule_unique(mein_spiel.naechster_spieler, 1.0)

def on_mouse_down(pos):
    # 1. Prüfen, ob der Würfel geklickt wurde
    wx, wy = mein_spiel.wuerfel.x, mein_spiel.wuerfel.y
    if abs(pos[0] - wx) < 20 and abs(pos[1] - wy) < 20:
        
        # Nur reagieren, wenn man würfeln darf UND der Würfel nicht schon rollt
        if not mein_spiel.gewuerfelt and not mein_spiel.wuerfel.ist_am_rollen:
            mein_spiel.wuerfel.ist_am_rollen = True
            
            # Starte die Animation: Ändere die Zahl alle 0.05 Sekunden
            clock.schedule_interval(wuerfel_tick, 0.05)
            # Beende die Animation nach 0.5 Sekunden
            clock.schedule_unique(wuerfel_stop, 0.5)
        return

    # 2. Prüfen, ob eine eigene Spielfigur geklickt wurde
    if mein_spiel.gewuerfelt:
        aktueller_spieler = mein_spiel.get_aktueller_spieler()
        for figur in aktueller_spieler.figuren:
            if figur.status == "START":
                px = figur.start_x * CELL_SIZE + OFFSET
                py = figur.start_y * CELL_SIZE + OFFSET
            elif figur.status == "LAUFFELD":
                px = LAUFFELDER[figur.position][0] * CELL_SIZE + OFFSET
                py = LAUFFELDER[figur.position][1] * CELL_SIZE + OFFSET
            elif figur.status == "ZIEL": # Anklicken im Ziel
                px = ZIEL_FELDER[figur.farbe][figur.ziel_position][0] * CELL_SIZE + OFFSET
                py = ZIEL_FELDER[figur.farbe][figur.ziel_position][1] * CELL_SIZE + OFFSET
                    
            dist = math.hypot(pos[0] - px, pos[1] - py)
            if dist < 15: 
                clock.unschedule(mein_spiel.naechster_spieler)
                mein_spiel.figur_bewegen(figur)
                break

pgzrun.go()
