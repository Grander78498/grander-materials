import paho.mqtt.client as mqtt
import time
from datetime import datetime, timedelta
import pandas as pd

ip = '192.168.1.15'
port = 1883

topics = [
    '/devices/wb-msw-v3_21/controls/Current Motion',
    '/devices/wb-msw-v3_21/controls/Temperature',
    '/devices/wb-map12e_23/controls/Ch 1 P L2'
]

current_values = {}
result_json = []

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Успешное подключение к брокеру")
        else:
            print("Не удалось подключиться, код %d\n", rc)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(ip, port)
    return client

def subscribe(client, topic):
    def on_message(client, userdata, msg):
        print(f"Received {msg.payload.decode()} from {msg.topic} topic")
        current_values.update({msg.topic: msg.payload.decode()})

    client.subscribe(topic)
    client.on_message = on_message


def append_json(motion, temperature, power):
    global result_json
    result_json.append({
        'motion': motion,
        'temperature': temperature,
        'power': power,
        'file_time': time.ctime(),
        'case_id': ip.split('.')[-1]
    })


def write_csv():
    df = pd.DataFrame(result_json)
    df.to_csv('data.csv', index=False)


def main():
    client = connect_mqtt()

    for topic in topics:
        subscribe(client, topic)

    client.loop_start()

    end_time = datetime.now() + timedelta(minutes=10)
    time.sleep(1)

    while datetime.now() < end_time:
        motion = current_values.get(topics[0])
        temperature = current_values.get(topics[1])
        power = current_values.get(topics[2])

        append_json(motion, temperature, power)
        time.sleep(5)

    write_csv()
    client.loop_stop()
    print("Данные сохранены в csv в течение 10 минут.")


if __name__ == '__main__':
    main()
