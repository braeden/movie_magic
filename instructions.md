## Required Packages:

- VLC
- ImageMagick
- Plus dependencies 


**Tested with Linux, should work universally**

## Capture the intital frames: 

`vlc /path/to/movie/file --video-filter=scene --vout=dummy --scene-ratio=250 --scene-path="/home/user/Pictures/folder/"`

- `scene-ratio` is how many frames VLC will wait until capturing another image, 
  - ex. at 24FPS, 240 would be 10 seconds
- `scene-path` is the folder location that the images will be stores in
- **You can speed up the VLC window using the `]` key, but too much speed will cause it to drop frames**
- **Don't use the same directory for input and output**

## Shave the images down to a small strips:

`mogrify -path /output/folder/path -shave 49%x0 /input/folder/path/*.png`

- `-path` flag is followed by the folder path to output the cropped frames to
- `-shave` flag is followed by a percentage or # of pixels to crop from the `HORIZONTALxVERTICAL`
 - Depending on the frame size, you may want to use a percentage like `49.95%` to crop in smaller
- Last file path is for the input frames, same folder you used as VLC output

## Combine strips horizontally for final image:

`convert +append /input/folder/with/strips/*.png /home/user/Pictures/output.png`

- `+append` appends horizontally
- First path is the input, and selects all of the PNGs in that folder, should contain all of the strips
- Second path is a single image output
