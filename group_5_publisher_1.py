
import numpy as np
import math
import random
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime


class Publisher():

    def __init__(self,broker,port,topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.data = {}
        self.jsonData = ""
        self.value = 0
        self.timestamp = ""
        self.publish()


    def generate_value(self):
        time = np.arange(0,2*math.pi,math.pi/10)
        amplitude = np.sin(time)
        self.value = random.choice(amplitude)
        self.timestamp = datetime.now().strftime('%M:%S.%f')[:-4]
    

    def json_package(self):
          self.data = {
                "y-value" : self.value, 
                "Timestamp" : self.timestamp
            }
    
    def ConvToJson(self):
        self.jsonData = json.dumps(self.data,default=str)
    
    
    def publish(self):
        try:
            self.client = mqtt.Client()
            self.client.connect(self.broker,self.port)
            print("Connected to MQTT Broker: " + str(self.broker))
            print("Publishing values to topic: " + self.topic)
            while True:
                self.generate_value()
                self.json_package()
                self.ConvToJson()
                self.client.publish(self.topic,self.jsonData)
                print("Published: " + str(self.jsonData) + " to topic: " + self.topic)
                time.sleep(1)
        except:
            print("Connection Failed")
            exit()


if __name__ == "__main__":
    broker = "mqtt.eclipseprojects.io"
    port = 1883
    topic = "AMPLITUDE"
    Publisher(broker,port,topic)

    