from datetime import datetime
import ujson
import paho.mqtt.client as mqtt

with open('.credentials') as f:
    credentials = ujson.load(f)


# API document see: https://github.com/eclipse/paho.mqtt.python#subscribe-unsubscribe
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code {result_code}.\t\t{time_stamp}".format(
        result_code=str(rc), time_stamp=get_local_timestamp()))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("network_watchdog_status_topic", 0), ("smart_uv_light_status_topic", 0)])


def get_local_timestamp() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("{topic}\t{payload}\t{time_stamp}".format(
        topic=msg.topic, payload=str(msg.payload), time_stamp=get_local_timestamp()))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=credentials["username"], password=credentials["password"])
client.connect("192.168.1.194", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
