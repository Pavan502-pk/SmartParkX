import cv2

def OBJECT_SIZE():
    # Load the image of the car
    image = cv2.imread("E:\\MAJOR_PROJECT\\OBJECTSIZE\\SAMP\\1.jpg")

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection to the grayscale image
    edges = cv2.Canny(gray, 50, 150)

    # Find the contours of the edges in the image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Get the bounding rectangle of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    # The width of the vehicle is the width of the bounding rectangle
    vehicle_width = w
    
    # Display the width of the vehicle
    #print(vehicle_width)
    return vehicle_width

#OBJECT_SIZE()