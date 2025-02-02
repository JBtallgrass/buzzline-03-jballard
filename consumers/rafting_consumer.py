"""
rafting_consumer.py

Consume JSON messages from a Kafka topic related to rafting trips.

The script will:
- Parse JSON messages from Kafka.
- Track positive and negative feedback per guide.
- Log negative feedback for further investigation.
"""

#####################################
# Import Modules
#####################################

import os
import json
from collections import defaultdict
from dotenv import load_dotenv

# Import Kafka utilities
from utils.utils_consumer import create_kafka_consumer
from utils.utils_logger import logger

#####################################
# Load Environment Variables
#####################################

load_dotenv()

#####################################
# Getter Functions for .env Variables
#####################################

def get_kafka_topic() -> str:
    """Fetch Kafka topic from environment or use default."""
    topic = os.getenv("RAFTING_TOPIC", "rafting_feedback")
    logger.info(f"Kafka topic: {topic}")
    return topic


def get_kafka_consumer_group_id() -> str:
    """Fetch Kafka consumer group id from environment or use default."""
    group_id: str = os.getenv("RAFTING_CONSUMER_GROUP_ID", "rafting_group")
    logger.info(f"Kafka consumer group id: {group_id}")
    return group_id


#####################################
# Tracking Data
#####################################

# Track feedback per guide
guide_feedback = defaultdict(lambda: {"positive": 0, "negative": 0})

# Store negative comments for analysis
negative_feedback_log = []

#####################################
# Function to process a single message
#####################################

def process_message(message: str) -> None:
    """
    Process a single JSON message from Kafka.

    Args:
        message (str): The JSON message as a string.
    """
    try:
        # Log the raw message for debugging
        logger.debug(f"Raw message: {message}")

        # Parse the JSON string into a Python dictionary
        message_dict: dict = json.loads(message)

        # Ensure the processed JSON is logged for debugging
        logger.info(f"Processed JSON message: {message_dict}")

        # Ensure it's a dictionary before accessing fields
        if isinstance(message_dict, dict):
            guide = message_dict.get("guide", "unknown")
            comment = message_dict.get("comment", "No comment provided")  # ✅ Fix: Extract comment
            is_negative = message_dict.get("is_negative", False)

            # Process negative feedback with stop sign emoji
            if is_negative:
                comment = f"🛑 {comment}"  # ✅ Fix: Add emoji here safely
                guide_feedback[guide]["negative"] += 1
                negative_feedback_log.append(message_dict)
                logger.warning(f"Negative feedback for {guide}: {comment}")  # ✅ Log with emoji
            else:
                guide_feedback[guide]["positive"] += 1
            
            # Log updated guide performance
            logger.info(f"Updated feedback counts: {dict(guide_feedback)}")

        else:
            logger.error(f"Expected a dictionary but got: {type(message_dict)}")

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON message: {message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")


#####################################
# Save Negative Feedback Log
#####################################

def log_negative_feedback():
    """Save all negative feedback to a separate JSON file for analysis."""
    if negative_feedback_log:
        log_file = "negative_feedback.json"
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(negative_feedback_log, f, indent=4)
        logger.info(f"Negative feedback log saved to {log_file}")


#####################################
# Define main function for this module
#####################################

def main() -> None:
    """
    Main entry point for the consumer.

    - Reads the Kafka topic name and consumer group ID from environment variables.
    - Creates a Kafka consumer.
    - Processes rafting feedback messages from Kafka.
    """
    logger.info("START rafting consumer.")

    # Fetch environment variables
    topic = get_kafka_topic()
    group_id = get_kafka_consumer_group_id()
    logger.info(f"Consumer: Topic '{topic}' and group '{group_id}'...")

    # Create the Kafka consumer
    consumer = create_kafka_consumer(topic, group_id)

    # Poll and process messages
    logger.info(f"Polling messages from topic '{topic}'...")
    try:
        for message in consumer:
            message_str = message.value
            logger.debug(f"Received message at offset {message.offset}: {message_str}")
            process_message(message_str)
            log_negative_feedback()  # ✅ Fix: Log negative feedback **inside the loop** for real-time updates
    except KeyboardInterrupt:
        logger.warning("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")
    finally:
        consumer.close()
        logger.info(f"Kafka consumer for topic '{topic}' closed.")

    logger.info(f"END consumer for topic '{topic}' and group '{group_id}'.")


#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()
