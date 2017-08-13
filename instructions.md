## Required Packages:

- VLC OR FFMEG
- ImageMagick
- Python
- Plus dependencies 


**Tested with Linux, should work universally**

## Capture the intital frames: 
### FFMEG (faster)
`ffmpeg -i /path/to/movie/file.mp4 -vf "select=not(mod(n\,250))" -vsync vfr /path/to/output/scene%04d.png`
- 250 can be replaced with the number of frames you'd like to skip before capturing again
  - ex. at 24FPS, 240 would be 10 seconds
- **Don't use the same directory for input and output**

### VLC (requires extra steps)
`vlc /path/to/movie/file.mp4 --video-filter=scene --vout=dummy --scene-ratio=250 --scene-path="/path/to/output"`

- `scene-ratio` is how many frames VLC will wait until capturing another image, 
  - ex. at 24FPS, 240 would be 10 seconds
- `scene-path` is the folder location that the images will be stores in
- **You can speed up the VLC window using the `]` key, but too much speed will cause it to drop frames**
- **Don't use the same directory for input and output**

## Shave the images down to a small strips:

`mogrify -path /output/folder/path -shave 49.9%x0 /input/folder/path/*.png`

- `-path` flag is followed by the folder path to output the cropped frames to
- `-shave` flag is followed by a percentage or # of pixels to crop from the `HORIZONTALxVERTICAL`
- Depending on the frame size, you may want to use a percentage like `49.95%` to crop in smaller
- Last file path is for the input frames, same folder you used as VLC output

## *ONLY IF USING VLC* - Rename files within directory to ensure that the correct combination order is met:

*Purpose: add a 0 before VLC generated filenames for the lower frame numbers.*
*Must be used to achieve a an ordered slice combination*

*Otherwise, image magick will see "167500.png" before "16800.png" etc.*
*This program will turn 16800.png or scene16800.png into *prefix*016800.png*

1. Download the renaming script:
  
    - `wget https://github.com/braeden123/movie_magic/blob/master/rename_with_zero.py`
    - Or [here](https://raw.githubusercontent.com/braeden123/movie_magic/master/rename_with_zero.py)

2. Open it and edit it:
    - `vim rename_with_zero.py`
    - Edit the path parameters
  
3. Run it and let it rename files:

     - `python rename_with_zero.py`


## Combine strips horizontally for final image:

`convert +append /input/folder/with/strips/*.png /home/user/Pictures/output.png`

- `+append` appends horizontally
- First path is the input, and selects all of the PNGs in that folder, should contain all of the strips
- Second path is a single image output
- **If the final image turns out to be grayscale, try adding the flag `-colorspace RGB` or `colorspace CMY`**
