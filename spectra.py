# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:28:58 2024

@author: Kelby Palencia
"""
import matplotlib.pyplot as plt
from wotan import flatten 
import pandas as pd
import numpy as np
from scipy import stats
import time


## Finds the index bounds in a data set to limit figure parameters given lower and upper bounds. Returns it as a tuple
def find_bounds(lowlim,uplim,dset):
    
    if lowlim>dset[len(dset)-1] or uplim<dset[0]:
        raise ValueError("Data does not contain the given limit range")
    
    lower_index=0
    upper_index=0
    for x in range(len(dset)):
        if dset[x]<=lowlim:
            lower_index=x
        elif dset[x] <= uplim:
            upper_index=x
        elif dset[x] > uplim:
            break
    return(lower_index,upper_index)


def spectra_fig (     
        
        Inputfile,                #File input directory as a string
        
        emission_line_data=None,  #spectral line data that has the lines of interest
        
        Outfile=None,             #Output file directory as a string
        
        ):
    
    start=time.time()             #Store starting time stamp 
    
    if emission_line_data==None:  #If no emission line data is provided the script uses the harcoded spectral lines of interest
        #Hardcoded spectralines of interest to be used in data
        emission_line_data=[["OH (hydroxyl)",1612.231],["OH (hydroxyl)",1665.402],["OH (hydroxyl)",1667.359],["OH (hydroxyl)",1720.530],["HI (hydrogen)",1420.406],["H2CO (formaldehyde)",1428.685],["CH3OH (methanol)",1670.425],["CH3OH (methanol)",1616.593]]
        emission_line_df= pd.DataFrame(emission_line_data,columns=["Compound","Frequency (MHz)"]) #Converting spectral lines into data frame for easier use and manipulation
    
    if Outfile==None:                           #If there is no output file directory it will use the data directory and output a png graph of the data
        Outfile=Inputfile[0:len(Inputfile)-3]+"png"
    elif type(Outfile)!=str:                    #Verify the data output file is a string
        raise ValueError("Output file directory can only be a string") 
        
    if type(Inputfile)!=str:                    #Verify the data input file is a string
        raise ValueError("Input file directory can only be a string")    
        
    if Inputfile[len(Inputfile)-3:]!='csv':     #Verify the input file is a csv
        raise ValueError("unsupported or unrecognized file")
        
        
    #opening and reading data from given csv file
    data=pd.read_csv(Inputfile)
   
    #seperating the data from the CSV into frequency and Intensity
    frequency=data[data.columns[0]]
    Intensity=data[data.columns[1]]
    
    #preset for 8 plot figure
    fig, axs = plt.subplots(ncols=4,nrows=2,figsize=(20,10))        #figure size is in inches
    #original subplot specs hspace=0.350,wspace=0.400               
    fig.subplots_adjust(top=0.924,bottom=0.058,left=0.045,right=0.975,hspace=0.318,wspace=0.333) #figure subplot size configuration
    i=0  #Initializing counter variable for for loop. This is used to acessed data in the data frame 
    
    #loop that goes over the figure in the horizontal and vertical positions
    for x in range(2):
        
        for y in range(4):
            #determening the bounds of the data +- 1 from the spectral line  
            range_bounds=find_bounds(emission_line_df.iat[i,1]-1 , emission_line_df.iat[i,1]+1,frequency.tolist())
            #fuction returns the flatten data and the trendline of the data from the given bounds
            flat_Intensity,trend_line_Intensity =flatten(frequency[range_bounds[0]:range_bounds[1]],Intensity[range_bounds[0]:range_bounds[1]],window_length=51,cval=4, method='savgol',return_trend=True)
    
            k=(frequency[range_bounds[0]:range_bounds[1]]/emission_line_df.iat[i,1]).tolist() # represents the ratios of the observed frequency to the source frequency
            v=[]                                                                              # Initializing the velocity list        
            c=299792.4580                                                                     # Initializing the value of the speed of light in km/s
       
            '''
            loop that goes over all the ratios of the observed frequency and if the 
            value is lower or bigger than source frequency it calculates de velocity 
            due to redshift or blueshift  
            '''
            for l in range(len(k)):
                if k[l] > 1 :
                    v.append(((k[l]**2-1)/(k[l]**2+1)*c))       # Redshift
                elif k[l] <=1 :
                    v.append((((k[l]**2-1)/(k[l]**2+1))*c))     # Blueshift 
            
            r_sigma=stats.median_abs_deviation(Intensity[range_bounds[0]:range_bounds[1]]-trend_line_Intensity)  #Calculates the robust sigma of the flatten data in the given range 
          
            #setting the labels and tittle of each subplot
            axs[x,y].set_ylabel("Flux Density (Jy)")
            axs[x,y].set_xlabel("Frequency (MHz)")
            axs[x,y].set_title(str(emission_line_df.iat[i,0])+" "+str(emission_line_df.iat[i,1])+" MHz")                        #first index shows the name in the data frame
            
            axs[x,y].set_xticks(np.arange(round(frequency[range_bounds[0]]),round(frequency[range_bounds[1]]+1) , 0.5))         # sets up x ticks for the frequency                                                                                   
            axs[x,y].set_xlim(frequency[range_bounds[0]],frequency[range_bounds[1]])                                            # sets limit given the range bounds
            axs[x,y].set_ylim(-8*r_sigma,14*r_sigma)                                                                            # uses r_sigma value to determine sigma value
            axs[x,y].minorticks_on()
    
            #drawing vertical and horizontal lines due to sigma and emission_line of interest
            axs[x,y].axvline(x=emission_line_df.iat[i,1],color='red',linestyle="--",linewidth =1)
            axs[x,y].axhline(y=0,color="black",linestyle="-",linewidth =1)
            axs[x,y].axhline(y=round(3*r_sigma,3),color="green",linestyle="--",linewidth =1)
            axs[x,y].axhline(y=round(5*r_sigma,3),color="green",linestyle="--",linewidth =1)
            axs[x,y].axhline(y=round(-3*r_sigma,3),color="green",linestyle="--",linewidth =1)
            axs[x,y].axhline(y=round(-5*r_sigma,3),color="green",linestyle="--",linewidth =1)
            
            axs2=axs[x,y].twinx() #setting up for y axis in the same plot
            axs3=axs[x,y].twiny() #setting up for the x axis on the plot
    
            #setting up the tick labels and limit for the y axis to the right
            axs2.set_yticks([round(-5*r_sigma,3),round(-3*r_sigma,3),round(3*r_sigma,3),round(5*r_sigma,3)])        
            axs2.set_yticklabels(["-5\u03C3","-3\u03C3","3\u03C3","5\u03C3"])
            axs2.set_ylim(-8*r_sigma,14*r_sigma)
            axs2.tick_params(axis='y', colors='green')
            
            #setting up the labels and axis for the x axis on the top (dopple velocity)
            axs3.set_xticks(np.arange(-150,160,50))
            axs3.set_xlim(v[0],v[len(v)-1])
            axs3.set_xlabel("Source Velocity km/s")
    
            #Setting up the legend of the sigma values
            axs[x,y].text(frequency[range_bounds[0]]+0.05,12*r_sigma,"3\u03c3 = "+str(round(3*r_sigma*1E3,3))+" mJy",color='blue')
            axs[x,y].text(frequency[range_bounds[0]]+0.05,13*r_sigma,"\u03c3 = "+str(round(r_sigma*1E3,3))+" mJy",color='blue')
            
            #plotting the data on on the graph
            axs[x,y].plot(frequency[range_bounds[0]:range_bounds[1]],Intensity[range_bounds[0]:range_bounds[1]]-trend_line_Intensity,color="black",linewidth =0.7) #plot the frequency and the intensity - the trendline
            i=i+1     #counter    
    
    end=time.time()                 #Store ending time stamp 
    fig.figure.savefig(Outfile)     #Saves the figure in the specific directory 
    print("Time it took to generate figure is: "+str(end-start)+" s")    #prints the time it took to compute 