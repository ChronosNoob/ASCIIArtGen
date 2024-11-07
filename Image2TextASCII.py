from PIL import Image, ImageFilter

charlist = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'."
clistlen = len(charlist)
#print(clistlen)
split = int(255/clistlen)
thumbsize = 200




def savetxtfile(Text):
    File = open("Output.txt","w") #Makes a new file and saves the string to it for viewing
    File.write(Text)
    File.close()
    return

def getbrightnesschar(lumvalue):
    if isinstance(lumvalue,list) or isinstance(lumvalue,tuple):
        lumvalue = lumvalue[0] # Checks if there are any type errors with the luminance
    #print(lumvalue)
    if lumvalue > 255: #Checks if the luminance is in normal rgb bounds (0-255)
        lumvalue = 255
    elif lumvalue < 0:
        lumvalue = 0

    charval = int(lumvalue/split) #Finds the appropriate character in the ASCII symbol list
    #print(charval)
    if charval > len(charlist):
        charval = len(charlist)
    elif charval < 1:
        charval = 1 
    currentchar = charlist[charval-1] # Adjusts for list offset

    return currentchar
def decodeimage(filepath,ts,edgechoice):
    ImgString = "" # Instantiates a string for the art
    image = Image.open(filepath)
    if  image.height > ts and  image.width > ts:
        image.thumbnail((ts,ts),resample=Image.Resampling.NEAREST)
    #print(image.height)
    #print(image.width)
    #image.resize((thumbsize,image.width*2,resample=Image.Resampling.NEAREST)) # Resizing 
    if image.mode != "L":
        image.convert("L") # Converting to greyscale
    if edgechoice == "y" or edgechoice == "Y" or edgechoice == "Yes" or edgechoice == "yes":
        edgeconverted = image.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8,
                                          -1, -1, -1, -1), 1, 0))
    for y in range(image.height):
        for x in range(image.width): # Loops through each pixel by row
            luminance = image.getpixel((x,y)) #Usually would grab a tuple of values but for grayscale just gets Luminance 
            if edgeconverted:
                if edgeconverted.getpixel((x,y))[0]> 125:
                    bchar = getbrightnesschar(edgeconverted.getpixel((x,y))) # Checks if edge is found
                else: 
                    bchar = getbrightnesschar(luminance)
            else:
                bchar = getbrightnesschar(luminance)
             # Grabs character associated with brightness
            ImgString += bchar + " "
            #print(str(x) + "," + str(y))
        ImgString += "\n" # Creates a newline for the next row

    return ImgString
thumbsize = int(input("Enter the maximum amount of characters per line (above 300 gets freaky): "))
findchoice = input("Do you want edge enhancement?: ")
fp = input("Please enter the path to chosen file: ") #Asks for image filepath
Txt = decodeimage(fp,thumbsize,findchoice) # Processes image
savetxtfile(Txt) # Saves to file


            