"""
Capture frames from a camera using openCV and publish on an MQTT topic.
"""
import time
import os

from delegates.mqtt import get_mqtt_client
from delegates.helpers import pil_image_to_byte_array, get_now_string, get_config
from imutils.video import WebcamVideoStream
from imutils import opencv2matplotlib

from PIL import Image

CONFIG_FILE_PATH = os.getenv("MQTT_CAMERA_CONFIG", "./config/config.yml")
CONFIG = get_config(CONFIG_FILE_PATH)

MQTT_BROKER = CONFIG["mqtt"]["broker"]
MQTT_PORT = CONFIG["mqtt"]["port"]
MQTT_QOS = CONFIG["mqtt"]["QOS"]

MQTT_TOPIC_CAMERA = CONFIG["camera"]["mqtt_topic"]
VIDEO_SOURCE = CONFIG["camera"]["vide_source"]
FPS = CONFIG["camera"]["fps"]


def main():
    client = get_mqtt_client()
    client.connect(MQTT_BROKER, port=MQTT_PORT)
    time.sleep(4)  # Wait for connection setup to complete
    client.loop_start()

    # Open camera
    camera = WebcamVideoStream(src=VIDEO_SOURCE).start()
    time.sleep(2)  # Webcam light should come on if using one

    while True:
        frame = camera.read()
        np_array_RGB = opencv2matplotlib(frame)  # Convert to RGB

        image = Image.fromarray(np_array_RGB)  #  PIL image
        byte_array = pil_image_to_byte_array(image)
        client.publish(MQTT_TOPIC_CAMERA, byte_array, qos=MQTT_QOS)
        now = get_now_string()
        print(f"published frame on topic: {MQTT_TOPIC_CAMERA} at {now}")
        time.sleep(1 / FPS)


if __name__ == "__main__":
    main()
