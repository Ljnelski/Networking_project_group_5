import numpy as np
import math
import random

class DataGenerator():
    
    def __init__(self) -> None:
        self.base = 0
        self.climb = 0
        self.randomBase = 0
        self.randomSigma = 0

    def generate_value(self) -> int:

        newValue = 0
        randomValue = random.gauss(self.randomBase, self.randomSigma)
        newValue = randomValue + self.base
        # Adjust base value with climb if its wanted
        self.base = self.base + self.climb

        time = np.arange(0,2*math.pi,math.pi/10)
        amplitude = np.sin(time).tolist()        
        value = random.choice(amplitude)
        return value