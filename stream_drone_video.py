import sys,traceback,argparse,requests,base64
import tellopy
import av
import time
import image
import cStringIO
from requests.utils import quote


kafka_stream_header = {'Content-type': 'application/vnd.kafka.json.v1+json'}

def stream_frame(img_name_str, img_data_str):
    frame_stream_url = args.kakfa_rest_gateway + quote(args.kakfa_stream, safe='') + quote(':') + 'frames'
    print('### STREAMING TO: ' + frame_stream_url)
    frame_payload = '{"records":[{"value":{"img_name":"' + img_name_str + '","img_data":"' + img_data_str + '"}}]}'
    r = requests.post(frame_stream_url, headers=kafka_stream_header, data=frame_payload)
    print(r)
    print(r.json())

def main():
    drone = tellopy.Tello()
    try:
        drone.connect()
        drone.wait_for_connection(120.0)
        container = av.open(drone.get_video_stream())
        # skip first 300 frames
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                # Streaming is ON
                if stream_args:
                    # Store Image name
                    img_name_str = 'frame-%06d.jpg' % frame.index
                    print('### BEGIN NAME STRING ###')
                    print(img_name_str)
                    print('### END NAME STRING ###')
                    # Convert Bin image to String
                    buffer = cStringIO.StringIO()
                    frame.to_image().save(buffer, format="JPEG")
                    img_data_str = base64.b64encode(buffer.getvalue())
                    print('### BEGIN DATA STRING ###')
                    print(img_data_str)
                    print('### END DATA STRING ###')
                    stream_frame(str(img_name_str),str(img_data_str))

                frame_skip = int((time.time() - start_time)/frame.time_base)
                #time.sleep(5)

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
    args = parser.parse_args()

    stream_args = False
    if args.kakfa_rest_gateway and args.kakfa_stream :
        stream_args = True
        topic_url = args.kakfa_rest_gateway + quote(args.kakfa_stream, safe='')
        print ('Streaming to topic : ' + str(topic_url))

    main()
