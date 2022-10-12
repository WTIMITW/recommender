from kafka import KafkaAdminClient
from kafka.admin import NewPartitions

topic = "python_test1"
bootstrap_servers = 'localhost:9092'

admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
topic_partitions = {}
topic_partitions[topic] = NewPartitions(total_count=2)
admin_client.create_partitions(topic_partitions)
