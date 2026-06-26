# ItTD-minecraft
Turns images into .mcfunction files that spawn text displays
<img width="1920" height="1080" alt="2026-06-26_11 46 19" src="https://github.com/user-attachments/assets/d7cbd80a-9bb9-47c7-bef2-2ed14e5b6461" />
# Functionality:
* Supports .png and .jpg
* You can change the size of the image(read Usage)
* Fully vanilla(If you add the datapack on a server anybody will be able to see the image)
# Installation:
## Windows:
Unzip the archive and run the ItTD.exe
Put the images in the same folder as the executable and run it. You will be able to choose how many pixels should fit in a width of one block(simply enter the number of pixels) and then the datapack will be ready. Then just put it into the datapacks folder of your world
# Usage:
Use /function ittd:(the name of the image) and the image will be spawned.
Images can be removed by using /kill @e[tag=name of the image]
Also, i highly recommend using the Axiom mod to be able to easily move and rotate the images.
# Limitations:
* No transparency support(transparent pixels will just get their alpha value set to 1)
* Maximum width of an image is around 500 pixels. The only reason it's limited is because of minecraft's command length limitations in datapacks. It can be bypassed by using more .mcfunction files but it's not implemented yet
