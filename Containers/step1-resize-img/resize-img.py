import sys,io
import StringIO
from random import randint
from PIL import Image
from confluent_kafka import Consumer, KafkaError, Producer

# Parse args
read_topic = str(sys.argv[1])
write_topic = str(sys.argv[2])
target_width = int(sys.argv[3])

print('### Resizing images')

# Build consumer
consumer_group = randint(2000, 2999)
consumer = Consumer({'group.id': consumer_group, 'default.topic.config': {'auto.offset.reset': 'earliest'}})
consumer.subscribe([read_topic])
# Build producer
dst_data = sys.argv[2].split(":")
dst_stream = str(dst_data[0])
dst_topic = str(dst_data[1])
producer = Producer({'streams.producer.default.stream': dst_stream})

running = True
frameId = 0
while running:
	msg = consumer.poll(timeout=1)
	if msg is None: continue
	if not msg.error():
		src_image_data = msg.value()
		src_image = Image.open(io.BytesIO(src_image_data))
		src_width, src_height = src_image.size
		print('Reading from : ' + read_topic + ' Source Image ' + str(frameId) + ' (' + str(src_width) + 'x' + str(src_height) + ')')
		wpercent = (target_width/float(src_image.size[0]))
		hsize = int((float(src_image.size[1])*float(wpercent)))
		dst_image = src_image.resize((target_width,hsize), Image.ANTIALIAS)
		dst_width, dst_height = dst_image.size
		print('   -> Writing to : ' + write_topic + ' Target Size (' + str(dst_width) + 'x' + str(dst_height) + ')')
		dst_image_io = StringIO.StringIO()
		dst_image.save(dst_image_io, format='PNG')
		producer.produce(dst_topic, dst_image_io.getvalue())
		#producer.flush()
 	elif msg.error().code() != KafkaError._PARTITION_EOF:
		print(msg.error())
		running = False
	frameId += 1
#consumer.close()
