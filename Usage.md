#Usage
This is a guide parallel to developing.
The content of this file will describe how to use this project.
##Training

Training is done via terminal. The following command is an example of how it is used.
`python3 train.py --batch -1 --batch-size 3 --epochs 300 --img 416 --data ../datasets/Chess-Pieces_big/data.yaml --weights weights/yolov5n.pt`

--data
- ../datasets/Chess-Pieces_big/data.yaml

--weights weights/
- /yolov5n.pt
- /yolov5n6.pt
- /yolov5s.pt
- /yolov5m.pt
- /yolov5l.pt
- /yolov5x.pt
- /yolov5x6.pt


It is recommended to use n or s for nano deployment by official yolov5 developers.
##Export

##Detect
