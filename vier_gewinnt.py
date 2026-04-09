import pgzrun

# --- Konstanten ---
SPALTEN = 7
ZEILEN = 6
FELD_GROESSE = 80

WIDTH = SPALTEN * FELD_GROESSE
HEIGHT = ZEILEN * FELD_GROESSE
TITLE = "Vier Gewinnt - OOP Edition"

# Farben (RGB)
FARBE_LEER = (200, 200, 200)       # Hellgrau für leere Löcher
FARBE_SPIELER1 = (255, 50, 50)     # Rot
FARBE_SPIELER2 = (255, 255, 50)    # Gelb
FARBE_HINTERGRUND = (30, 100, 200) # Blaues Brett

# --- Klassen ---

class Spielstein:
    """Repräsentiert einen einzelnen eingeworfenen Spielstein."""
    def __init__(self, zeile, spalte, spieler):
        self.zeile = zeile
        self.spalte = spalte
        self.spieler = spieler
        
        # Berechne die Pixel-Koordinaten für die Bildschirmmitte des Feldes
        self.x = self.spalte * FELD_GROESSE + (FELD_GROESSE // 2)
        self.y = self.zeile * FELD_GROESSE + (FELD_GROESSE // 2)
        
        # Farbe basierend auf dem Spieler festlegen
        if self.spieler == 1:
            self.farbe = FARBE_SPIELER1
        else:
            self.farbe = FARBE_SPIELER2

    def zeichnen(self):
        """Zeichnet den Spielstein auf den Bildschirm."""
        radius = (FELD_GROESSE // 2) - 5
        screen.draw.filled_circle((self.x, self.y), radius, self.farbe)


class Spielfeld:
    """Verwaltet das Raster, die Spielsteine und die Spielregeln."""
    def __init__(self):
        # 2D-Liste (Array) für die Logik: 0 = Leer, 1 = Spieler 1, 2 = Spieler 2
        self.raster = [[0 for _ in range(SPALTEN)] for _ in range(ZEILEN)]
        # Liste für die Objekte, die gezeichnet werden sollen
        self.steine = []

    def einwerfen(self, spalte, spieler):
        """Sucht den tiefsten freien Platz in der Spalte und wirft einen Stein ein."""
        # Wir durchlaufen die Zeilen von unten (ZEILEN-1) nach oben (0)
        for zeile in range(ZEILEN - 1, -1, -1):
            if self.raster[zeile][spalte] == 0:
                # Logik aktualisieren
                self.raster[zeile][spalte] = spieler
                # Neues Objekt erstellen und speichern
                neuer_stein = Spielstein(zeile, spalte, spieler)
                self.steine.append(neuer_stein)
                return True # Erfolgreich eingeworfen
        return False # Spalte war voll

    def zeichnen(self):
        """Zeichnet das blaue Brett, die leeren Löcher und dann alle Steine."""
        screen.fill(FARBE_HINTERGRUND)
        
        # 1. Leere Löcher zeichnen
        for zeile in range(ZEILEN):
            for spalte in range(SPALTEN):
                x = spalte * FELD_GROESSE + (FELD_GROESSE // 2)
                y = zeile * FELD_GROESSE + (FELD_GROESSE // 2)
                radius = (FELD_GROESSE // 2) - 5
                screen.draw.filled_circle((x, y), radius, FARBE_LEER)
                
        # 2. Eingeworfene Steine zeichnen
        for stein in self.steine:
            stein.zeichnen()

    def pruefe_sieg(self, spieler):
        """Prüft, ob der übergebene Spieler 4 in einer Reihe hat."""
        # Horizontal prüfen
        for z in range(ZEILEN):
            for s in range(SPALTEN - 3):
                if self.raster[z][s] == spieler and self.raster[z][s+1] == spieler and self.raster[z][s+2] == spieler and self.raster[z][s+3] == spieler:
                    return True
                    
        # Vertikal prüfen
        for z in range(ZEILEN - 3):
            for s in range(SPALTEN):
                if self.raster[z][s] == spieler and self.raster[z+1][s] == spieler and self.raster[z+2][s] == spieler and self.raster[z+3][s] == spieler:
                    return True
                    
        # Diagonal (nach unten rechts \ )
        for z in range(ZEILEN - 3):
            for s in range(SPALTEN - 3):
                if self.raster[z][s] == spieler and self.raster[z+1][s+1] == spieler and self.raster[z+2][s+2] == spieler and self.raster[z+3][s+3] == spieler:
                    return True
                    
        # Diagonal (nach oben rechts / )
        for z in range(3, ZEILEN):
            for s in range(SPALTEN - 3):
                if self.raster[z][s] == spieler and self.raster[z-1][s+1] == spieler and self.raster[z-2][s+2] == spieler and self.raster[z-3][s+3] == spieler:
                    return True
                    
        return False

# --- Globale Spielsteuerung ---

brett = Spielfeld()
aktiver_spieler = 1
spiel_vorbei = False

def draw():
    """Pygame Zero Standard-Funktion zum Zeichnen des Bildschirms."""
    brett.zeichnen()
    
    if spiel_vorbei:
        gewinner_farbe = "red" if aktiver_spieler == 1 else "yellow"
        screen.draw.text(f"SPIELER {aktiver_spieler} GEWINNT!", 
                         center=(WIDTH//2, HEIGHT//2), 
                         fontsize=60, 
                         color=gewinner_farbe, 
                         shadow=(2,2),
                         owidth=1, ocolor="black")

def on_mouse_down(pos):
    """Pygame Zero Standard-Funktion für Mausklicks."""
    global aktiver_spieler, spiel_vorbei
    
    if spiel_vorbei:
        return # Nichts tun, wenn das Spiel zu Ende ist
    
    x, y = pos
    # Berechne, in welche Spalte geklickt wurde (0 bis 6)
    geklickte_spalte = x // FELD_GROESSE
    
    # Versuche den Stein einzuwerfen
    if brett.einwerfen(geklickte_spalte, aktiver_spieler):
        # Wenn erfolgreich, prüfe auf Sieg
        if brett.pruefe_sieg(aktiver_spieler):
            spiel_vorbei = True
        else:
            # Spieler wechseln (1 wird 2, 2 wird 1)
            aktiver_spieler = 2 if aktiver_spieler == 1 else 1

# Startet das Spiel (wichtig für IDEs wie Thonny)
pgzrun.go()