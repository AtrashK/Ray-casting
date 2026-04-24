import math

dir=30#changing the player's direction to radians, cuz pymath weird like that 
fd_bd_x=2.5*math.cos(math.radians(dir))
fd_bd_y=2.5*math.sin(math.radians(dir))
lf_rt_x=2.5*math.cos(math.radians(dir-90))
lf_rt_y=2.5*math.sin(math.radians(dir-90))

print("lf_rt_x = ", lf_rt_x)