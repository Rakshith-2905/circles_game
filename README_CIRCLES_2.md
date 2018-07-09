# Circles 2

A program capable of digitizing circles in a 20x20 grid.
The user can  toggle points on the grid on and off. When the user clicks the generate button, a circle would be generated that best fits the highlighted points.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Dependencies

Python 2.7  
*See [Installing python](https://www.python.org/download/releases/2.7/) for instructions on how to install python.*  
Pygame 1.9.3  
*See [Installing pygame](https://cit.dixie.edu/cs/1410/pygame-installation.pdf) for instructions on how to install pygame.*  


## How to run

open a terminal or console. Change the operating directory to where the ```circles_2.py``` is  and type in

```
python circles_2.py
```

## Program structure

The program function ```create_game_env()``` to a game environment in pygame with 20x20 grids and digitalizes the grid points.

Then the program calls the ``` main() ``` function which monitors mouse clicks.  
When a click is recorded the pixel position of the click is appended to a list `circle[]`. When the generate button is clicked the mean and standard deviation(S.D) of the points is calculated and the points which are not in the median (+-) 2* SD are removed(outliers).

The optimal circle radius computation is shown in the image attached

another method is used where in all the possible circles that can be drawn with the digital points are taken and the least square error is computed for all these points. The circle with the minimum least square error is selected

## Authors

* **Rakshith Subramanyam** -  [github](https://github.com/Rakshith-2905)


## License

None
