"""
rafting_consumer.py

Consume JSON messages from a Kafka topic related to rafting trips.

This script:
- Logs ALL customer feedback to `rafting_project_log.log`
- Flags negative comments with a red 🛑
- Logs environmental data (weather & river conditions)
"""

#####################################
# Import Modules
#####################################

import os
import json
from collections import defaultdict
from dotenv import load_dotenv

# Import Kafka utilities & logger
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
# Load Weather & River Data
#####################################

def load_json_data(file_path: str) -> dict:
    """Load JSON data from a given file path."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return {entry["date"]: entry for entry in json.load(f)}
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in file: {file_path}")
        return {}

# Load environmental data
WEATHER_DATA_FILE = "data/weather_conditions.json"
RIVER_FLOW_DATA_FILE = "data/river_flow.json"

weather_lookup = load_json_data(WEATHER_DATA_FILE)
river_lookup = load_json_data(RIVER_FLOW_DATA_FILE)

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
        # Parse the JSON string into a Python dictionary
        message_dict: dict = json.loads(message)

        # Extract data
        guide = message_dict.get("guide", "unknown")
        comment = message_dict.get("comment", "No comment provided")
        is_negative = message_dict.get("is_negative", False)
        trip_date = message_dict.get("date", "unknown")

        # Get environmental conditions for this date
        weather = weather_lookup.get(trip_date, {})
        river = river_lookup.get(trip_date, {})

        weather_summary = (
            f"🌤 {weather.get('weather_condition', 'Unknown')} | "
            f"🌡 {weather.get('temperature', 'N/A')}°F | "
            f"💨 Wind {weather.get('wind_speed', 'N/A')} mph | "
            f"🌧 {weather.get('precipitation', 'N/A')} inches rain"
        )

        river_summary = (
            f"🌊 Flow {river.get('river_flow', 'N/A')} cfs | "
            f"📏 Water Level {river.get('water_level', 'N/A')} ft | "
            f"🌡 Water Temp {river.get('water_temperature', 'N/A')}°F"
        )

        # Flag negative comments with a red 🛑
        if is_negative:
            comment = f"🛑 {comment}"
            guide_feedback[guide]["negative"] += 1
            message_dict["weather_summary"] = weather_summary
            message_dict["river_summary"] = river_summary
            negative_feedback_log.append(message_dict)

        else:
            guide_feedback[guide]["positive"] += 1

        # Log ALL feedback
        logger.info(f"📝 Feedback ({trip_date}) | Guide: {guide} | Comment: {comment}")
        logger.info(f"⛅ {weather_summary}")
        logger.info(f"🌊 {river_summary}")

        # Log updated guide performance
        logger.info(f"📊 Updated feedback counts: {dict(guide_feedback)}")

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
        logger.info(f"📂 Negative feedback log saved to {log_file}")


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
    logger.info("🚀 START rafting consumer.")

    # Fetch environment variables
    topic = get_kafka_topic()
    group_id = get_kafka_consumer_group_id()

    # Create the Kafka consumer
    consumer = create_kafka_consumer(topic, group_id)

    # Poll and process messages
    try:
        for message in consumer:
            message_str = message.value
            process_message(message_str)
            log_negative_feedback()
    except KeyboardInterrupt:
        logger.warning("⚠️ Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"❌ Error while consuming messages: {e}")
    finally:
        consumer.close()
        logger.info("✅ Kafka consumer closed.")

#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()
