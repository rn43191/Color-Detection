"""
    Recognize Color from an Image using OpenCV and bit of pandas
"""
import argparse
import cv2
import pandas as pd

#declaring global variables
dClicked = False
r = g = b = posX = posY = 0

# Add argurment to get image path through command line
parser = argparse.ArgumentParser()
parser.add_argument('-i', "--image", required=True, help="Path of image for recognition")
args = vars(parser.parse_args())
image_path = args['image']

# Reading image from OpenCV
img = cv2.imread(image_path)
    # cv2.imshow('test', img)
    # cv2.waitKey(5000)

# Reading csv(format) with pandas and load it into the pandas dataframe
index = ["clr", "clrName", "hex", "red", "green", "blue"]
csv = pd.read_csv("color.csv", names=index, header=None)
    # print(csv.head(5))

def click_and_set(event, x, y, flags, param):
    # Triggered on Double Click
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global dClicked, r, g, b, posX, posY
        dClicked = True
        posX = x
        posY = y
        b, g, r = img[y, x]
        r = int(r)
        g = int(g)
        b = int(b)

def getClrName(R, G, B):
    minimum = 10000
    # finding the closest color by comparing the hex values
    for i in range(len(csv)):
        dis = abs(R- int(csv.loc[i, "red"])) + abs(G- int(csv.loc[i, "green"])) + abs(B- int(csv.loc[i, "blue"]))
        if dis <= minimum:
            minimum = dis
            name = csv.loc[i, "clrName"]
    return name

# Create a window for image and set callback func to be called on mouse event
cv2.namedWindow('DoubleClickOnImage')
cv2.setMouseCallback('DoubleClickOnImage', click_and_set)

# driver  loop
while(1):

    cv2.imshow("DoubleClickOnImage", img)
    if dClicked:
        # cv2.rectangle(image, startpoint, endpoint, color, thickness)
        # -1 thickness fills rectangle entirely to make background for displaying name
        cv2.rectangle(img, (20, 20), (750, 62), (b, g, r), -1)

        display = getClrName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType,(optional bottomLeft bool))
        font = cv2.FONT_ITALIC
        cv2.putText(img, display, (50, 50), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
        #For light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, display, (50, 50), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)

        dClicked = False

    # Break the loop when user hits esc key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
