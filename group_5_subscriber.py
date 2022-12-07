import numpy as np
import datetime
import json
import tkinter as tk 
import matplotlib
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class Subscriber():

    def __init__(self,broker,port,topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.x_values = []
        self.y_values = []

    def _pop(self,values,size):
        if (len(values) == size):
            values.pop(0)  

    def append_val(self, topic, msg):        
        timeStamp = msg["Timestamp"]

        # print("Subscriber Timestamp Recived: ", timeStamp)
        element = datetime.datetime.strptime(timeStamp, '%Y/%m/%d-%H:%M:%S')
        # print("Subscriber Timestamp Converted To: dateTime ", element)
        timeAsFloat = element.hour * 3600 + element.minute * 60 + element.second
        # print("Subscriber Timestamp Converted To: float ", timeAsFloat)
            
        self.x_values.append(msg["Timestamp"])
        self.y_values.append(msg["y-value"])


    def on_message(self, client, userdata, message):
        msg = json.loads(message.payload.decode("utf-8"))
        self.append_val(message.topic,msg)
        # print("Received message '" + " '{}' , Timestamp '{}' ".format(str(msg["y-value"]),str(msg["Timestamp"]) ))

    def run(self):
        try:
            self.client = mqtt.Client()
            self.client.connect(self.broker, self.port)
            self.client.subscribe(self.topic)
            self.client.on_message = self.on_message
            self.client.loop_start()
        except:
            print("Connection Failed")
            exit()

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        topics = [("OSCILLATIONS", 0),("AMPLITUDE", 1)]
        self.subscriber = Subscriber("mqtt.eclipseprojects.io", 1883, topics)      

        self.title("Oscillation and Amplitude Graph")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry("1000x1000")

        frame = tk.Frame(self).pack()
        tk.Label(frame, text="Graph page!").pack(padx=10,pady=10)

        figure = Figure((5,5), dpi=100)
        self.graph = figure.add_subplot(111)
        # self.graph.plot([1,2,3,4],[1,2,3,4])

        canvas = FigureCanvasTkAgg(figure,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ani = FuncAnimation(figure, self.animate, interval=1000)

        # # start subscriber
        self.subscriber.run()
    
    def animate(self, i):
        # clear plot
        self.graph.cla()

        # plot data
        self.graph.plot(self.subscriber.x_values, self.subscriber.y_values)    

        #stack x_labels to muiltiple lines
        x_data = list(self.subscriber.x_values)
        dataLen = len(x_data)
        
        print("\n\n\n\n\n")

        if dataLen == 0:            
            return

        x_labels = []              

        if dataLen == 1: # if there is one element just create the label
            x_labels.append(str(x_data[i]).replace('-', '\n')) 
        else:
            x_labels = []
            labelCount = 5       
            lastLabelIndex = dataLen - 1
            labelPositions = []

            # calculate where labels need to be
            for i in range(0, dataLen, max(int(lastLabelIndex/(labelCount - 1)), 1)):            
                labelPositions.append(i)
        
            # set last label position to be the last datapoint in the array
            labelPositions[len(labelPositions) - 1] = lastLabelIndex
            
            # Create labels for x axis
            for i in range(0, dataLen):
                print("index: ", i, ", nextLabelPos: ", labelPositions[0])
                print("labelPositions: ", labelPositions)

                if i == labelPositions[0]: 
                    print("Appending Label at pos ", i)             
                    x_labels.append(str(x_data[i]).replace('-', '\n')) 
                    if len(labelPositions) > 0: # don't pop if last label
                         labelPositions.pop(0)                
                        #  print("labelPositions: ", labelPositions)
                else:
                    x_labels.append("")                   

        self.graph.set_xticks(self.graph.get_xticks())
        self.graph.set_xticklabels(x_labels)   

    def on_closing(self):
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()




            