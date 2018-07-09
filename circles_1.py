#!/usr/bin/python

"""
    Requirements to run the code:
    Opencv 3.4.1
    Pygame 1.9.3
"""

import pygame
import math

# Pygame screen properties
background_colour = (255,255,255)
(width, height) = (700, 700)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Part 1')
screen.fill(background_colour)


"""
    Function to set up the game environment with the digitalized grids
"""
def create_game_env(rows=20,columns=20):

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
    Function to draw the mean, max and min circles
"""
def compute_circle(center,radius,m):
    circle = [] # A List containing the pixel points of the user drawn circle

    # # Getting all the points in a square that circumscribes the circle
    # # and satisfies the circle equation (X-X_c)^2 + (Y-y_c)^2 = r^2
    for x in range(int(center[1]-radius-20),int(center[1]+radius+20)):
        for y in range(int(center[0]-radius-20),int(center[0]+radius+20)):
            # # Computing the distance of each point in the square from the center
            rad = math.sqrt(((x-center[1])**2)+((y-center[0])**2))
            # # Consider only the points that are satisfying the radius condition
            if abs(rad-radius)<1:
                # # Appending these points to a list
                circle.append((x,y))
                # # Draw a small dot in that point
                pygame.draw.circle(screen, (0,0,0), (y,x), 1)
                pygame.display.update()

    # # Iterating through each point(pixel point) in the list circle to get the
    # # closest digital points. Computed by calculating the euclidean dist
    digital_circle = []

    # # Iterating through each pixel point
    for x in range(len(circle)):

         # # A List to store the distance betweem the digital points in the
         # # circle and the center of the circle
        dist_center=[]

        # # Iterating through each digital point
        for i in range(len(m)):
            for j in range(len(m)):

                # # Check if the distance of a point in the circle is close to a digital point
                if(math.sqrt(((circle[x][0]-m[i][j][0])**2)+((circle[x][1]-m[i][j][1])**2))<10):
                    if(m[i][j]) not in digital_circle:
                        digital_circle.append(m[i][j])
    # # Iterate through all the digital points the circle touches
    for a in range(len(digital_circle)):
        pygame.draw.circle(screen, (0,100,255), (digital_circle[a][1],digital_circle[a][0]), 8)
        # # Compute the distance betweem the digital points in the circle and the center of the circle
        dist_center.append(math.sqrt((digital_circle[a][0]-center[1])**2 + (digital_circle[a][1]-center[0])**2))

    # # Draw two circle using the minimum and maximum distance between
    # # the center of the circle to the digital points that touches the circle
    pygame.draw.circle(screen, (200,0,0), center, int(min(dist_center)),3)
    pygame.draw.circle(screen, (200,0,0), center, int(max(dist_center)),3)

"""
    Function running the main algorithm in the game environment
"""
def main(m, grid = 20):

    running = True

    # # Loop will be executing till game the window is closed
    while running:
        pygame.display.update()

        # # Monitoring the events like mouse click
        for event in pygame.event.get():

            # # Read mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                # # Get starting the position of the mouse click
                start_pos = pygame.mouse.get_pos()

                # # Convert the mouse position in pixel to the DC cordinates
                # # By computing the min of the dist of every DC point with the mouse point
                start_row_diff = []
                start_column_diff = []

                for i in range(len(m)):
                    for j in range(len(m)):
                        start_row_diff.append( abs(start_pos[1]-m[i][j][0]))
                        start_column_diff.append( abs(start_pos[0]-m[i][j][1]))

                # # Computing the pixel coordinates of the digital point
                start_circle = m[start_column_diff.index(min(start_column_diff))][int(start_row_diff.index(min(start_row_diff))/grid)]
                # # Change the Color of the circle to indicate the click
                pygame.draw.circle(screen, (128,0,0),start_circle, 8)

            # #Get mouse unclick
            if event.type == pygame.MOUSEBUTTONUP:

                # # Get ending the position of the mouse unclick
                end_pos = pygame.mouse.get_pos() # rows = end_pos[1] columns = end_pos[0])

                # # Convert the mouse position in pixel to the DC cordinates
                # # By computing the min of the dist of every DC point with the mouse point
                row_diff = []
                column_diff = []
                for i in range(len(m)):
                    for j in range(len(m)):
                        row_diff.append( abs(end_pos[1]-m[i][j][0]))
                        column_diff.append( abs(end_pos[0]-m[i][j][1]))

                # # Computing the pixel coordinates of the digital
                end_circle = m[column_diff.index(min(column_diff))][int(row_diff.index(min(row_diff))/grid)]

                # # Getting the Radius of the circle to be drawn
                # # By Computing the Equlidian dist between the start point and the end point of the mouse click
                circle_radius = (math.sqrt(((end_circle[1] - start_circle[1])**2)+((end_circle[0] - start_circle[0])**2)))

                # # Change the Color of the circle to indicate the click
                pygame.draw.circle(screen, (0,128,0),end_circle , 8)

                # # Call the Function to draw the mean, max and min circles
                compute_circle(start_circle,circle_radius,m)

            # # Check if the window is closed
            if event.type == pygame.QUIT:
                running = False
"""
Begining of the program
"""
if __name__ == '__main__':
    m = create_game_env(20,20)
    main(m)
