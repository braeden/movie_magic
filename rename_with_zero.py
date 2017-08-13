#
#Purpose: add a 0 before VLC generated filenames for the lower frame numbers
#Must be used to achieve a an ordered slice combination
#
#Otherwise, image magick will see "167500.png" before "16800.png" etc.
#This program will turn 16800.png or scene16800.png into *prefix*016800.png
#
import os
path="/home/braeden/Pictures/test2/" #File path with slices
for fileName in os.listdir(path):
	if len(filter(str.isdigit, fileName))==5: #if the # of digits in the filename is equal to 5
		newFileName = fileName[0:-9]+'0'+fileName[-9:-1]+fileName[-1] #append a '0' before the other digits
		os.rename(path+fileName, path+newFileName) # then rename it
