from nvidialibs.jetcam.csi_camera import CSICamera
import cv2

camera = CSICamera()
img = camera.read()

while True:
	frame=camera.read()
	cv2.imshow("Cam", frame)
	if cv2.waitKey(1) & 0xFF in (27, ord('q')):
		break

camera.running=False
cv2.destroyAllWindows()



