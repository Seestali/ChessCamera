import os, torch, cv2
from detection.figureAssignment import *
from detection.chessLocalisation import *
from time import sleep

##### Main #####
# initiate interactive TUI
def mainMenu():
    chessboard = None
    isOriented = False
    orientation = 0


    model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt')  # local model
    model.conf = 0.25

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
            # open camera feed
            print("Press any key to quit to main menu")
            c = waitForUserInput()
            # close camera feed
            print("Closing camera feed...")
        elif choice == "2":
            clear_console()
            print("Detecting orientation and chessboard")
            # TODO: take image with camera and save in directory 'cameraFeed/' as jpeg
            # save with specific filename
            # save resized as 416 x 416! important for model.

            # get file from directory
            img = 'cameraFeed/rotation270.jpeg'
            chessboard = setup(img)  # returns the chessboard tiles

            if chessboard is not None:
                print("Chessboard detected")
                # Inference
                interference = model(img, size=416)
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
                # TODO: take image with camera and save in directory 'cameraFeed/' as jpeg
                # save with specific filename
                # save resized as 416 x 416! important for model.

                # get file from directory
                img = 'cameraFeed/rotation270.jpeg'

                print("Running detection")
                interference = model(img, size=416)
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


