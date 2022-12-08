# RUNS TWO PUBLISHERS AS THREADS

import threading
from group_5_publisher import Publisher

broker = "mqtt.eclipseprojects.io"
port = 1883
topic1 = "OSCILLATIONS"
topic2 = "AMPLITUDE"

p1 = Publisher(broker, port, topic1)
p2 = Publisher(broker, port, topic2)

t1 = threading.Thread(target=p1.publish)
t2 = threading.Thread(target=p2.publish)

t1.start()
t2.start()