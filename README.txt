To run ChessCamera on Jetson Nano, please use:

python3 RunYoloOnJetson.py

---------
datasets:
contains the different datasets that have been trained and worked with.
"Chess-Pieces_big" is the dataset with which the model has been trained
"Chess-Pieces_check_Accuracy" is the dataset with which the model has been evaluated
"emptyChessBoard" is a dataset with empty chessboard pictures for testing purposes

cameraModule:
contains packages for taking pictures with connected PiCamera

detection:
contains all developed python files for chessboard localisation and figure assignment and reading out csv files

development:
contains development files

jetson:
contains folder for camera feed (saved runtime pictures and test pictures)

yolo5:
contains a fork of yolov5
all the runs are available in folder "runs/train"
