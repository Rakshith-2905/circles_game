#!/usr/bin/python
"""
    Requirements to run the code:
    Python 2.7.14
    Pygame 1.9.3
"""
import pygame
import math
import numpy as np

"""
    Pygame screen properties
"""

background_colour = (255,255,255)
(width, height) = (700, 700)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Part 2')
screen.fill(background_colour)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


"""
    Function to set up the game environment with the digitalized grids
"""
def game_env(rows=20,columns=20):

    y = 50
    matrix = [[0 for i in xrange(rows)] for i in xrange(columns)]

    for i in range(rows):
        x = 50
        for j in range(columns):
            matrix[i][j] = (y,x)
            pygame.draw.circle(screen, (128,128,128), matrix[i][j], 8)
            x = x+30
        y = y+30
    return matrix

"""
    Function to create and monitor the generate button in the game environment
"""
def button(msg, mouse, x = 300, y = 640, w = 100, h = 40, ic = (0,255,0), ac = (0,155,0)):

    # Checking for mouse click
    click = pygame.mouse.get_pressed()

    # Checking if the mouse is over the button or not
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        # Return true if the mouse is clicked on the button
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    textsurface = myfont.render('Generate', False, (0, 0, 0))
    screen.blit(textsurface,(305,648))

"""
    Function running the main algorithm in the game environment
"""
def main(m,grid = 20):

    running = True
    # # Creating a empty list to hold the points that user clicks
    points = []
    # # Loop will be executing till the game window is closed
    while running:
        pygame.display.update()

        # # Monitoring the events like mouse click
        for event in pygame.event.get():

            # # Check if the window is closed
            if event.type == pygame.QUIT:
                running = False
            # # Get mouse unclick
            if event.type == pygame.MOUSEBUTTONUP:

                # # Get the position of the mouse
                end_pos = pygame.mouse.get_pos() # rows = end_pos[1] columns = end_pos[0])

                # # Check if the mouse is not on the button
                if end_pos[1] < 640:
                    # # Convert the mouse position in pixel to the DC cordinates
                    # # By computing the min of the dist of every DC point with the mouse point
                    row_diff = []
                    column_diff = []
                    for i in range(len(m)):
                        for j in range(len(m)):
                            row_diff.append( abs(end_pos[1]-m[i][j][0]))
                            column_diff.append( abs(end_pos[0]-m[i][j][1]))

                    # # Computing the pixel coordinates of the DC
                    circle = m[column_diff.index(min(column_diff))][int(row_diff.index(min(row_diff))/20)]
                    if circle not in points:points.append(circle)

                    # #Change the Color of the circle to indicate the click
                    pygame.draw.circle(screen, (255,0,0),circle , 8)


            # # Calling the function to read the generate button state
            but = button('Generate',pygame.mouse.get_pos())

            # # Creating a empty list to hold the radius and center of the circle
            circle_radius = []
            # # If the generate button is pressed execute the following conditions
            if but:
                final_list = []

                # # Computing the mean and standard deviation(S.D) of the points
                mean = np.mean(points, axis=0)
                sd = np.std(points, axis=0)

                # # Placing a yellow dot to denote the mean
                # pygame.draw.circle(screen, (255,255,0), (int(mean[0]),int(mean[1])), 5)

                # # Computing median
                x_sorted = sorted([x[0] for x in points])
                y_sorted = sorted([x[1] for x in points])

                if(len(x_sorted)%2 is 0):
                    x_center = int(x_sorted[len(x_sorted)/2]+x_sorted[(len(x_sorted)/2)-1])/2
                    y_center = int(y_sorted[len(y_sorted)/2]+y_sorted[(len(y_sorted)/2)-1])/2
                else:
                    x_center = x_sorted[((len(x_sorted)-1)/2)]
                    y_center = y_sorted[((len(y_sorted)-1)/2)]
                median = (x_center,y_center)


                # # Removing outliers which lie outside 1.5 of S.D in the gaussian distribution
                for x in points:

                    if ((median[0] - 2 * sd[0] < x[0] < median[0] + 2 * sd[0]) and (median[1] - 2 * sd[1] < x[1] < median[1] + 2 * sd[1])):
                        final_list.append(x)
                points = final_list

                # # Computing new center without outliers
                center = np.mean(points, axis=0)
                center = (int(center[0]),int(center[1]))
                pygame.draw.circle(screen, (255,0,0), center, 5)


                # # By doing some math(refer readme) the optimal radius is found
                # # out to the mean of all the radius(between center and all mouse clicks)
                for a in range(len(points)):
                    # # Getting the Radius of the circle to be drawn
                    # # By Computing the Equlidian dist between the center and every point of the mouse click
                    circle_radius.append(math.sqrt(((center[1] - points[a][1])**2)+((center[0] - points[a][0])**2)))

                print(circle_radius)
                rad = np.mean(circle_radius, axis=0)
		# # Drawing a blue circle with method 1
                pygame.draw.circle(screen, (0,0,255), center, int(rad),3)

                # # *********Alternate method - Least Square ***********

                # # Getting all the possible circles that can be drawn with the points

                circle_radius = []
                d3 = []
                mini = -1
                for a in range(len(points)):
                    # # Getting the Radius of the circle to be drawn
                    # # By Computing the Equlidian dist between the center point and the end point of the mouse click
                    circle_radius.append(math.sqrt(((center[1] - points[a][1])**2)+((center[0] - points[a][0])**2)))

                    # theta goes from 0 to 2pi
                    theta = np.linspace(0, 2*np.pi, 100)

                    # the radius of the circle
                    r = math.sqrt(((center[1] - points[a][1])**2)+((center[0] - points[a][0])**2))

                    # compute x1 and x2 that satisfies the line equation
                    x = r*np.cos(theta)+center[0]
                    y = r*np.sin(theta)+center[1]


                    # # Compute least squares error for all the possible circles with the digital points
                    d2 = 0
                    temp = []

                    for b in range(len(points)):
                        d = []
                        for j in range(len(x)):
                            d.append(math.sqrt(((x[j] - points[b][0])**2)+((y[j] - points[b][1])**2)))

                        if min(d) not in temp:
                            temp.append(min(d))
                            d2 += (min(d)**2)
                    d3.append(d2)

                k = d3.index(sorted(d3)[0])
                # # Drawing a red circle with method 1
                pygame.draw.circle(screen, (255,0,0), center, int(circle_radius[k]),3)
                pygame.display.update()
                points = []


"""
Begining of the program
"""
if __name__ == '__main__':

    # # Setting up the main game environment for 20X20 grid
    m = game_env(20,20)
    main(m,20)
