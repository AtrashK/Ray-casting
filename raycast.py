#import various libaries
import turtle
import time
import math
import pyautogui
pyautogui.FAILSAFE = False #allows cursor to go to corners of the screen

#setting up the screen, and it's properties, and hiding the cursor
screen=turtle.getscreen()
screen.colormode(255)
screen.bgcolor("black")
screenTk = screen.getcanvas().winfo_toplevel()
screenTk.attributes("-fullscreen", 1)
screenTk.config(cursor="none")

turtle.ht() #hides the og turtle

screen.tracer(0) # stops time

#setting up the player turtle
player=turtle.Turtle()
player.up()
player.ht()
player.setheading(30)

#setting up the test turtle (not in use)
test=turtle.Turtle()
test.ht()
test.up()

#setting up the rendering turtle
ray=turtle.Turtle()
ray.up()
ray.ht()
ray.color(0,0,255)
ray.pensize(10)

screen.update() #starts time

#setting up the variables for held keys
key_held_w = False
key_held_s = False
key_held_a = False
key_held_d = False

distance_array=[] #array containing the distances from the player to the wall
map=[] #it's in the name dawg

with open("map.txt") as readfile:
    line=readfile.readline().rstrip("\n")
    while line:
        map.append(line)
        line=readfile.readline().rstrip("\n")

#properties of the map
width=len(map[0])
height=len(map)
tile_size=50
map_left=-1*(width/2)*tile_size
map_top=(height/2)*tile_size

mapping=turtle.Turtle()
mapping.ht()
mapping.up()
mapping.color("white")
mapping.fillcolor("white")

player_sprite=turtle.Turtle()
player_sprite.up()
player_sprite.color("red")
player_sprite.shape("circle")
player_sprite.shapesize(0.3, 0.3)

screen.tracer(0) # stops time

for i in range((len(map))*len(map[1])):
    turtle.up()
    turtle.goto(tile_size*(i%width), -tile_size*(i//width))
    if map[i//width][i%width]=="#":
        turtle.goto(turtle.xcor()-tile_size/2, turtle.ycor()+tile_size/2)
        turtle.down()
        turtle.begin_fill()
        turtle.setx(turtle.xcor()+tile_size)
        turtle.sety(turtle.ycor()-tile_size)
        turtle.setx(turtle.xcor()-tile_size)
        turtle.sety(turtle.ycor()+tile_size)
        turtle.end_fill()

#variables needed in finding the spawn point
spawn_found=False
spawn_counter=0

#looking for the first non-wall grid, in the map, from the top left corner
while (spawn_found==False):
    if (map[spawn_counter//width][spawn_counter%width]!="#"):
        spawn_found=True
    else:
        spawn_counter+=1

#defining which row and col that is
row=spawn_counter//width
col=spawn_counter%width
starting_x=(col*tile_size)+map_left+(tile_size/2)
starting_y=map_top-(row*tile_size)-(tile_size/2)

player.goto(starting_x, starting_y) #player spawns here

#the function for the holding and release of the 4 movement keys
def press_w():
    global key_held_w
    key_held_w = True

def release_w():
    global key_held_w
    key_held_w = False

def press_s():
    global key_held_s
    key_held_s = True

def release_s():
    global key_held_s
    key_held_s = False

def press_a():
    global key_held_a
    key_held_a = True

def release_a():
    global key_held_a
    key_held_a = False

def press_d():
    global key_held_d
    key_held_d = True

def release_d():
    global key_held_d
    key_held_d = False

def is_wall(x, y): #function for checking if a point x,y is in a wall
    global height, width, map, tile_size, map_left, map_top #yes, ik, disgusting, cba to clean up

    col=int((x-map_left)/tile_size) #determing which col the point is in
    row=int((map_top-y)//tile_size) #determing which row the point is in

    if (row<0 or row>height-1 or col<0 or col>width-1): #if the point is outside the map
        return True
    else:
        if (map[row][col]=="#"): #or the point is a wall
            return True
        else:
            return False
    
def player_movement(): #function for player movement
    global key_held_w, key_held_s, key_held_a, key_held_d, moved #one day
    dir=math.radians(player.heading()) #changing the player's direction to radians, cuz pymath weird like that 
    fd_bd_x=2.5*math.cos(dir)
    fd_bd_y=2.5*math.sin(dir)
    lf_rt_x=2.5*math.cos(dir-(math.pi/2))
    lf_rt_y=2.5*math.sin(dir-(math.pi/2))

    if key_held_w and not is_wall(player.xcor()+fd_bd_x, player.ycor()+fd_bd_y): #if w held, and a wall aint infront
        player.forward(2.5)
    if key_held_s and not is_wall(player.xcor()-fd_bd_x, player.ycor()-fd_bd_y): #if s held, and a wall aint behind
        player.backward(2.5)

    if key_held_d and not is_wall(player.xcor()+lf_rt_x, player.ycor()+lf_rt_y): #if d held, and a wall aint to the right
        player.goto(player.xcor()+lf_rt_x, player.ycor()+lf_rt_y)
    if key_held_a and not is_wall(player.xcor()-lf_rt_x, player.ycor()-lf_rt_y): #if a held, and a wall aint to the right
        player.goto(player.xcor()-lf_rt_x, player.ycor()-lf_rt_y)

def casting_ray(num_rays, FOV, horror_mode): #function for calculating distances to a wall 
    global distance_array, tile_size #ignore this
    distance_array.clear() #emptys the distance array every frame
    for i in range(0, num_rays+1): #repeats for number of rays
        x=player.xcor() #starting x cor of the ray
        y=player.ycor() #starting y cor of the ray
        distance=0 #starting distance of the ray 
        dir=player.heading()+(FOV/2)-((FOV*i)/num_rays) #setting the direction of the ray
        dx=math.cos(math.radians(dir))#setting the x increment
        dy=math.sin(math.radians(dir))#setting the y increment

        while not is_wall(x,y): #while the point ahead isn't a wall
            x+=dx #increasing the x cor of the ray
            y+=dy #increasing the y cor of the ray 
            distance+=1

        #idk what was going on, some DDA bs
        # while not is_wall(x, y): 
        #     if (dx>0):
        #         next_vl=tile_size*((x//tile_size)+1)#the next vertical line
        #     else:
        #         if(x%tile_size!=0):
        #             next_vl=tile_size*(x//tile_size)
        #         else:
        #             next_vl=tile_size*((x//tile_size)-1)

        #     distance_to_next_vl=(next_vl-x)/dx

        #     if (dy>0):
        #         next_hl=tile_size*((y//tile_size)+1)#the next horizontal line
        #     else:
        #         if(y%tile_size!=0):
        #             next_hl=tile_size*(y//tile_size)
        #         else:
        #             next_hl=tile_size*((y//tile_size)-1)

        #     distance_to_next_hl=(next_hl-y)/dy

        #     if (distance_to_next_vl<distance_to_next_hl):
        #         distance+=distance_to_next_vl
        #         if (dx>0):
        #             x+=distance_to_next_vl*dx
        #             y+=distance_to_next_vl*dy
        #         else:
        #             x+=(next_vl-x-tile_size)
        #             y+=-(next_vl-x-tile_size)*math.tan(math.radians(180-dir))

        #     else:
        #         distance+=distance_to_next_hl
        #         x+=distance_to_next_hl*math.cos(math.radians(dir))
        #         y+=distance_to_next_hl*math.sin(math.radians(dir))
        
        corrected_distance=distance*math.cos(math.radians(player.heading()-dir))+0.00000001 #corrects the fish-eye...ness
        distance_array.append(corrected_distance) #appends the distance to the array

    render(num_rays, distance_array, horror_mode)

def render(num_rays, distance_array, horror_mode): #function for actually rendering everything
    ray.clear() #clears the screen every frame
    width = screenTk.winfo_screenwidth() #width of the screen
    height = screenTk.winfo_screenheight() #height of the screen
    ray.pensize(width/num_rays) #adjusting the thickness of a line, depending on number of rays
    ray.setx(-width/2) #where you start rendering from 
    for i in range(len(distance_array)): #repeating for number of rays (or distances)
        length=20000/distance_array[i] #some random number, used to calculate the length of the wall
        #drawing the room
        ray.up()
        ray.sety(height/2)
        if (horror_mode):
            ray.color(0, 0, 0)
        else:
            ray.color(100, 100, 100)
        ray.down()
        ray.sety(length/2)
        #drawing the walls
        ray.up()
        if (horror_mode):
            b=int(1000/distance_array[i])
        else:
            b=int(2000/distance_array[i])
        b=min(b, 255)
        b=max(b, 0.00000001)
        ray.color(0, 0, b)
        ray.down()
        ray.sety(ray.ycor()-length)
        #drawing the floor
        ray.up()
        ray.down()
        if (horror_mode):
            ray.color(0, 0, 0)
        else:
            ray.color(10, 10, 10)
        ray.sety(-height/2)
        ray.setx(ray.xcor()+ray.pensize())

def mouse_movement(last_mouse_x): #function for changing the player dir based on mousemovement
    width = screenTk.winfo_screenwidth()
    
    current_x = screenTk.winfo_pointerx()
    delta_x = current_x - last_mouse_x #caluclates the mousemovement, in a frame
    if (current_x==width-1): #if the mouse is at the edge, sends it to the opposite edge.
        pyautogui.moveTo(0, None)
    elif (current_x==0):
        pyautogui.moveTo(width-1, None)
    last_mouse_x = current_x

    sensitivity = 0.2 #some variable
    player.seth(player.heading() - delta_x * sensitivity) #setting the dir

def minimap(starting_x, starting_y):
    global map, tile_size

    mapping.clear()
    width=len(map[0])
    height=len(map)
    map_tile_size=20

    screen.tracer(0) # stops time

    x_adj=-800
    y_adj=400

    player_sprite.setheading(player.heading())
    player_sprite.goto(player.xcor()*(map_tile_size/tile_size)+((-starting_x+tile_size)*(map_tile_size/tile_size))+x_adj, player.ycor()*(map_tile_size/tile_size)-((starting_y+tile_size)*(map_tile_size/tile_size))+y_adj)

    for i in range((len(map))*len(map[1])):
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
    

def main(starting_x, starting_y): #main function
    #de variables
    num_rays=120
    FOV=90
    horror_mode=True
    last_mouse_x = screenTk.winfo_pointerx()

    #los funciones
    casting_ray(num_rays, FOV, horror_mode)

    player_movement()

    mouse_movement(last_mouse_x)

    minimap(starting_x, starting_y) #-125, 75   

    #print("current position = ", player.xcor(), player.ycor())

    # dir=player.heading()
    # print("dir = ", dir)
    # print(2.5*math.cos(math.radians(90-dir)))

    screen.update()
    screen.ontimer(lambda:main(starting_x, starting_y), 10) #repeats the main function, every ms

#movement stuff, idk man
screen.listen()
screen.onkeypress(press_w, "w")  
screen.onkeyrelease(release_w, "w")
screen.onkeypress(press_s, "s")  
screen.onkeyrelease(release_s, "s")

screen.onkeypress(press_a, "a")  
screen.onkeyrelease(release_a, "a")
screen.onkeypress(press_d, "d")  
screen.onkeyrelease(release_d, "d")

main(starting_x, starting_y)

screen.mainloop()