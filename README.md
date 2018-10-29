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

![ ](https://github.com/Ruslan0990/Transform-My-Live/blob/master/gifs/ROI_selection.gif)
![ ](https://github.com/Ruslan0990/Transform-My-Live/raw/master/gifs/FT_live.gif)

## Dependancies
 * GUI written using [wxPython](http://www.wxpython.org/)
 * Figures embeddded in UI using [matplotlib](http://www.matplotlib.org)
 * Screen capturing with [mss](https://github.com/BoboTiG/python-mss)

## Credits
* [Ruslan0990](https://github.com/Ruslan0990)
* [littlechristiaan](https://github.com/littlechristiaan)

* ROI selection code from [ashokfernandez](https://github.com/ashokfernandez)
* Sample image credit: [link](http://www.werteloberfell.com/)
