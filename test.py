import turtle
import math
import time

map=[]
with open("map.txt") as readfile:
    line=readfile.readline().rstrip("\n")
    while line:
        map.append(line)
        line=readfile.readline().rstrip("\n")

screen=turtle.getscreen()
screen.colormode(255)
screenTk = screen.getcanvas().winfo_toplevel()
screenTk.attributes("-fullscreen", 1)

screen.tracer(0)

mapping=turtle.Turtle()
mapping.ht()

mapping.clear()
width=len(map[0])
height=len(map)
map_tile_size=20

x_adj=map_tile_size-(len(map[0])*map_tile_size)/2
y_adj=(len(map)*map_tile_size)/2-map_tile_size


for i in range(len(map[0]),len(map)):
    mapping.up()
    mapping.goto(map_tile_size*(i%width)+x_adj, -map_tile_size*(i//width)+y_adj)
    if map[i//width][i%width]=="#":
        mapping.goto(mapping.xcor()-map_tile_size/2, mapping.ycor()+map_tile_size/2)
        mapping.down()
        mapping.begin_fill()
        mapping.setx(mapping.xcor()+map_tile_size)
        mapping.sety(mapping.ycor()-map_tile_size)
        mapping.setx(mapping.xcor()-map_tile_size)
        mapping.sety(mapping.ycor()+map_tile_size)
        mapping.end_fill()

turtle.goto(-70, 50)

screen.update()
screen.mainloop()