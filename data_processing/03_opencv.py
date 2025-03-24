import cv2


image=cv2.imread('image/apple.jpg')

cv2.imshow("image",image) # show image

resize_image = cv2.resize(image,(200,100))
cv2.imshow("re-size image",resize_image)


gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("change image color",gray_image)
cv2.imwrite('image/output.jpg',gray_image)  # create image

print(image.shape)      # no.of row and col and dimension
print(resize_image.shape)

cv2.rectangle(image,(200,200),(250,220),(0,0,0),3)
cv2.circle(image, (300, 100), 50, (255, 0, 0), -1)
cv2.line(image, (100, 100), (200, 200), (255, 0, 0), 2)
cv2.imshow("image",image) # show image

# slicing image
image = cv2.imread('image/apple.jpg',cv2.IMREAD_GRAYSCALE)
print(image.shape)
cv2.imshow('image',image)
image[200:300, 200:300] = 255 
cv2.imshow('image',image)

if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
    


# capture image
cap = cv2.VideoCapture(0)
count=0
while True:
    count+=1
    ret, frame = cap.read()
    if not ret:
        break
    if count%10==2:
        cv2.imshow("Webcam Feed", frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



# detect face
# Load the pre-trained Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Capture video from webcam
cap = cv2.VideoCapture(0)  # 0 = Default webcam

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
    print(faces)
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        print(x, y, w, h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)  # Green rectangle

    # Display the frame with detected faces
    cv2.imshow("Live Face Detection", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()