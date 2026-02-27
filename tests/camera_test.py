import cv2


gst=("nvarguscamerasrc ! sensor-id=0 ! "
        "nvvidconv ! "
        "videoconvert ! "
		"appsink")
cap = cv2.VideoCapture(gst, cv2.CAP_GSTREAMER)
if not cap.isOpened():
	raise RuntimeError ("Error GStreamer")
while True:
	ret,frame= cap.read()
	if not ret:
		break
	cv2.imshow("camera",frame)
	if cv2.waitKey(1) & 0xFF==27:
			break
cap.release()
cv2.destroyAllWindows()

#nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=640, height=480, format=NV12, framerate=30/1 ! nvvidconv ! video/x-raw, width=640, height=480, format=BGRx ! videoconvert ! autovideosink

 #gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! "video/x-raw(memory:NVMM),width=640,height=480" ! nvvidconv  ! videoconvert ! autovideosink
