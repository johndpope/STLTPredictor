import cv2
import glob
import sys
import os


faceDet = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
faceDet_two = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_alt2.xml")
faceDet_three = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_alt.xml")
faceDet_four = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_alt_tree.xml")

#emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Define emotions

#img_arg = sys.argv[1]
#img_arg2 = sys.argv[2]

def extract(path_to_img, path_to_output):
    files = glob.glob("%s" % path_to_img) #Get list images at location
    #print "files: ", files

    directory = '/'.join(path_to_output.split('/')[:-1])
    #print "create directory:", directory
    if not os.path.exists(directory):
	os.makedirs(directory)

    for f in files:
	#print "f: ", f
	#print "f[-1]", f.split('/')[-1]

	frame = cv2.imread(f) #Open image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Convert image to grayscale

	#Detect face using 4 different classifiers
        face = faceDet.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        face_two = faceDet_two.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        face_three = faceDet_three.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        face_four = faceDet_four.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

        #Go over detected faces, stop at first detected face, return empty if no face.
        if len(face) == 1:
            facefeatures = face
        elif len(face_two) == 1:
            facefeatures = face_two
        elif len(face_three) == 1:
            facefeatures = face_three
        elif len(face_four) == 1:
            facefeatures = face_four
        else:
            facefeatures = ""
        
        #Cut and save face
        for (x, y, w, h) in facefeatures: #get coordinates and size of rectangle containing face
            #print "face found in file: %s" %f
            gray = gray[y:y+h, x:x+w] #Cut the frame to size

	    try:
                out = cv2.resize(gray, (350, 350)) #Resize face so all images have same size
		cv2.imwrite("%s" % path_to_output, out) #Write image
                #cv2.imwrite("%s" % (path_to_output, f.split('/')[-1]), out) #Write image
            except:
               	pass #If error, pass file



	if str(facefeatures) == "":
		return facefeatures
	else:
		return path_to_output

#for emotion in emotions: 
#extract(img_arg, img_arg2) #Call

'''
Face extraction was adapted from : http://www.paulvangent.com/2016/04/01/emotion-recognition-with-python-opencv-and-a-face-dataset/ it is used to classify a face on an image and crop it from the image, afterwards it saves the new image of just a face in some directory

'''
