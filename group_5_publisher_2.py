import numpy as np
import paho.mqtt.client as mqtt
from datetime import datetime
import random
import json
import time

class Publisher():
    
    def __init__(self,broker,port,topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.publish()


    def generate_value(self) -> int:
        shape, scale = 2.0, 2.0
        oscillations = np.random.gamma(shape,scale,1)
        self.value = random.choice(oscillations)
        self.timestamp = datetime.now().strftime('%M:%S.%f')[:-4]
    
    
    def json_package(self):
            self.data = {
            "y-value" : self.value, 
            "Timestamp" : self.timestamp
            }
    
    
    def save_json(self):
        self.jsonData = json.dumps(self.data,default=str)
    
    def publish(self):
        try:
            self.client = mqtt.Client("Gamma_Wave_Inside_Sensor")
            self.client.connect(self.broker,self.port)
            print("Connected to MQTT Broker: " + str(self.broker))
            print("Publishing values to topic: " + self.topic)
            while True:
                self.generate_value()
                self.json_package()
                self.save_json()
                self.client.publish(self.topic,self.jsonData)
                print("Published: " + str(self.jsonData) + " to topic: " + str(self.topic))
                time.sleep(1)
        except:
            print("Connection Failed")
            exit()
        time.sleep(2)
        


if __name__ == "__main__":
    broker = "mqtt.eclipseprojects.io"
    port = 1883
    topic = "OSCILLATIONS"
    Publisher(broker,port,topic)
