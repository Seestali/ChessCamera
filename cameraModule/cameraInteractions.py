import cv2
import nanocamera as nano

def captureImage(chessboardIsFound):
    # Create the Camera instance
    camera = nano.Camera(flip=2, width=1280, height=720, fps=1)
    print('CSI Camera ready? - ', camera.isReady())
    if camera.isReady():
            # read the camera image
            frame = camera.read()
            # display the frame
    # close the camera instance
    camera.release()
    # remove camera object
    del camera
    return frame

def show_camera():
    # Create the Camera instance
    camera = nano.Camera(flip=2, width=1280, height=720, fps=30)
    print('CSI Camera ready? - ', camera.isReady())
    while camera.isReady():
        try:
            # read the camera image
            frame = camera.read()
            # display the frame
            cv2.imshow("Video Frame", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break

    # close the camera instance
    camera.release()

    # remove camera object
    del camera