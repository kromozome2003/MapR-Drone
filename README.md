# MapR-Drone
Draft under construction, don't clone/fork yet

# Run PACC w/MapR-ES+POSIX+Python and all libs (Clean)
```
git clone https://github.com/kromozome2003/MapR-Drone.git
cd MapR-Drone
wget http://package.mapr.com/releases/installer/mapr-setup.sh
chmod +x mapr-setup.sh
./mapr-setup.sh docker client
```
* Respond to the questions as is :
* Image OS class: ubuntu16
* Docker FROM base image name:tag: ubuntu:16.04
* MapR core version: 6.0.1
* MapR MEP version: 5.0.0
* Install Hadoop YARN client: y
* Add POSIX (FUSE) client to container: y
* Add HBase client to container: n
* Add Hive client to container: n
* Add Pig client to container: n
* Add Spark client to container: n
* Add Streams clients to container: y
* MapR client image tag name:  maprtech/pacc:6.0.1_5.0.0_ubuntu16_yarn_fuse_streams
* Container network mode:  bridge
* Container memory: 0
```
docker build -t test1 Containers/ubuntu-baseline/
vi docker_images/client/mapr-docker-client.sh
```
* MAPR_CLUSTER=demo.mapr.com
* MAPR_CLDB_HOSTS=192.168.56.101:7222
* MAPR_MOUNT_PATH=/mapr
* MAPR_CONTAINER_USER=mapr
* MAPR_CONTAINER_UID=2000
* MAPR_CONTAINER_PASSWORD=mapr
* LAST LINE —> replace  maprtech/pacc:6.0.1_5.0.0_ubuntu16_yarn_fuse_streams by  test1:latest
```
chmod +x docker_images/client/mapr-docker-client.sh
docker_images/client/mapr-docker-client.sh
```
ONCE IN THE CONTAINER SHELL
```
export LD_LIBRARY_PATH=/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server
python consumer.py
```
    
