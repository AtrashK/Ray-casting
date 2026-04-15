import turtle
import time

# Setup screen
screen = turtle.Screen()
screen.title("FPS Counter Example")
screen.tracer(0)  # turn off auto-updating for manual control

# Turtle for drawing FPS text
fps_turtle = turtle.Turtle()
fps_turtle.hideturtle()
fps_turtle.penup()
fps_turtle.goto(-200, 200)

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
    fps_turtle.write(f"FPS: {fps:.2f}", font=("Arial", 16, "normal"))

    # Update screen
    screen.update()

    # Call this function again (game loop)
    screen.ontimer(update, 16)  # ~60 FPS target

# Start loop
update()
screen.mainloop()