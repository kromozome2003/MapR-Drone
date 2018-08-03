import sys,traceback,argparse,requests,base64
import tellopy
import av,cv2,numpy
import time
import cStringIO
from requests.utils import quote

kafka_stream_header = {'Content-type': 'application/vnd.kafka.json.v1+json'}
flight_timeout = 10

def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)

def stream_frame(img_data_str):
    frame_stream_url = args.kakfa_rest_gateway + quote(args.kakfa_stream, safe='') + quote(':') + 'frames'
    print('### STREAMING TO: ' + frame_stream_url)
    #frame_payload = '{"records":[{"value":{"img_name":"' + img_name_str + '","img_data":"' + img_data_str + '"}}]}'
    frame_payload = '{"records":[{"value":"' + img_data_str + '"}]}'
    r = requests.post(frame_stream_url, headers=kafka_stream_header, data=frame_payload)
    #print(r)
    #print(r.json())
    print('    Response: ' + str(r))

def main():
    drone = tellopy.Tello()
    try:
        # Subscribe to flight events data
        #drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
        # Set Log_Level
        #drone.set_loglevel(level=drone.LOG_DEBUG)
        # Connect to the drone
        drone.connect()
        drone.wait_for_connection(600.0)
        # Init a video stream
        container = av.open(drone.get_video_stream())
        drone.set_video_encoder_rate(rate=1)
        # Take Off
        #drone.takeoff()
        # Start Chrono
        timeout_start = int(time.time())
        while int(time.time()) < int(timeout_start + flight_timeout):
            for frame in container.decode(video=0):
                # Streaming is ON
                if stream_args:
                    # Store Image name
                    img_name_str = 'frame-%06d.jpg' % frame.index

                    # Convert Bin image to String
                    buffer1 = cStringIO.StringIO()
                    frame.to_image().save(buffer1, format="PNG")
                    img_data_str = base64.b64encode(buffer1.getvalue())
                    #img = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                    #ret, jpeg = cv2.imencode('.png', img)
                    #img_data_bytes = jpeg.tobytes()
                    #buffer = cStringIO.StringIO()
                    #img_data_str = base64.b64encode(buffer.getvalue())

                    print('Elapsed:' + str(int(time.time()-(timeout_start + flight_timeout))) + 'Image name:' + img_name_str + ', String size:' + str(len(img_data_str)))
                    print('### BEGIN DATA STRING ###')
                    print(img_data_str)
                    print('### END DATA STRING ###')

                    stream_frame(img_data_str)

                #time.sleep(0.5)

        print('Flight time expired, landing...')

    except Exception as ex:
        #exc_type, exc_value, exc_traceback = sys.exc_info()
        #traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.land()
        drone.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group('stream')
    group.add_argument('-g', '--kafka-rest-gw', dest='kakfa_rest_gateway', type=str, default='', help='URL of Kafka REST gateway.')
    group.add_argument('-s', '--kafka-stream', dest='kakfa_stream', type=str, default='', help='Kafka stream name.')
    args = parser.parse_args()

    dummy_stream = False
    if args.dummy_stream :
        dummy_stream = True
        print ('Dummy message : On')

    stream_args = False
    if args.kakfa_rest_gateway and args.kakfa_stream :
        stream_args = True
        topic_url = args.kakfa_rest_gateway + quote(args.kakfa_stream, safe='')
        print ('Streaming to topic : ' + str(topic_url))

    main()