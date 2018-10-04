# MapR-Drone
This project is intended to demonstrate the capabilities of MapR platform to deal with realtime use cases.
What is more realtime than controlling a flying drone ?
What if on top of this use case we decide to process the video stream coming from the drone's camera ?
Let's do it !

## Prerequisites
### A Tello drone ([available on Amazon](https://www.amazon.com/Quadcopter-DJI-Technology-Accessories-Controller/dp/B078YLX1XJ/ref=sr_1_3?ie=UTF8&qid=1538662628&sr=8-3&keywords=tello+drone))
![](/medias/tello-drone.jpg)
### An Intel [NCS](https://movidius.github.io/ncsdk/ncs.html) ([available on Mouser.fr](https://www.mouser.fr/new/Intel/intel-movidius-stick/))
![](/medias/ncs-plugged.jpg)
Check my other project to understand how to [configure Intel NCS into VirtualBox](https://github.com/kromozome2003/MapR-YoloNCS)
### A computer (I use a MacBook Pro 13" with 16G of RAM)
### Docker (CPUs:4, Memory:1.8GiB, Swap:1.0GiB)
![](/medias/docker-version.png)
![](/medias/docker-settings.png)
### A MapR PACC docker image with MapR-ES client installed named : "maprtech/pacc:6.0.1_5.0.0_ubuntu16_yarn_streams"
as the Dockerfile for each container start from this image (MapR PACC created with mapr-setup.sh)
```
wget http://package.mapr.com/releases/installer/mapr-setup.sh
chmod +x mapr-setup.sh
./mapr-setup.sh docker client
```
Respond to the questions as is :
* Image OS class: ubuntu16
* Docker FROM base image name:tag: ubuntu:16.04
* MapR core version: 6.0.1
* MapR MEP version: 5.0.0
* Install Hadoop YARN client: y
* Add POSIX (FUSE) client to container: n
* Add HBase client to container: n
* Add Hive client to container: n
* Add Pig client to container: n
* Add Spark client to container: n
* Add Streams clients to container: y
* MapR client image tag name:  maprtech/pacc:6.0.1_5.0.0_ubuntu16_yarn_streams
* Container network mode:  bridge
* Container memory: 0

### VirtualBox
![](/medias/virtualbox-version.png)
### A MapR Cluster (mine is a single VM v6.0.1 under ubuntu)
I use an ubuntu VM because on iOS (Mac) docker don't allow to share /dev/usb devices (required to detect objects on images).
This is the reason why I decided to detect objects from the MapR cluster itself instead of using one more container w/NCS attached (should work under Linux machine).

## Architecture
![](/medias/mapr-dip-architecture.png)
* Tello drone is acting as an AP (Wifi Access Point + DHCP server)
* Container #1 (drone-client) is controlling the drone using the open source TelloPy project (takeoff + put the drone video stream into a MapR stream (with the Kafka API) + landing)
* Container #2 (step1-resize-img) is resizing every image from the source MapR stream then put the result in a destination MapR stream using kafka API
* Container #3 (step2-detect-obj) which in my case is a VM, is the MapR cluster itself due to iOS limitations. Based on YOLO it reads from the step1-resize-img MapR stream, analyze the objects on the image (using the Intel NCS) then write into another MapR stream using the kafka API
* Container #4 (MapR DSR) is used to explore the data with a zeppelin notebook (see MapR docs for more information about the [Data Science Refinery](https://mapr.com/docs/60/DataScienceRefinery/DataScienceRefineryOverview.html))
* Container #5 (front-ui) is a web server (based on Flask) to display streams results in realtime at the different stages of the DIP (Distributed Image Processing)
Those 3 containers are based on MapR PACC images to consume MapR streams

## Setup the MapR streams
Assuming your MapR cluster/sandbox is up & running w/IP 192.168.56.101 and you have a valid license for streams
Create the required streams & topics for this demo on MapR cluster
We will use the clean-stream.sh script that clean & recreate the streams
```
ssh 192.168.56.101
sudo mkdir -p /mapr/demo.mapr.com/demos/drone
maprcli stream topic delete -path /demos/drone/drone1 -topic frames
maprcli stream topic delete -path /demos/drone/drone1 -topic resized
maprcli stream topic delete -path /demos/drone/drone1 -topic analyzed
maprcli stream topic create -path /demos/drone/drone1 -topic frames
maprcli stream topic create -path /demos/drone/drone1 -topic resized
maprcli stream topic create -path /demos/drone/drone1 -topic analyzed
```
Note : every time you need to empty all streams you can run the clean-stream.sh one more time

## Running the demo
First you will need to get this project on your laptop
```
git clone https://github.com/kromozome2003/MapR-Drone.git
```
Then start each Micro-service in the following order :

### Container #2 (step1-resize-img)
```
cd MapR-Drone/Containers/step1-resize-img
docker build -t step1-resize-img .
./startup.sh
```

### Container #5 (front-ui)
```
cd MapR-Drone/Containers/front-ui
docker build -t front-ui .
./startup.sh
```

### Starting Container #1 (drone-client)
```
cd MapR-Drone/Containers/drone-client
docker build -t drone-client .
./startup.sh
```
* Option 1 : getting the video stream from the drone
* Option 2 : getting the video stream from file (video./mp4)
To change the option, edit the file MapR-Drone/Containers/drone-client/startup.sh

### Container #3 (step2-detect-obj) VM in my case
```
ssh <your MapR cluster>
git clone https://github.com/kromozome2003/MapR-Drone.git
cd MapR-Drone/Containers/step2-detect-obj
python py_examples/object_detection_app.py
```

## Visit the web page to see live streaming from the Drone
[http://localhost:5000/](http://localhost:5000/)
