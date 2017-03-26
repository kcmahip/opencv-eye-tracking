import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0) #initialize video capture
left_counter=0  #counter for left movement
right_counter=0	#counter for right movement
	
th_value=5   #changeable threshold value 

def thresholding( value ):  # function to threshold and give either left or right
	global left_counter
	global right_counter
	
	if (value<=54):   #check the parameter is less than equal or greater than range to 
		left_counter=left_counter+1		#increment left counter 

		if (left_counter>th_value):  #if left counter is greater than threshold value 
			print 'RIGHT'  #the eye is left
			left_counter=0   #reset the counter

	elif(value>=54):  # same procedure for right eye
		right_counter=right_counter+1

		if(right_counter>th_value):
			print 'LEFT'
			right_counter=0
while 1:
	ret, frame = cap.read()
	cv2.line(frame, (320,0), (320,480), (0,200,0), 2)
	cv2.line(frame, (0,200), (640,200), (0,200,0), 2)
	if ret==True:
		col=frame
		
		frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		pupilFrame=frame
		clahe=frame
		blur=frame
		edges=frame
		eyes = cv2.CascadeClassifier('haarcascade_eye.xml')
		detected = eyes.detectMultiScale(frame, 1.3, 5)
		for (x,y,w,h) in detected: #similar to face detection
			cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)	 #draw rectangle around eyes
			cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)   #draw cross
			cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
			pupilFrame = cv2.equalizeHist(frame[y+(h*.25):(y+h), x:(x+w)]) #using histogram equalization of better image. 
			cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) #set grid size
			clahe = cl1.apply(pupilFrame)  #clahe
			blur = cv2.medianBlur(clahe, 7)  #median blur
			circles = cv2.HoughCircles(blur ,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=7,maxRadius=21) #houghcircles
			if circles is not None: #if atleast 1 is detected
				circles = np.round(circles[0, :]).astype("int") #change float to integer
				print 'integer',circles
				for (x,y,r) in circles:
					cv2.circle(pupilFrame, (x, y), r, (0, 255, 255), 2)
					cv2.rectangle(pupilFrame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
					#set thresholds
					thresholding(x)
					

				

		#frame = cv2.medianBlur(frame,5)
		cv2.imshow('image',pupilFrame)
		cv2.imshow('clahe', clahe)
		cv2.imshow('blur', blur)

		
		if cv2.waitKey(1) & 0xFF == ord('q'):
	       	 break

cap.release()
cv2.destroyAllWindows()
