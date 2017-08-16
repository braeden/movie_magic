# Required Packages:

- VLC or FFMPEG
- ImageMagick
  - Includes `convert` and `mogrify`
- Python
- Plus dependencies 


**Tested with Linux, should work universally with a bit of work**

---------

# Use the automated [script](https://raw.githubusercontent.com/braeden123/movie_magic/master/automate.py)

*Unix only command structure*

1. `wget https://raw.githubusercontent.com/braeden123/movie_magic/master/automate.py` **OR** save it from [here](https://raw.githubusercontent.com/braeden123/movie_magic/master/automate.py)

2. `python automate.py '/movie\ folder/path/FilenameHere.mp4' [-h] [-v] [-l ###] [-s ###] [-f ###] [p ##]`

- Will produce 4 folders and 2 output files
- **The filename/path must use bash escapes AND be surrounded in single quotes.**
- Uses FFmpeg
- **More detailed help is available with the `-h` or `--help` flags.**

---------
# Customize the creation

## Capture the initial frames: 
#### FFmpeg (faster)
`ffmpeg -i /path/to/movie/file.mp4 -vf "select=not(mod(n\,250))" -vsync vfr /path/to/output/scene%04d.png`
- 250 can be replaced with the number of frames you'd like to skip before capturing again
  - ex. at 24FPS, 240 would be 10 seconds
- **Don't use the same directory for input and output**

#### VLC (requires extra steps)
`vlc /path/to/movie/file.mp4 --video-filter=scene --vout=dummy --scene-ratio=250 --scene-path="/path/to/output"`

- `scene-ratio` is how many frames VLC will wait until capturing another image, 
  - ex. at 24FPS, 240 would be 10 seconds
- `scene-path` is the folder location that the images will be stores in
- **You can speed up the VLC window using the `]` key, but too much speed will cause it to drop frames**
- **Don't use the same directory for input and output**

## Option #1 - Shave the images down to a small slices:

`mogrify -path /output/folder/path -shave 49.9%x0 /input/folder/path/*.png`

- `-path` flag is followed by the folder path to output the cropped frames to
- `-shave` flag is followed by a percentage or # of pixels to crop from the `HORIZONTALxVERTICAL`
- Change to `-shave 0x49%` to capture strips **horizonally**
- Depending on the frame size, you may want to use a percentage like `49.95%` to crop in smaller
- Last file path is for the input frames, same folder you used as VLC output

## Option #2 - Shave the images down to single color strips:

`mogrify -path /output/folder/path -resize 1x1 input/folder/path/*.png` 

- Shrinks each frame to 1x1 images, averaging colors

`mogrify -path /output/folder/strips/path -resize 2x900! input/pixel/images/path/*.png`

- Stretches those pixels unto 2x900px strips
- Make the output of the first command become the input directory for the second command
- Change to `-resize 900x2!` to make **horizontal** strips

## *ONLY IF USING VLC* - Rename files within directory to ensure that the correct combination order is met:

*Purpose: add a 0 before VLC generated filenames for the lower frame numbers.*
*Must be used to achieve a an ordered slice combination*

*Otherwise, image magick will see "167500.png" before "16800.png" etc.*
*This program will turn 16800.png or scene16800.png into *prefix*016800.png*

1. Download the renaming script:
  
    - `wget https://github.com/braeden123/movie_magic/blob/master/rename_with_zero.py` **OR** save it from [here](https://raw.githubusercontent.com/braeden123/movie_magic/master/rename_with_zero.py)

2. Open it and edit it:
    - `vim rename_with_zero.py` **OR** use your favorite text editor
    - Edit the path parameters
  
3. Run it and let it rename files:

     - `python rename_with_zero.py`


## Combine strips for final image:

`convert +append /input/folder/with/strips/*.png /home/user/Pictures/output.png`

- `+append` appends horizontally, `-append` appends vertically 
- First path is the input, and selects all of the PNGs in that folder, should contain all of the strips
- Second path is a single image output
- **If the final image turns out to be grayscale, try adding the flag `-colorspace RGB` or `-colorspace CMY`**
