## imports and decls as in `apriltag_test`

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((5*4,3), np.float32)
objp[:,:2] = np.mgrid[0:4,0:5].T.reshape(-1,2)

objpoints = []
imgpoints = []

try:
  while True:
    frame = cam.read()
    grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(grey, (4,5), None)
#  	if ret:
#      K = cv.calibrateCamera()
#      print(K)
#      fx, fy, cx, cy = K[0,0], K[1,1], K[2,0], K[2,1]
    if ret == True:
        objpoints.append(objp)
 
        corners2 = cv.cornerSubPix(grey,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
 
        # Draw and display the corners
        cv.drawChessboardCorners(frame, (4,5), corners2, ret)
    cv.imshow('Cam', frame)
    if cv.waitKey(1) & 0xFF in (27, ord('q')):
      break
except KeyboardInterrupt:
  ...

ret = cv.calibrateCamera(objpoints, imgpoints, grey.shape[::-1], None, None)
if ret[0]:
  print(ret)
