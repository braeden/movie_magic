#ARG 1 = Movie filename
#ARG 2 = Optional "-v" flag for vertical combination

import os
import sys

#How many frames to wait for each image capture, ex. 240 at 24fps = 10sec
frame_delay = "250" # You'll need to delete the "Images" folder for this to take effect

#Individual color strip size
#One axis resolution is determined by strip_x*frames-captured
strip_x = "2"   #Values swapped when vertical is choosen
strip_y = "900" #

#How much frame is cropped for slices *2
#Recommend only editing slice_percent_x
slice_percent_x = "49.93%" #Values swapped when vertical is choosen
slice_percent_y = "0%" 	   #

#Other variable presets
append_command = "+append"
filename_suffix = "horizontal"

if len(sys.argv) > 2:
	if sys.argv[2]=="-v" or sys.argv[2]=="--vertical": #When the vertical flag is used
		strip_x, strip_y = strip_y, strip_x
		slice_percent_x, slice_percent_y = slice_percent_y, slice_percent_x
		append_command = "-append"
		filename_suffix = "vertical"

directories = ['Images', 'Colors', 'Slices', 'Strips']

#Create directories if they don't exist
for name in directories:
	if not os.path.exists(name): 
		os.makedirs(name)

#Capture frames from source
if not os.listdir(directories[0]): #If the folder doesn't already contain a capture
	os.system('ffmpeg -i ' + sys.argv[1] + ' -vf "select=not(mod(n\,' + frame_delay +'))" -vsync vfr ' + directories[0] + '/scene%04d.png')

#Create slices
os.system('mogrify -path ' + directories[2] + ' -shave '+ slice_percent_x + 'x' + slice_percent_y + ' ' + directories[0] + '/*.png')

#Create 1x1 color averages, then expand them to strip size
os.system('mogrify -path ' + directories[1] + ' -resize 1x1 ' + directories[0] + '/*.png')
os.system('mogrify -path ' + directories[3] + ' -resize ' + strip_x + 'x' + strip_y + '! ' + directories[1] +'/*.png')

#Create slices output
os.system('convert ' + append_command + ' -colorspace CMY -verbose ' + directories[2] + '/*.png slices_output_' + filename_suffix + '.png')

#Create strips output
os.system('convert ' + append_command + ' -colorspace CMY -verbose ' + directories[3] + '/*.png strips_output_' + filename_suffix + '.png')
