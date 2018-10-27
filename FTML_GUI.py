import wx  
import numpy as np
import mss
import cv2
from skimage.color import rgb2gray 
import time
import matplotlib       
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

class ROI_panel(wx.Frame):
    def __init__(self, parent , sct):            
        wx.Frame.__init__(self, parent, -1,'ROI selection', size=(600, 400))        
        self.main = parent
        save_button = wx.Button(self, label="OK" )
        save_button.SetFont( wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.BOLD)  )
        cancel_button = wx.Button(self, label="Cancel" )
        cancel_button.SetFont( wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.BOLD)  )
        self.Bind(wx.EVT_BUTTON, self.OnSave, save_button)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, cancel_button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow) 
        # Intitialise the matplotlib figure
        self.figure = plt.figure()
        # Create an axes, turn off the labels and add them to the figure
        self.axes = plt.Axes(self.figure,[0,0,1,1])      
        self.axes.set_axis_off() 
        self.figure.add_axes(self.axes) 
        # Add the figure to the wxFigureCanvas
        self.canvas = FigureCanvas(self, -1, self.figure)
        # Initialise the rectangle      
        self.rect = Rectangle((0,0), 1, 1, facecolor='None', edgecolor='green')
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.axes.add_patch(self.rect)
        # Sizer to contain the canvas
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1,  wx.EXPAND|wx.ALL,5)                
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(save_button, 0, wx.ALIGN_CENTER|wx.ALL, border=5)
        hbox.Add(cancel_button, 0, wx.ALIGN_CENTER|wx.ALL, border=5)
        self.sizer.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        self.SetSizer(self.sizer)
        self.Layout()
        # Connect the mouse events to their relevant callbacks
        self.canvas.mpl_connect('button_press_event', self._onPress)
        self.canvas.mpl_connect('button_release_event', self._onRelease)
        self.canvas.mpl_connect('motion_notify_event', self._onMotion)
        self.pressed = False
        # with mss.mss() as sct:
        img=np.asarray(sct.grab(sct.monitors[1]))
        # img = rgb2gray(img)        
        # Add the image to the figure and redraw the canvas. Also ensure the aspect ratio of the image is retained.
        self.axes.imshow(img,aspect='equal') 
        self.canvas.draw()

    def _onPress(self, event):
            # Check the mouse press was actually on the canvas
            if event.xdata is not None and event.ydata is not None:
                # Upon initial press of the mouse record the origin and record the mouse as pressed
                self.pressed = True
                self.rect.set_linestyle('dashed')
                self.x0 = event.xdata
                self.y0 = event.ydata

    def _onRelease(self, event):
        # Check that the mouse was actually pressed on the canvas to begin with and this isn't a rouge mouse 
        # release event that started somewhere else
        if self.pressed:
            # Upon release draw the rectangle as a solid rectangle
            self.pressed = False
            self.rect.set_linestyle('solid')
            # Check the mouse was released on the canvas, and if it wasn't then just leave the width and 
            # height as the last values set by the motion event
            if event.xdata is not None and event.ydata is not None:
                self.x1 = event.xdata
                self.y1 = event.ydata
            # Set the width and height and origin of the bounding rectangle
            self.boundingRectWidth =  self.x1 - self.x0
            self.boundingRectHeight =  self.y1 - self.y0
            self.bouningRectOrigin = (self.x0, self.y0)
            # Draw the bounding rectangle
            self.rect.set_width(self.boundingRectWidth)
            self.rect.set_height(self.boundingRectHeight)
            self.rect.set_xy((self.x0, self.y0))
            self.canvas.draw()

    def _onMotion(self, event):
        # If the mouse has been pressed draw an updated rectangle when the mouse is moved so 
        # the user can see what the current selection is
        if self.pressed:
            # Check the mouse was released on the canvas, and if it wasn't then just leave the width and 
            # height as the last values set by the motion event
            if event.xdata is not None and event.ydata is not None:
                self.x1 = event.xdata
                self.y1 = event.ydata            
            # Set the width and height and draw the rectangle
            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))
            self.canvas.draw()

    def OnSave(self, event):
        if self.x0 and self.x1 :
            ROI_msg ='[' + str(int(self.x0))+ ',' + str(int(self.x1))+';' + str(int(self.y0))+',' + str(int(self.y1)) +']' 
            self.main.mon = {"top": int( min(self.y0,self.y1)), "left": int(min(self.x0,self.x1)), "width": int( abs(self.x1-self.x0)) , "height": int( abs(self.y1 - self.y0)) }
            self.main.ROI_text.SetLabel( ROI_msg  )   
            self.main.ROI_text.Update()        
            self.main.Layout()
            print('Selected ROI ....')   
            self.Close(True)
        else:
            print('No ROI selected....')   

    def OnCloseWindow(self, event):
        self.Destroy()

class mainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None , title="FTML" ,  size=(400, 600) )
        bold_font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.BOLD)    
        normal_font = wx.Font(14, wx.DECORATIVE, wx.NORMAL,wx.NORMAL) 
        collpane = wx.CollapsiblePane(self, label="" )
        collpane.Expand() 
        pane = collpane.GetPane()

        self.paneSz= wx.BoxSizer(wx.VERTICAL) 
        self.paneSz.Add(collpane, 0,  wx.EXPAND | wx.ALL, 0)
        self.button1 = wx.Button(pane, wx.ID_ANY, "Select ROI") 
        self.button1.Bind(wx.EVT_BUTTON, self.select_ROI)     
        self.button1.SetFont(bold_font)
        self.button2 = wx.Button(pane, wx.ID_ANY, "Start FFT") 
        self.button2.Bind(wx.EVT_BUTTON, self.startFFT)     
        self.button2.SetFont(bold_font)        
        self.ROI_text1 = wx.StaticText(pane,wx.ID_ANY, 'ROI: ') 
        self.ROI_text1.SetFont(normal_font)
        self.ROI_text = wx.StaticText(pane, wx.ID_ANY, 'not set') 
        self.ROI_text.SetFont(normal_font)
        self.fps_lbl = wx.StaticText(pane,wx.ID_ANY, "FPS: ")
        self.fps_input = wx.TextCtrl(pane,wx.ID_ANY, "5")
        self.fps_input.SetFont(normal_font) 
        self.fps_lbl.SetFont(normal_font)           
        self.fps_input.Bind(wx.EVT_TEXT_ENTER, self.on_user_fps_input)

        self.mon = {}
        self.timer = wx.Timer(self)
        self.fps = 5
        self.fps_limit =15
        self.FFTrunning =0
        self.sct = mss.mss()
        # Intitialise the FFT matplotlib figure
        self.FtFig = plt.figure()
        self.FFTaxes = plt.Axes(self.FtFig,[0,0,1,1])      
        self.FFTaxes.set_axis_off() 
        self.FtFig.add_axes(self.FFTaxes) 
        self.FFTcanvas = FigureCanvas(self, -1, self.FtFig)    

        gs = wx.GridSizer(rows=3, cols=2, hgap=5, vgap=5)
        gs.AddMany([(self.button1, 0, wx.ALIGN_CENTER ),        
            (self.button2, 0, wx.ALIGN_CENTER ), 
            (self.ROI_text1, 0, wx.ALIGN_CENTER ), 
            (self.ROI_text, 0, wx.ALIGN_CENTER ), 
            (self.fps_lbl,  0,wx.ALIGN_CENTER ), 
            (self.fps_input, 0, wx.ALIGN_CENTER ) ])    

        pane.SetSizer(gs)     
        self.paneSz.SetSizeHints(pane)
        
        self.sizer= wx.BoxSizer(wx.VERTICAL) 
        self.sizer.Add(self.paneSz, 0, wx.EXPAND | wx.ALL, 0)
        
        sizerCanvas= wx.BoxSizer(wx.VERTICAL)         
        sizerCanvas.Add(self.FFTcanvas, 1,  wx.EXPAND|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL ,5) 
        sizerCanvas.SetItemMinSize(self.FFTcanvas, (500,500))

        self.sizer.Add(sizerCanvas, 1,  wx.EXPAND|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL ,0)       
        
        self.SetSizer(self.sizer)
        self.Layout()
        print('Initialized GUI ....')   

    def select_ROI(self, evt):
        self.roi_panel = ROI_panel( self, self.sct )
        self.roi_panel.Show()

    def on_user_fps_input(self, event):
        try:
            self.fps =  int (self.fps_input.GetValue())     
            if  self.fps>self.fps_limit:
                 print ("I capped your fps to "+  str(self.fps_limit) )
                 self.fps = self.fps_limit
                 self.fps_input.SetLabelText(str(self.fps_limit))
            self.timer.Stop()
            self.timer.Start(1000./self.fps)
        except ValueError: 
            print ("Please type a number in the input textbox.")

    def startFFT(self, evt):
        if self.mon:
            if not self.FFTrunning:
                self.FFTrunning =1
                self.button2.LabelText = "Stop FFT"
                img= rgb2gray(np.asarray(self.sct.grab(self.mon)))
                img=np.abs(np.fft.fftshift(np.fft.fft2(img)))
                self.FFTim = self.FFTaxes.imshow(np.log(img+1),aspect='equal', cmap= plt.cm.get_cmap('CMRmap')) 
                self.FFTcanvas.draw()                
                self.timer.Start(1000./self.fps)
                self.Bind(wx.EVT_TIMER, self.NextFrame)
            else:
                self.button2.LabelText = "Start FFT"
                self.timer.Stop()
                self.FFTrunning = 0
        else:
            msg = wx.MessageDialog(self, "Please select a region of interest first.", 'hoi', wx.OK | wx.ICON_INFORMATION )
            msg.ShowModal()
            msg.Destroy()
    
    def NextFrame(self, e):
        img= rgb2gray(np.asarray(self.sct.grab(self.mon)))
        img=np.abs(np.fft.fftshift(np.fft.fft2(img)))
        self.FFTim.set_array(np.log(img+1))
        self.FFTcanvas.draw()

if __name__ == "__main__":
    app = wx.App()
    window = mainWindow()
    window.Show()
    app.MainLoop()
