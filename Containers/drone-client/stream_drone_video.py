import argparse, tellopy, av, time, cv2, numpy
from confluent_kafka import Producer

def main():
    drone = tellopy.Tello()
    try:
        # Connect to the drone
        drone.connect()
        drone.wait_for_connection(600.0)
        # Init a video stream
        container = av.open(drone.get_video_stream())
        # Take Off
        #drone.takeoff()
        # Start Chrono
        start_time = int(time.time())
        timeout = True
        # Loop until timeout
        while True:
            for frame in container.decode(video=0):
                # Store Image name
                img_name_str = 'frame-%06d.jpg' % frame.index
                # If streaming
                if stream_args:
                    # Convert frame to image
                    frameIMG = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                    ret, jpeg = cv2.imencode('.png', frameIMG)
                    print('  ###  Streaming frame : ' + img_name_str)
                    producer.produce(topic, jpeg.tobytes())
                    producer.flush()

                # Time control
                elapsed_time = int(time.time() - start_time)
                print('  ##  Elapsed:' + str(elapsed_time) + ' seconds / Image name:' + img_name_str)

                # Check timeout
                if elapsed_time > flight_time:
                    timeout = True
                    break

            # Exit on timeout
            if timeout:
                print('Flight time expired')
                break

    # Catch exceptions
    except Exception as ex:
        #exc_type, exc_value, exc_traceback = sys.exc_info()
        #traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)

    # Clean exit w/landing + disconnect
    finally:
        print('Landing...')
        drone.land()
        print('Disconnecting...')
        drone.quit()


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--duration', dest='duration', default=10, help='Flight time duration.')
    # Argument group for kafka streaming
    group = parser.add_argument_group('stream')
    group.add_argument('-s', '--kafka-stream', dest='kafka_stream', type=str, default='', help='Kafka stream path.')
    group.add_argument('-t', '--kafka-topic', dest='kafka_topic', type=str, default='', help='Kafka topic name.')
    args = parser.parse_args()

    # Duration arg
    if args.duration:
        flight_time = int(args.duration)
        print ('Setting duration to : ' + str(flight_time))

    # Streaming args
    stream_args = False
    if args.kafka_stream and args.kafka_topic:
        stream_args = True
        stream_path = args.kafka_stream
        topic = args.kafka_topic
        producer = Producer({'streams.producer.default.stream': stream_path, 'message.max.bytes': 10000000})
        print ('Streaming to : ' + str(stream_path) + ' On topic : ' + topic)

    # Launch main
    main()
