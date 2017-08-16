import os
import sys
import argparse

parser = argparse.ArgumentParser(
	description="Automates the creation of strips and slices for movies",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter
	epilog="This program is built for Linux, may work for other OSes. All extranous folders can  be deleted after completion. Program retains the Image folder for speed if possible.")

parser.add_argument("filepath", help="MUST BE SURROUNDED IN SINGLE QUOTES. Use the filepath to access your video for processing, eg. /path/to/file.mp4 or file.mp4")

parser.add_argument("-v", "--vertical", help="Change outputs to slice and combine vertically",
                    action="store_true", default=False)
parser.add_argument("-l, --largestrip", help="Large axis dimensions of color strips", 
					action="store", default='900', dest="largestrip")
parser.add_argument("-s, --smallstrip", help="Small axis dimensions of color strips", 
					action="store", default='2', dest="smallstrip")
parser.add_argument("-f, --frames", help="How many frames to wait for each image capture. You must delete the Image folder if it is not the 1st time the program has been run on a file. ex. 240 at 24fps = 10sec", 
					action="store", default='250', dest="frames")
parser.add_argument("-p, --percent", help="How much each side of each frame is cropped in. Requires a percent symbol.", 
					action="store", default='49.93', dest="percent")

args = parser.parse_args()

#How many frames to wait for each image capture, ex. 240 at 24fps = 10sec
frame_delay = args.frames # You'll need to delete the "Images" folder for this to take effect

#Individual color strip size
#One axis resolution is determined by strip_x*frames-captured
strip_x = args.smallstrip   #Values swapped when vertical is choosen
strip_y = args.largestrip #0
#How much frame is cropped for slices *2
#Recommend only editing slice_percent_x
slice_percent_x = args.percent+"%" #Values swapped when vertical is choosen
slice_percent_y = "0%" 	   #

#Other variable presets
append_command = "+append"
filename_suffix = "horizontal"

if os.path.isfile(args.filepath.replace("\\","")):
	print(args.filepath)
	path, filename = os.path.split(args.filepath) #  Tuple for spltting before and after last "/" ini path 
else:
	print("Please use a correct file path")
	exit()

if args.vertical:
	strip_x, strip_y = strip_y, strip_x
	slice_percent_x, slice_percent_y = slice_percent_y, slice_percent_x
	append_command = "-append"
	filename_suffix = "vertical"

directories = ['Images', 'Colors', 'Slices', 'Strips'] # Storage folder names, can be changed

directories = [os.path.join(path, name) for name in directories] # Using list comprehension to change directories to contain the full filepath

#Create directories if they don't exist
for i, name in enumerate(directories): 
	if not os.path.exists(name.replace("\\","")): #Gets rid of necessary bash escapes for python
		os.makedirs(name.replace("\\",""))

#Capture frames from source
if not os.listdir(directories[0].replace("\\","")): #If the folder doesn't already contain a capture - get rid of escaped chars from orignal input
	os.system('ffmpeg -i ' + os.path.join(path, filename) + ' -vf "select=not(mod(n\,' + frame_delay +'))" -vsync vfr ' + os.path.join(directories[0], "scene%04d.png"))

#Create slices
os.system('mogrify -path ' + directories[2] + ' -shave '+ slice_percent_x + 'x' + slice_percent_y + ' ' + os.path.join(directories[0], "*.png"))

#Create 1x1 color averages, then expand them to strip size
os.system('mogrify -path ' + directories[1] + ' -resize 1x1 ' + os.path.join(directories[0], "*.png"))
os.system('mogrify -path ' + directories[3] + ' -resize ' + strip_x + 'x' + strip_y + '! ' + os.path.join(directories[1], "*.png"))

#Create slices output
os.system('convert ' + append_command + ' -colorspace CMY -verbose ' + os.path.join(directories[2], "*.png") + ' ' + os.path.join(path, 'slices_output_' + filename_suffix + '.png'))

#Create strips output
os.system('convert ' + append_command + ' -colorspace CMY -verbose ' + os.path.join(directories[3], "*.png") + ' ' + os.path.join(path, 'strips_output_' + filename_suffix + '.png'))
