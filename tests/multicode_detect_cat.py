from nvidialibs.jetcam.csi_camera import CSICamera
import cv2 as cv
import cv2.aruco as aruco
import os
import shutil

dict_names = (
    "DICT_4X4_100",
    "DICT_4X4_250",
    "DICT_5X5_100",
    "DICT_5X5_250",
    "DICT_6X6_250",
    "DICT_7X7_250",
    "DICT_APRILTAG_25H9",
    "DICT_APRILTAG_36H11",
)

dicts = (
    *(aruco.getPredefinedDictionary(getattr(aruco, predef)) for predef in dict_names),
)

cidx = 0
maxidx = len(dicts)

detector = aruco.ArucoDetector(dicts[cidx])

cam = CSICamera(fps=30, capture_width=1280, capture_height=720, width=1280, height=720)

curframe = 0
maxframe = 900
recording = False


def setup_dir(name):
    if not os.path.exists(name):
        os.mkdir(name)

    if not os.path.exists(f"{name}/found"):
        os.mkdir(f"{name}/found")

    if not os.path.exists(f"{name}/none"):
        os.mkdir(f"{name}/none")


setup_dir(dict_names[cidx])

while (key := cv.waitKey(1) & 0xFF, not (key in (27, ord("q"))))[-1]:
    img = cam.read()

    if (key == ord(" ")) and not recording:
        cidx += 1
        cidx %= maxidx
        detector.setDictionary(dicts[cidx])
        name = dict_names[cidx]
        setup_dir(name)

    if (key == ord("p")) and not recording:
        name = dict_names[cidx]
        shutil.rmtree(name, ignore_errors=True)
        setup_dir(name)

    cor, ids, *_ = detector.detectMarkers(img)
    aruco.drawDetectedMarkers(img, cor, ids)

    cv.putText(
        img,
        f"dict={dict_names[cidx]}, {recording=}, frame={curframe}/{maxframe}",
        (0, 10),
        cv.FONT_HERSHEY_PLAIN,
        1,
        (255, 255, 255, 255),
    )

    if (key == ord("r")) and not recording:
        recording = True
        curframe = 1

    if recording and curframe <= maxframe:
        curframe += 1
        suffix = ""
        if ids is not None:
            suffix = f"_{"_".join(str(x) for x in ids)}"
        cv.imwrite(
            f"{dict_names[cidx]}/{"found" if ids is not None else "none"}/{curframe:03}{suffix}.png",
            img,
        )
    elif recording and curframe > maxframe:
        recording = False
        curframe = 0

    cv.imshow("cam", img)
