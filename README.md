## Description: 
Fourier transform a part of your screen in realtime.
An embedded matplotlib plot shows the 2D Fourier transform of a selected part of your screen. 
The region of interest and the fps count can be controlled from within the GUI. 

## Usage  
* Run FTML_GUI.py
* Click on select ROI
* Mark the region of interest in the image of your screen dispayed in the pop-up window and accept with OK.
* Click on Start FFT
* Change the desired frame rate in the textbox and accept with enter.

## Dependancies
 * GUI written using [wxPython](http://www.wxpython.org/)
 * Figures embeddded in UI using [matplotlib](http://www.matplotlib.org)
 * Selecting an area on an image using [Rectangle Selector Panel](https://github.com/ashokfernandez/wxPython-Rectangle-Selector-Panel)
 * Screen capturing with [mss](https://github.com/BoboTiG/python-mss)
