import sys,traceback,argparse,requests
import tellopy
import av
import time
import image


kafka_stream_header = {'Content-type': 'application/vnd.kafka.json.v1+json'}

def stream(img_str):
    payload='{"records":[{"value":{'
    payload+='"frame":"' + frame + '"'
    payload += '}}]}'
    r = requests.post(kafka_stream_url, headers=kafka_stream_header, data=payload)
    r
    r.json()

def main():
    drone = tellopy.Tello()
    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        container = av.open(drone.get_video_stream())
        # skip first 300 frames
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                img = frame.to_image()
                img.save('frame-%04d.jpg' % frame.index)
                # Streaming is ON
                if stream_args:
                    stream(str(image))
                frame_skip = int((time.time() - start_time)/frame.time_base)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group('stream')
    group.add_argument('-g', '--kafka-rest-gw', dest='kakfa_rest_gateway', type=str, default='', help='URL of Kafka REST gateway.')
    group.add_argument('-s', '--kafka-stream', dest='kakfa_stream', type=str, default='', help='Kafka stream name.')
    group.add_argument('-t', '--kafka-topic', dest='kakfa_topic', type=str, default='', help='Kafka topic.')
    args = parser.parse_args()

    stream_args = False
    if args.kakfa_rest_gateway and args.kakfa_stream and args.kakfa_topic:
        stream_args = True
        kafka_stream_url = args.kakfa_rest_gateway + quote(args.kakfa_stream, safe='') + quote(':') + args.kakfa_topic
        print ('Streaming to : ' + str(kafka_stream_url))

    main()
