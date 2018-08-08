from flask import Flask, Response
from confluent_kafka import Consumer, KafkaError
consumer = Consumer({'group.id': 'mygroup', 'default.topic.config': {'auto.offset.reset': 'earliest'}})
consumer.subscribe(['/demos/drone/drone1:frames'])

app = Flask(__name__)

@app.route('/')

def index():
	return Response(kafkastream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def kafkastream():
	running = True
	frameId = 0
	while running:
		msg = consumer.poll(timeout=1.0)
		if msg is None: continue
		if not msg.error():
			print('receiving frame ' + str(frameId))
			yield (b'--frame\r\n'
				b'Content-Type: image/png\r\n\r\n' + msg.value() + b'\r\n\r\n')
  		elif msg.error().code() != KafkaError._PARTITION_EOF:
			print(msg.error())
			running = False
		frameId += 1
	consumer.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
