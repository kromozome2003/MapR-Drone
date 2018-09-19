import sys
from flask import Flask, render_template, Response
from confluent_kafka import Consumer, KafkaError

# Parse args
#topic = str(sys.argv[1])

# Build consumer
consumer_frames = Consumer({'group.id': 'capture', 'default.topic.config': {'auto.offset.reset': 'earliest'}})
consumer_frames.subscribe(['/demos/drone/drone1:frames'])

consumer_resized = Consumer({'group.id': 'capture', 'default.topic.config': {'auto.offset.reset': 'earliest'}})
consumer_resized.subscribe(['/demos/drone/drone1:resized'])

app = Flask(__name__)

@app.route('/')
def video():
	return render_template('index.html')

@app.route('/video_feed_frames')
def video_feed_frames():
	return Response(kafkastream_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_resized')
def video_feed_resized():
	return Response(kafkastream_resized(), mimetype='multipart/x-mixed-replace; boundary=frame')

def kafkastream_frames():
	running = True
	frameId = 0
	print('Start of loop')
	while running:
		print('  Polling message')
		msg = consumer_frames.poll(timeout=0.200)
		print('  Message obtained')
		if msg is None:
			print('  Message is None')
			continue
		if not msg.error():
			print('  Message is valid, receiving frame ' + str(frameId))
			yield (b'--frame\r\n'
				b'Content-Type: image/png\r\n\r\n' + msg.value() + b'\r\n\r\n')
  		elif msg.error().code() != KafkaError._PARTITION_EOF:
			print('  Bad message')
			print(msg.error())
			running = False
		frameId += 1
	consumer_frames.close()

def kafkastream_resized():
	running = True
	frameId = 0
	print('Start of loop')
	while running:
		print('  Polling message')
		msg = consumer_resized.poll(timeout=0.200)
		print('  Message obtained')
		if msg is None:
			print('  Message is None')
			continue
		if not msg.error():
			print('  Message is valid, receiving frame ' + str(frameId))
			yield (b'--frame\r\n'
				b'Content-Type: image/png\r\n\r\n' + msg.value() + b'\r\n\r\n')
  		elif msg.error().code() != KafkaError._PARTITION_EOF:
			print('  Bad message')
			print(msg.error())
			running = False
		frameId += 1
	consumer_resized.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
