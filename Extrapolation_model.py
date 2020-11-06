# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plot

# Get x values of the sine wave
time        = np.arange(0, 100, 0.1);

# Amplitude of the sine wave
amplitude   = 10*np.sin(0.15*time)

# disturbance (sum of sines)
amplitude2 = 0.25*np.sin(.6*time -.4) + 0.4*np.sin(.7*time+.5) + 0.9*np.sin(.3*time)
disturbance= 1*amplitude2

## to make compensatory tracking uncomment the next line ##
# amplitude=np.zeros(1000)

## Parameters ##

OutGain=15 # gain for extrapolation model
XGain=20   # gain for extrapolation model

OutGain2=15 # gain for position control model

# for both models
slow=0.5
Ref=0
delay=2
dt=1/100

# intialise
out=np.zeros(1000)
out2=np.zeros(1000)
error=0


# Run Model
for index in range(1,999):
    if index < 6:
       out[index]=0
       out2[index]=0
    elif index > 6:
    
       # calculate error terms for models
       error =  out2[index-delay] - amplitude[index-delay]
       velocity_error = out[index-delay] - (amplitude[index-delay] + (XGain*(amplitude[index-delay]-amplitude[index-(delay+1)])))   
       
       # add disturbance to error terms
       error = error + disturbance[index]
       velocity_error = velocity_error+disturbance[index]
       
       # velocity extrapolation model
       out[index] = out[index-1] + slow*((OutGain*(Ref - velocity_error)) - out[index-1]) * dt

       # position control model
       out2[index] = out2[index-1] + slow*((OutGain2*(Ref - error)) -  out2[index-1]) * dt


plot.plot(time,amplitude,time,out,time,out2,time,disturbance)
plot.title('Sine wave')
# Give x axis label for the sine wave plot
plot.xlabel('Time')
# Give y axis label for the sine wave plot
plot.ylabel('Amplitude = sin(time)')
plot.grid(True, which='both')
plot.axhline(y=0, color='k')

np.corrcoef(amplitude,out) # correlation coefficient extrapolation model
np.corrcoef(amplitude,out2) # correlation coefficient control model

    
    
