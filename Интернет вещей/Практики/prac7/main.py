import paho.mqtt.client as mqtt
import time
import json
import xml.etree.ElementTree as ET
import os
import csv
from datetime import datetime, timedelta

ip = '192.168.1.15'
port = 1883

topics = [
    '/devices/wb-msw-v3_21/controls/Current Motion',
    '/devices/wb-msw-v3_21/controls/Sound Level',
    '/devices/wb-msw-v3_21/controls/Illuminance',
    '/devices/wb-msw-v3_21/controls/Temperature',
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


def append_json(motion, sound_level, illuminance, temperature):
    global result_json
    result_json.append({
        'motion': motion,
        'sound_level': sound_level,
        'illuminance': illuminance,
        'temperature': temperature,
        'file_time': time.ctime(),
        'case_id': ip.split('.')[-1]
    })


def write_json():
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(result_json, file, indent=4)


def write_xml():
    root = ET.Element('data')
    for item in result_json:
        data_item = ET.SubElement(root, 'item')
        for key in item:
            value = ET.SubElement(data_item, key)
            value.text = item[key]

    with open('data.xml', 'w', encoding='utf-8') as file:
        file.write(ET.tostring(root, encoding='unicode'))


def main():
    client = connect_mqtt()

    for topic in topics:
        subscribe(client, topic)

    client.loop_start()

    end_time = datetime.now() + timedelta(minutes=1)
    time.sleep(1)

    while datetime.now() < end_time:
        temperature = current_values.get(topics[0])
        humidity = current_values.get(topics[1])
        air_quality = current_values.get(topics[2])
        sound_level = current_values.get(topics[3])

        append_json(temperature, humidity, air_quality, sound_level)
        time.sleep(5)

    write_json()
    write_xml()
    client.loop_stop()
    print("Данные сохранены в XML и JSON файл в течение 1 минуты.")


if __name__ == '__main__':
    main()
