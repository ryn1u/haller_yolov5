# Haller YoloV5

To repo jest forkiem orginalnego repot YoloV5 od Ultralytics (<https://github.com/ultralytics/yolov5>)
Odwiedź żeby dowiedzieć się więcej z oficjalnej deokumentacji.

Repo to jest potrzebne w dwóch miejscach:

1. Do tereningów z generatora danych

2. Do inferencji w ROS

## Treningi i generator

Umieść to repo wewnątrz folderu *home/GeneratedDatasets/* .

Aby generator rozpoczął tworzenie obrazów stwórz folder w *GeneratedDatasets* i dodaj w tym folderze plik *request.txt*. Wewnątrz wpisz ilość obrazów do wygenerowania. Foldery oraz pliki request możes tworzyć bez wyłączania generatora :-) .

home
|
|-GeneratedDatasets
|   |-train
|   |   |-request.txt
|   |
|   |-val
|   |   |-request.txt
|   |
|   |-haler_yolov5 (to repo)

**WAŻNE**
Jeżeli tworzysz datasety z obrazami to pamiętaj aby wpisać je do *data/haller.yaml* !!!

Aby uruchomić trening będąc w folderze z repo wpisz komendę:

```
python3 train.py --batch 8 --epochs 10 --data haller.yaml --weights yolov5s6.pt --freeze 12 --imgsz 1280 --project haller --name haller_net
```

Jeśli masz dużo pamięci RAM możesz dodać opcję --cache żeby przyspieszyć trening.

Zmień ilość batchy, epochs oraz parametry --project i --name według uznania.

Po zakonczeniu treningu plik z wagami znajduje się w: *haller_yollov5/(--project)/(--name)/weights/best.pt*

## ROS i YOLO

Wersję pod hallera paczki yolov5_ros dostępna w: https://github.com/ryn1u/yolov5_ros

Umieść to repo w folderze *(nazwa twojego catkin workspace. pewnie HallerSim)/src/yolov5_ros/src/*
Wmieść wewnątrz catkin workspace paczkę detection_msgs pobraną z: https://github.com/mats-robotics/detection_msgs

W tym samym folderze (czyli gdzie znajduje się plik detect.py) umieść plik z najlepszymi wgami *best.py*
Konfigracja poprzez plik *yolov5_ros/launch/yolov5.launch*. Są w tam wypisane nazwy topiców i inne ważne dane.

catkin_ws
|-detection_msgs
|
|-yolov5_ros
|   |-launch
|   |
|   |-src
|   |   |-haller_yolo (to repo)
|   |   |-best.pt
|   |   |-detect.py

**WAŻNE**
Pamiętaj żeby po zgraniu wszytskich paczek użyj comedy ``` catkin_make ``` w folderze workspace!

Aby odpalić yolo z rosem będąc w folderze catkin workspace'u wpisz komendy:

```
source devel/setup.bash
roslaunch yolov5_ros yolov5.launch
```
