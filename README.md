# spectra
Python module that generates a 4x2 detrended spectra figure with 8 spectral lines of interest. Detrended data uses the Savgol fit model. This script was written as part of an ongoing research project at the Planetary Habitability Laboratory.

Functionality:

		Currently the fucntionionality of the emission_line_data variable is disabled. This variable is intented for the user to input a list of interested spectral lines to graph. 

 		Currently the emission lines that are hardcoded are:
	 	OH (hydroxyl) - 1612.231 MHz
		OH (hydroxyl) - 1665.402 MHz
		OH (hydroxyl) - 1667.359 MHz
		OH (hydroxyl) - 1720.530 MHz
		HI (hydrogen) - 1420.406 MHz
		H2CO (formaldehyde) - 1428.685 MHz
		CH3OH (methanol) - 1670.425 MHz
		CH3OH (methanol) - 1616.593 MHz

Functions:
		
		find_bounds( lowlim , uplim , dset ) - returns a tuple of the lower limit index and upper limit index given a dataset 
		spectra_fig( Inputfile , emission_line_data , Outputfile ) - generates a figure given a directory of a csv input file and saves image file in given output directory or directiry of the input file.


Requirements:

		Requieres the following libraries:
			Scipy
	 		Wotan
			time
	 		matplotlib.pyplot
			pandas
			numpy


 Usage:

 		Have the spectra.py in the working directory or python libraries of your IDE
	 	

		Example

		In [1]: import spectra
	
		In [2}: spectra.spectra_fig("C:/User__working_directory/data_file_name.csv")
		Time it took to generate figure is: 0.965... seconds
		# Python matplotlib graph window will open with the figure and it will save an image in the input file directory
	
		In [3]: spectra.spectra_fig("C:/User_working_directory/data_file_name.csv", Outfile="C:/User_working_directory/.../Image_name.png")
		Time it took to generate figure is : 0.8648... seconds 
		#Python matplotlib graph window will open with the figure and it will save an image in the given output directory with given name for image


 
		
	 
	 
