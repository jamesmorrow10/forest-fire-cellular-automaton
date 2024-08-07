import pygame
from forest_fire_cellular_automaton import forest
import time as time

pygame.init()
height = 400    
width = 400
# Set up the drawing window
surface = pygame.display.set_mode([width, height])
# scale determines the size of one tree/site.
scale = 2
# scale = 1.8
# setting up the forest
genesis_probability = 0.005
f = 1/100.0
# (gen = 0.005, f = 1/10000.0)
combustion_probability = genesis_probability*f

# sherwood_forest = forest(int(height/scale), int(width/scale), tree_genesis_probability, combustion_probability, 0)
sherwood_forest = forest(int(width/scale), int(height/scale), genesis_probability, combustion_probability, 1)


# Run until the user asks to quit
running = True
frame = 1
while running:
    frame += 1
    print(frame)
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for row in range(0, len(sherwood_forest.automaton_array)):
        for column in range(0, len(sherwood_forest.automaton_array[row])):
            color = (0, 0, 0)
            # keep empty sites black
            if sherwood_forest.automaton_array[row][column] == 0:
                pass
            # sites with trees are green
            elif sherwood_forest.automaton_array[row][column] == 1:
                color = (0, 255, 0)
            # burning sites are reds
            elif sherwood_forest.automaton_array[row][column] == 2:
                color = (255, 0, 0)
            else:
                print("Error: the forest sites should only be able to take on the values: 0, 1 and 2.\n")
            # Drawing Rectangle/forest site
            if frame == 0 or frame > 20:
                pygame.draw.rect(surface, color, pygame.Rect(scale*row, scale*column, scale, scale))
                # advance the forest state by one time step
                sherwood_forest.update()
    
    # to display the changes
    pygame.display.flip()
    time.sleep(0.01)
# Done! Time to quit.
pygame.quit()
