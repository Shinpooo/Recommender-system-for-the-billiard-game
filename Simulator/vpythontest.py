from vpython import *
scene.range = 5
b = box()

drag = False
s = None # declare s to be used below

def down(evt):
    global drag, s
    loc = evt.pos
    print(loc)
    if -0.5 <= loc.x <= 0.5 and -0.5 <= loc.y <= 0.5:
    #s = sphere(pos=scene.mouse.pos,
    #    color=color.red,
    #    size=0.2*vec(1,1,1))
    #b.pos = scene.mouse.pos
        drag = True

def move():
    global drag, s 
    if drag: # mouse button is down
        b.pos = scene.mouse.pos

def up():
    global drag, s
    s.color = color.cyan
    drag = False

scene.bind("mousedown", down)

scene.bind("mousemove", move)

scene.bind("mouseup", up)