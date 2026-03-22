import pgzrun
# Only for class reference
# from pgzero.actor import Actor


raumschiff = Actor("raumschiff_gruen.png")
meteorit = Actor("meteorit.png")
laser = Actor("laser_ohne_strahl.png")


raumschiff.x=200
raumschiff.y=100

meteorit.x=400
meteorit.y=100

laser.x=400
laser.y=300


def draw():
    screen.blit("sterne.png",(0,0))
    raumschiff.draw()
    meteorit.draw()
    laser.draw()

def on_key_down():
    raumschiff.x = 700
    raumschiff.y = 200
    raumschiff.angle=90

def on_mouse_down(pos):
    raumschiff.x = pos[0]
    raumschiff.y = pos[1]

pgzrun.go()