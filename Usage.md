#Usage
This is a guide parallel to developing.
The content of this file is will include a series of commands and configurations under which the project has been trained and used.
##Training

`python3 train.py --batch -1 --batch-size 2 --epochs 300 --img 416 --data ../datasets/Chess-Pieces/data.yaml --weights weights/yolov5n.pt`

--data
- ../datasets/Chess-Pieces_big/data.yaml

--weights weights/
- /yolov5s.pt
- /yolov5m.pt
- /yolov5l.pt
- /yolov5x.pt

##Export

##Detect