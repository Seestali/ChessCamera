
import os
import torch

from cameraModule.cameraInteractions import *
from detection.chessLocalisation import *
from detection.figureAssignment import *


##### Main #####
# initiate interactive TUI
def mainMenu():
    chessboard = None
    orientation = 0




    while True:
        clear_console()
        print(34*"-")
        print("1. Open Camera feed to adjust placement of chessboard")
        print("2. Detect orientation and chessboard (figure on A1)")
        print("3. Run detection")
        print("4. Exit")
        print(34*"-" + "\n")
        choice = waitForUserInput()
        if choice == "1":
            clear_console()
            print("Opening camera feed...")
            print("Press q or ESC to exit to main menu")
            # open camera feed
            show_camera()
            # close camera feed
            c = waitForUserInput()
            print("Closing camera feed...")
        elif choice == "2":
            clear_console()
            print("Detecting orientation and chessboard")
            captureImage(False)

            # get file from directory
            img = 'jetson/cameraFeed/orientation.jpeg'

            # imread taken frame
            chessboard = setup(img)  # returns the chessboard tiles

            if chessboard is not None:
                print("Chessboard detected")
                model = torch.hub.load('ultralytics/yolov5', 'custom', path='jetson/weights/best.pt')  # local model
                model.conf = 0.25
                clear_console()
                # Inference
                interference = model(img, size=416)
                model = None
                # Assign figure to chessboard
                chessboard = assignFigures(interference, chessboard)
                print("Figures assigned")

                orientation = findRotation(chessboard)
                print("Orientation detected: " + str(orientation * 90))
                print("Remembering orientation")

                print("Chessboard orientation corrected")
                #chessboard.tiles = np.rot90(chessboard.tiles, k=orientation, axes=(1, 0))  # axes=(1,0) ==> 90 deg clockwise; axes(0,1) ==> 90 deg counterclockwise
                draw(chessboard)
                #clear chessboard from setup process
                clear(chessboard)
                print("Press any key to quit to main menu")
                c = waitForUserInput()
            else:
                print("Could not detect chessboard...")
                print("Press any key to quit to main menu")
                c = waitForUserInput()
        elif choice == "3":
            clear_console()
            if chessboard is None:
                print("Please detect the chessboard first")
                print("Press any key to return to the main menu")
                c = waitForUserInput()
            else:
                captureImage(True)
                img = 'jetson/cameraFeed/chessboard.jpeg'
                img = cv2.imread(img)
                image = cv2.resize(img, (416, 416))
                model = torch.hub.load('ultralytics/yolov5', 'custom', path='jetson/weights/best.pt')  # local model
                model.conf = 0.25
                clear_console()
                print("Running detection")
                interference = model(image, size=416)
                model = None
                # Assign figure to chessboard
                chessboard = assignFigures(interference, chessboard)
                chessboard_copy = chessboard
                chessboard_copy.tiles = np.rot90(chessboard_copy.tiles, k=orientation, axes=(1, 0))  # axes=(1,0) ==> 90 deg clockwise; axes(0,1) ==> 90 deg counterclockwise
                print("Detection done")
                print("FEN-String: " + board_to_fen(chessboard_copy))
                clear(chessboard)
                print("Press any key to return to the main menu")
                c = waitForUserInput()
        elif choice == "4":
            print("Exiting")
            break

def waitForUserInput():
    choice = input("Enter your choice: ")
    return choice

def clear_console():
    os.system('clear')

if __name__ == "__main__":
    mainMenu()


