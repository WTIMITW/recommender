import pandas as pd
from kafka import KafkaProducer
import time
import datetime
import json
import numpy as np
import mindpandas as mpd
import multiprocessing

KAFKA_HOST = 'localhost'
KAFKA_PORT = 9092
KAFKA_TOPIC = "python_test1"
columns = ['label', *(f'I{i}' for i in range(1, 14)), *(f'C{i}' for i in range(1, 27))]
micro_batch_size = 1000
serializer = lambda v: json.dumps(v).encode('utf-8')
class myProducer():
    def __init__(self, host, port, topic, key_serializer, value_serializer):
        self.host = host
        self.port = port
        self.topic = topic
        self.key_serializer = key_serializer
        self.value_serializer = value_serializer
        bootstrap_servers = '{Kafka_host}:{Kafka_port}'.format(Kafka_host=self.host, Kafka_port=self.port)
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                      key_serializer=self.key_serializer,
                                      value_serializer=self.value_serializer)

    def loopSender(self, val, columns, partition_num):
        self.producer.send(self.topic, key=columns, value=val, partition=partition_num)


def messageSender(host, port, topic, key_serializer, value_serializer, partition_num):
    producer = myProducer(host, port, topic, key_serializer, value_serializer)
    df = pd.read_csv('./output.tsv', sep='\t')
    row, col = df.shape
    matrix = df.values
    for i in range(0, row):
        val = matrix[i].tolist()
        producer.loopSender(val, columns, partition_num)

if __name__ == '__main__':
    try:
        producer1 = multiprocessing.Process(target=messageSender,
                                            kwargs={"host": KAFKA_HOST,
                                                    "port": KAFKA_PORT,
                                                    "topic": KAFKA_TOPIC,
                                                    "key_serializer": serializer,
                                                    "value_serializer": serializer,
                                                    "partition_num": 0})
        producer2 = multiprocessing.Process(target=messageSender,
                                            kwargs={"host": KAFKA_HOST,
                                                    "port": KAFKA_PORT,
                                                    "topic": KAFKA_TOPIC,
                                                    "key_serializer": serializer,
                                                    "value_serializer": serializer,
                                                    "partition_num": 1})
        producer1.start()
        producer2.start()
    except KeyboardInterrupt:
        print("Abort by user")
        producer1.close()
        producer2.close()
