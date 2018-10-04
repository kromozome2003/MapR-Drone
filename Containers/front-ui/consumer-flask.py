import sys,time
from random import randint
from flask import Flask, render_template, Response
from confluent_kafka import Consumer, KafkaError

# Parse args
topic1 = str(sys.argv[1])
topic2 = str(sys.argv[2])
topic3 = str(sys.argv[3])
#topic1 = '/demos/drone/drone1:frames'
#topic2 = '/demos/drone/drone1:resized'
#topic3 = '/demos/drone/drone1:analyzed'

sleep_time = 0
consumer_group = randint(3000, 3999)

# Build consumer
consumer_frames = Consumer({'group.id': consumer_group, 'default.topic.config': {'auto.offset.reset': 'earliest'}})
consumer_frames.subscribe([topic1])
consumer_resized = Consumer({'group.id': consumer_group, 'default.topic.config': {'auto.offset.reset': 'earliest'}})
consumer_resized.subscribe([topic2])
consumer_analyzed = Consumer({'group.id': consumer_group, 'default.topic.config': {'auto.offset.reset': 'earliest'}})
consumer_analyzed.subscribe([topic3])

app = Flask(__name__)

@app.route('/')
def video():
	return render_template('index.html')

@app.route('/video_feed_frames')
def video_feed_frames():
	return Response(stream_frames(consumer_frames), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_resized')
def video_feed_resized():
	return Response(stream_resized(consumer_resized), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_analyzed')
def video_feed_analyzed():
	return Response(stream_analyzed(consumer_analyzed), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream_frames(consumer):
	running = True
	frameId = 0
	print('Start of loop')
	while running:
		print('  Polling message')
		msg = consumer.poll(timeout=1)
		print('  Message obtained')
		if msg is None:
			print('  Message is None')
			continue
		if not msg.error():
			print('  Message is valid, receiving frame ' + str(frameId))
			yield (b'--frame\r\n' + b'Content-Type: image/png\r\n\r\n' + msg.value() + b'\r\n\r\n')
			time.sleep(sleep_time)
			frameId += 1
  		elif msg.error().code() != KafkaError._PARTITION_EOF:
			print('  Bad message')
			print(msg.error())
			running = False
	#consumer.close()

def stream_resized(consumer):
	running = True
	frameId = 0
	print('Start of loop')
	while running:
		print('  Polling message')
		msg = consumer.poll(timeout=1)
		print('  Message obtained')
		if msg is None:
			print('  Message is None')
			continue
		if not msg.error():
			print('  Message is valid, receiving frame ' + str(frameId))
			yield (b'--frame\r\n' + b'Content-Type: image/png\r\n\r\n' + msg.value() + b'\r\n\r\n')
			time.sleep(sleep_time)
			frameId += 1
  		elif msg.error().code() != KafkaError._PARTITION_EOF:
			print('  Bad message')
			print(msg.error())
			running = False
	#consumer.close()

def stream_analyzed(consumer):
	running = True
	frameId = 0
	print('Start of loop')
	while running:
		print('  Polling message')
		msg = consumer.poll(timeout=1)
		print('  Message obtained')
		if msg is None:
			print('  Message is None')
			continue
		if not msg.error():
			print('  Message is valid, receiving frame ' + str(frameId))
			yield (b'--frame\r\n' + b'Content-Type: image/png\r\n\r\n' + msg.value() + b'\r\n\r\n')
			frameId += 1
			time.sleep(sleep_time)
  		elif msg.error().code() != KafkaError._PARTITION_EOF:
			print('  Bad message')
			print(msg.error())
			running = False
	#consumer.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
