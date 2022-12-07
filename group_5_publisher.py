
import json
import paho.mqtt.client as mqtt
import time
from group_5_dataGenerator import DataGenerator
from datetime import datetime


class Publisher():

    def __init__(self, broker, port, topic) -> None:
        self.broker = broker
        self.port = port
        self.topic = topic
        self.data = {}
        self.dataGenerator = DataGenerator()
        self.publish()   
   
    def createData(self) -> str:

        data = {
            "y-value" : self.dataGenerator.generate_value(),
            "Timestamp" : datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
        }


        data = json.dumps(data, default=str)
        return data

    def publish(self):
        # Created Package
        self.client = mqtt.Client()
        self.client.connect(self.broker,self.port)
        print("Connected to MQTT Broker: " + str(self.broker))
        print("Publishing values to topic: " + self.topic)

        while True:
            package = self.createData()
            try:                        
                self.client.publish(self.topic, package)
                print("Published: " + str(package) + " to topic: " + self.topic)
                time.sleep(1)
            except Exception as e:
                print("Connection Failed:")
                raise e
                exit()


if __name__ == "__main__":
    broker = "mqtt.eclipseprojects.io"
    port = 1883
    topic = "OSCILLATIONS"
    Publisher(broker,port,topic)
