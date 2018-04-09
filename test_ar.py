from __future__ import print_function
import cv2
from ar_markers import detect_markers



print('Press "q" to quit')
capture = cv2.VideoCapture(1)

capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1280)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,720)

if capture.isOpened():  # try to get the first frame
        frame_captured, frame = capture.read()
else:
        frame_captured = False

timer=0
while frame_captured:
	frame_orig = frame.copy();
        markers = detect_markers(frame)
	found=[False,False,False];

        for marker in markers:
                marker.highlite_marker(frame)
		if(marker.id==1):
			found[0]=True
		if(marker.id==3):
			found[1]=True
		if(marker.id==7):
			found[2]=True
	
	if found==[True,True,True]:
		timer = timer +1;
	else:
		timer=0
	
	if timer==3:
		break;

        cv2.imshow('Test Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        frame_captured, frame = capture.read()

for marker in markers:
	print(marker.center,"\n");
	cv2.circle(frame_orig,marker.center,5,(0,0,255),-1)
cv2.imshow('FOUND!',frame_orig)
cv2.waitKey()
# When everything done, release the capture
capture.release()
cv2.destroyAllWindows()
