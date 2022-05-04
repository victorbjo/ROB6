from dataclasses import replace
import glob
from PIL import Image
import re
def tryint(s):
    try:
        return int(s)
    except:
        return s
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]
def makeGif(frame_folder, gifName, durationParam = 2): #Standard 20fps gif
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
    images = frames = []
    for image in glob.glob(f"{frame_folder}/*.png"):
        images.append(image)
    images.sort(key=alphanum_key)
    print(len(images))
    frames = []
    for idx, image in enumerate(images):
        tempImage = image.replace("\\", "/")
        print(tempImage)
        frames.append(Image.open(tempImage))
        #frames[-1].close()
    frame_one = frames[0]
    fps = int(1000/durationParam)
    frame_one.save(gifName, format="GIF", append_images=frames,
               save_all=True, duration=fps, loop=1)
    print("I made a gif "+gifName)
makeGif("images", "RRT.gif", 10)