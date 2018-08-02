import time
import cv2
from confluent_kafka import Producer
#  connect to Kafka
producer = Producer({'streams.producer.default.stream': '/demos/drone/drone1'})
# Assign a topic
topic = 'frames'

def video_emitter(video):
    # Open the video
    video = cv2.VideoCapture(video)
    print(' emitting.....')

    # read the file
    frameId=0
    while (video.isOpened):
        # read the image in each frame
        success, image = video.read()
        # check if the file has read to the end
        if not success:
            break
        # convert the image png
        ret, jpeg = cv2.imencode('.png', image)
        # Convert the image to bytes and send to kafka
        print('sending frame ' + str(frameId))
	producer.produce(topic, jpeg.tobytes())
        # To reduce CPU usage create sleep time of 0.2sec  
        #time.sleep(0.2)
	frameId += 1
    # clear the capture
    video.release()
    printf('done emitting')

if __name__ == '__main__':
    video_emitter('video.mp4')
