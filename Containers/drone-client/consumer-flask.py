import sys
from flask import Flask, Response
from confluent_kafka import Consumer, KafkaError

# Parse args
topic = str(sys.argv[1])

# Build consumer
consumer = Consumer({'group.id': 'capture', 'default.topic.config': {'auto.offset.reset': 'earliest'}})
consumer.subscribe([topic])

app = Flask(__name__)

@app.route('/')

def index():
	return Response(kafkastream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def kafkastream():
	running = True
	frameId = 0
	print('Start of loop')
	while running:
		print('  Polling message')
		msg = consumer.poll(timeout=0.200)
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
	consumer.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
