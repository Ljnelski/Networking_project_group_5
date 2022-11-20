import time
import json
import tkinter as tk 
import matplotlib
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class Subscriber():

    def __init__(self,broker,port,topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.fig, self.ax = plt.subplots(2, 1)
        self.oscillation_values = []
        self.oscillation_timestamps = []
        self.amplitude_values = []
        self.amplitude_timestamps = []
        self.fig, self.ax = plt.subplots(1,2)

    def label_axi(self):

        self.ax[0].set_xlabel("Time")
        self.ax[0].set_ylabel("Oscillations")
        self.ax[0].set_title ("Oscillation Time Graph")
        self.ax[1].set_xlabel("Time")
        self.ax[1].set_ylabel("Amplitude")
        self.ax[1].set_title("Amplitude Time Graph")


    def set_font_plt(self):
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["font.size"] = "7"
        plt.setp(self.ax[0].get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.setp(self.ax[1].get_xticklabels(), rotation=30, horizontalalignment='right')


    def _pop(self,values,size):
        if (len(values) == size):
            values.pop(0)


    def plot_axis(self):
        self.ax[0].plot(self.oscillation_timestamps, self.oscillation_values)
        self.ax[1].plot(self.amplitude_timestamps, self.amplitude_values)


    def animate(self, i):
        # clear axis
        self.ax[0].clear()
        self.ax[1].clear()

        # once values length reaches 5 then remove first element of values and timestamps
        if (len(self.oscillation_values) == 16):
            self.oscillation_values.pop(0)
            self.oscillation_timestamps.pop(0)

        if (len(self.amplitude_values) == 6):
            self.amplitude_values.pop(0)
            self.amplitude_timestamps.pop(0)

        # plot axis of Oscillation
        self.ax[0].plot(self.oscillation_timestamps, self.oscillation_values)

        # plot axis of Amplitude
        self.ax[1].plot(self.amplitude_timestamps, self.amplitude_values)

        # label axis
        self.label_axi()

        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["font.size"] = "7"
        plt.setp(self.ax[0].get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.setp(self.ax[1].get_xticklabels(), rotation=30, horizontalalignment='right')


    def append_val(self,topic,msg):
        if (topic == "OSCILLATIONS"):
            self.oscillation_values.append(msg["y-value"])
            self.oscillation_timestamps.append(msg["Timestamp"])
        if (topic == "AMPLITUDE"):
            self.amplitude_values.append(msg["y-value"])
            self.amplitude_timestamps.append(msg["Timestamp"])


    def on_message(self, client, userdata, message):
        msg = json.loads(message.payload.decode("utf-8"))
        self.append_val(message.topic,msg)
        print("Received message '" + " '{}' , Timestamp '{}' ".format(str(msg["y-value"]),str(msg["Timestamp"]) ))

    def run(self):
        try:
            self.client = mqtt.Client()
            self.client.connect(self.broker, self.port)
            self.client.subscribe(self.topic)
            self.client.on_message = self.on_message
            self.client.loop_start()
            ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)
            plt.show()
        except:
            print("Connection Failed")
            exit()


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        topics = [("OSCILLATIONS", 0),("AMPLITUDE", 1)]
        s = Subscriber("mqtt.eclipseprojects.io", 1883, topics)

       

        self.title("Oscillation and Amplitude Graph")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry("1000x1000")

        # add title 
        self.title = tk.Label(self, text="Oscillation and Amplitude Graph", font=("Times New Roman", 20))
        self.title.pack()


        # get figure and axis from subscriber class
        self.fig = s.fig
        self.ax = s.ax

        # create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # create toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # create button quit customize
        self.button = tk.Button(master=self, text="Quit", command=self.on_closing)
        self.button.pack(side=tk.BOTTOM)

        # start subscriber
        s.run()
    
    def on_closing(self):
        self.quit()
        self.destroy()

    
if __name__ == "__main__":
    app = App()
    app.mainloop()




            