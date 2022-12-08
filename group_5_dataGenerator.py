import numpy as np
import math
import random
import datetime
class DataGenerator():
    
    def __init__(self) -> None:
        self.base = 0
        self.climb = 0.1
        self.randomBase = 0
        self.randomSigma = 2
        self.signAmpHour = 0
        self.signAmpMinute = 10


    def generate_value(self) -> int:
        newValue = 0
        t = int(datetime.datetime.now().timestamp())

        sinMinuteCycleValue = self.signAmpMinute * math.sin(((2 * math.pi)/(60) * t))
        randomValue = random.gauss(self.randomBase, self.randomSigma)

        newValue = randomValue + self.base + sinMinuteCycleValue
        # Adjust base value with climb if its wanted
        self.base = self.base + self.climb

        time = np.arange(0,2*math.pi,math.pi/10)
        amplitude = np.sin(time).tolist()        
        value = random.choice(amplitude)
        return newValue