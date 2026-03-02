from nvidialibs.jetcam.csi_camera import CSICamera
import cv2 as cv
import numpy as np

FILENAME = "./assets/k.npz"
WITDTH=int(1280/4)
HEIGHT=int(720/4)
CB_W, CB_H = 7, 5

cam = CSICamera(width=WITDTH,height=HEIGHT)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((CB_W*CB_H,3), np.float32)
objp[:,:2] = np.mgrid[0:CB_H,0:CB_W].T.reshape(-1,2)
objp *= 0.032

objpoints = []
imgpoints = []

def main():
  try:
    while len(imgpoints) < 100:
      frame = cam.read()
      grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

      ret, corners = cv.findChessboardCorners(grey, (CB_H, CB_W), None) 

      if ret == True:
          objpoints.append(objp.copy())
          #corners *= 4
          
          corners2 = cv.cornerSubPix(grey, corners, (11,11), (-1,-1), criteria)
          imgpoints.append(corners2)
  
          # Draw and display the corners
          cv.drawChessboardCorners(frame, (CB_H, CB_W), corners2, ret)
      cv.imshow('Cam-calibrate', frame)
      if cv.waitKey(1) & 0xFF in (27, ord('q')):
        break
  except KeyboardInterrupt:
    ...

  ret, K, coef, _, _ = cv.calibrateCamera(objpoints, imgpoints, (CB_H, CB_W), None, None) 
  K=K*4
  K[2,2]=1
  print(K)
  print(coef)
  if ret:
    np.savez(FILENAME,
            cameraMAtrix=K,
            distCoffs=coef,
            imageSize=np.array([1280, 720], dtype=np.int32))

if __name__ == "__main__":
  main()
