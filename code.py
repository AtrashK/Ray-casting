import turtle
import time
import math

screen=turtle.getscreen()
screen.colormode(255)
screen.bgcolor("black")
screenTk = screen.getcanvas().winfo_toplevel()
screenTk.attributes("-fullscreen", 1)

turtle.ht()

# stops time
screen.tracer(0)

player=turtle.Turtle()
player.up()
player.ht()
#player.shape("circle")

test=turtle.Turtle()
test.ht()
test.up()

ray=turtle.Turtle()
ray.up()
ray.ht()
ray.color(0,0,255)
ray.pensize(10)

screen.update()

key_held_w = False
key_held_s = False
key_held_a = False
key_held_d = False
key_held_left=False
key_held_right=False

moved=True
distance_array=[]

# map=["########",
#      "#   #  #",
#      "# # ## #",
#      "# #    #",
#      "#    # #",
#      "########"]

map=["#########",
     "#       #",
     "# ## ## #",
     "# #   # #",
     "#   #   #",
     "# #   # #",
     "# ## ## #",
     "#       #",
     "#########",]

width=len(map[0])
height=len(map)
tile_size=50
map_left=-1*(width/2)*tile_size
map_top=(height/2)*tile_size

spawn_found=False
spawn_counter=0

while (spawn_found==False):
    if (map[spawn_counter//width][spawn_counter%width]!="#"):
        spawn_found=True
    else:
        spawn_counter+=1

row=spawn_counter//width
col=spawn_counter%width

player.goto((col*tile_size)+map_left+(tile_size/2), map_top-(row*tile_size)-(tile_size/2))

# Turtle for drawing FPS text
width = screenTk.winfo_screenwidth()
height = screenTk.winfo_screenheight()
fps_turtle = turtle.Turtle()
fps_turtle.hideturtle()
fps_turtle.penup()
fps_turtle.goto(-(width/2)+50, (height/2)-50)

# Variables for FPS calculation
frame_count = 0
start_time = time.time()
fps = 0

def update():
    global frame_count, start_time, fps

    # Count frames
    frame_count += 1

    # Calculate FPS every second
    current_time = time.time()
    elapsed = current_time - start_time

    if elapsed >= 1.0:
        fps = frame_count / elapsed
        frame_count = 0
        start_time = current_time

    # Clear and redraw FPS text
    fps_turtle.clear()
    fps_turtle.write(f"FPS: {int(fps//1)}", font=("Arial", 16, "normal"))

    # Update screen
    screen.update()

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

def press_left():
    global key_held_left
    key_held_left = True

def release_left():
    global key_held_left
    key_held_left = False

def press_right():
    global key_held_right
    key_held_right = True

def release_right():
    global key_held_right
    key_held_right = False

def is_wall(x, y):
    global height, width, map, tile_size, map_left, map_top

    col=int((x-map_left)/tile_size)
    row=int((map_top-y)//tile_size)

    if (row<0 or row>height-1 or col<0 or col>width-1):
        return True
    else:
        if (map[row][col]=="#"):
            return True
        else:
            return False
    
def player_movement():
    global key_held_w, key_held_s, key_held_a, key_held_d, moved
    dir=math.radians(player.heading())

    if key_held_w and not is_wall(player.xcor()+2.5*math.cos(dir), player.ycor()+2.5*math.sin(dir)):
        player.forward(2.5)
    if key_held_s and not is_wall(player.xcor()-2.5*math.cos(dir), player.ycor()-2.5*math.sin(dir)):
        player.backward(2.5)

    if key_held_d and not is_wall(player.xcor()+2.5*math.cos(90-dir), player.ycor()-2.5*math.sin(90-dir)):
        player.goto(player.xcor()+2.5*math.cos(90-dir), player.ycor()-2.5*math.sin(90-dir))

    if key_held_a and not is_wall(player.xcor()-2.5*math.cos(90-dir), player.ycor()+2.5*math.sin(90-dir)):
        player.goto(player.xcor()-2.5*math.cos(90-dir), player.ycor()+2.5*math.sin(90-dir))

    if key_held_left:
        player.seth(player.heading()+5)
    if key_held_right:
        player.seth(player.heading()-5)

def casting_ray(num_rays, FOV):
    global distance_array, tile_size
    distance_array.clear()
    for i in range(0, num_rays+1):
        x=player.xcor()
        y=player.ycor()
        distance=0
        dir=player.heading()+(FOV/2)-((FOV*i)/num_rays)
        #dir=(player.heading()-i)
        dx=math.cos(math.radians(dir))
        dy=math.sin(math.radians(dir))

        while not is_wall(x,y):
            x+=dx
            y+=dy
            distance+=1

        # while not is_wall(x, y):
        #     if (dx>0):
        #         next_vl=tile_size*((x//tile_size)+1)#the next vertical line
        #     else:
        #         if(x%tile_size!=0):
        #             next_vl=tile_size*(x//tile_size)
        #         else:
        #             next_vl=tile_size*((x//tile_size)-1)

        #     distance_to_next_vl=abs((next_vl-x)/dx)

        #     if (dy>0):
        #         next_hl=tile_size*((y//tile_size)+1)#the next horizontal line
        #     else:
        #         if(y%tile_size!=0):
        #             next_hl=tile_size*(y//tile_size)
        #         else:
        #             next_hl=tile_size*((y//tile_size)-1)

        #     distance_to_next_hl=abs((next_hl-y)/dy)

        #     if (distance_to_next_vl<distance_to_next_hl):
        #         distance+=distance_to_next_vl
        #         x+=distance_to_next_vl*math.cos(math.radians(dir))
        #         y+=distance_to_next_vl*math.sin(math.radians(dir))
        #     else:
        #         distance+=distance_to_next_hl
        #         x+=distance_to_next_hl*math.cos(math.radians(dir))
        #         y+=distance_to_next_hl*math.sin(math.radians(dir))
        
        corrected_distance=distance*math.cos(math.radians(player.heading()-dir))+0.00000001
        distance_array.append(corrected_distance)

    render(num_rays, distance_array)

def render(num_rays, distance_array):
    ray.clear()
    width = screenTk.winfo_screenwidth()
    height = screenTk.winfo_screenheight()
    ray.pensize(width/num_rays)
    ray.setx(-width/2)
    for i in range(len(distance_array)):
        length=20000/distance_array[i]
        ray.up()
        ray.sety(height/2)

        ray.color(100, 100, 100)
        ray.down()
        ray.sety(length/2)

        ray.up()
        b=int(2000/distance_array[i])
        b=min(b, 255)
        b=max(b, 0.00000001)
        ray.color(0, 0, b)
        ray.down()
        ray.sety(ray.ycor()-length)

        ray.up()
        ray.down()
        ray.color(10, 10, 10)
        ray.sety(-height/2)
        ray.setx(ray.xcor()+ray.pensize())

def main():
    num_rays=120
    FOV=90

    casting_ray(num_rays, FOV)

    player_movement()

    update()

    #print(distance_array)

    # print(player.xcor(), player.ycor())
    # print(player.heading())

    screen.update()
    screen.ontimer(main, 10)

screen.listen()
screen.onkeypress(press_w, "w")  
screen.onkeyrelease(release_w, "w")
screen.onkeypress(press_s, "s")  
screen.onkeyrelease(release_s, "s")

screen.onkeypress(press_a, "a")  
screen.onkeyrelease(release_a, "a")
screen.onkeypress(press_d, "d")  
screen.onkeyrelease(release_d, "d")

screen.onkeypress(press_left, "Left")  
screen.onkeyrelease(release_left, "Left")
screen.onkeypress(press_right, "Right")
screen.onkeyrelease(release_right, "Right")

main()

screen.mainloop()