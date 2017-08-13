import os
import sys
#Argument 1 = Movie filename


os.system('mkdir Images Colors Slices Strips')

os.system('ffmpeg -i ' + sys.argv[1] + ' -vf "select=not(mod(n\,250))" -vsync vfr Images/img_%04d.png')

os.system('mogrify -path Slices -shave 49.93%x0 Images/*.png')

os.system('mogrify -path Colors -resize 1x1 Images/*.png; mogrify -path Strips -resize 2x900! Colors/*.png')

os.system('convert +append -colorspace CMY -verbose Slices/*.png ouput1.png')

os.system('convert +append -colorspace CMY -verbose Strips/*.png ouput2.png')
