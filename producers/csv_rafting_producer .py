import json
import time
from kafka import KafkaConsumer, KafkaProducer
from utils.utils_logger import logger

#####################################
# Kafka Configuration
#####################################

KAFKA_SOURCE_TOPIC = "rafting_csv_feedback"
KAFKA_TARGET_TOPIC = "processed_csv_feedback"
KAFKA_BROKER = "localhost:9092"

# Create Kafka Consumer (Reads CSV-Formatted Messages)
consumer = KafkaConsumer(
    KAFKA_SOURCE_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    group_id="csv_producer_group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# Create Kafka Producer (Publishes Processed Messages)
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

#####################################
# Stream CSV Data to New Kafka Topic
#####################################

for message in consumer:
    csv_data = message.value

    # Process data (Example: Mark guide performance status)
    csv_data["status"] = "reviewed"

    # Send processed data to Kafka
    producer.send(KAFKA_TARGET_TOPIC, value=csv_data)
    logger.info(f"✅ Processed and Republished CSV Data: {csv_data}")
    time.sleep(1)  # Simulating real-time processing
