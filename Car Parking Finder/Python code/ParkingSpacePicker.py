import cv2
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

width, height = 115, 50  # width and height of a single parking space

# Path to the file
file_path = 'CarParkPos'

# Load previously saved parking positions if available
if os.path.exists(file_path):
    with open(file_path, 'rb') as f:
        posList = pickle.load(f)
else:
    posList = []

# Mouse click event handler
def mouseClick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
        print(f"Added position: ({x}, {y})")
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                print(f"Removed position: ({x1}, {y1})")

    # Save the updated positions
    with open(file_path, 'wb') as f:
        pickle.dump(posList, f)
    print(f"Positions saved to {file_path}")

# Function to handle matplotlib events
def onclick(event):
    if event.button == 1:  # Left click
        mouseClick(cv2.EVENT_LBUTTONDOWN, int(event.xdata), int(event.ydata), None, None)
    elif event.button == 3:  # Right click
        mouseClick(cv2.EVENT_RBUTTONDOWN, int(event.xdata), int(event.ydata), None, None)
    update_display()

# Function to update the display
def update_display():
    # Read the image
    img = cv2.imread('C:\\Users\\batla\\OneDrive\\Desktop\\coding\\Car Parking Finder\\parkingimg.png')

    # Draw rectangles on the image based on the positions in posList
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 0), 2)

    # Convert BGR (OpenCV format) to RGB (matplotlib format)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Clear the current plot
    plt.clf()

    # Display the image using matplotlib
    plt.imshow(img_rgb)
    plt.title("Image")
    plt.axis('off')  # Hide the axis
    plt.draw()

# Initial display
fig, ax = plt.subplots()
fig.canvas.mpl_connect('button_press_event', onclick)
update_display()
plt.show()
