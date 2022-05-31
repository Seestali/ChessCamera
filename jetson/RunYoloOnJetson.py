import os, torch
from detection.figureAssignment import *
from detection.chessLocalisation import *
from time import sleep

chessboard = None
orientation = 0

##### Setup #####

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt')  # local model
model.conf = 0.25

##### Main #####
# initiate interactive TUI
def mainMenu():
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
            print("Press any key to quit")
            # open camera feed
            c = waitForUserInput()
            print("Closing camera feed...")
            # close camera feed
        elif choice == "2":
            clear_console()
            print("Detecting orientation and chessboard")
            sleep(2)
            # take picture with camera
            #chessboard = setup(image)
            # detectOrientation()
            global chessboard
            chessboard = ChessBoard()
            print("Detection done")
            print("Press any key to return to the main menu")
            c = waitForUserInput()
        elif choice == "3":
            clear_console()
            if chessboard is None:
                print("Please detect the chessboard first")
                print("Press any key to return to the main menu")
                c = waitForUserInput()
            else:
                print("Running detection")
                sleep(2)
                #runDetection()
                print("Detection done")
                print("FEN-String: hier")
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




# 2. case: detect chessboard with figure on A1
# 2.1 case: detection successful
# save chessboard position somewhere
# 2.2 case: detection unsuccessful
# instructions to increase success rate:

# 2.3 case: detect figures on chessboard
# take picture of chessboard with camera feed
# run yolo on picture
# display FEM-String

# wait for user input and return value

