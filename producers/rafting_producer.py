import os
import sys
import time
import pathlib
import json
import subprocess  # <-- Allows running the utility scripts
from dotenv import load_dotenv

# Import Kafka utilities
from utils.utils_producer import (
    verify_services,
    create_kafka_producer,
    create_kafka_topic,
)
from utils.utils_logger import logger

#####################################
# Load Environment Variables
#####################################

load_dotenv()

#####################################
# Function to Run Data Generation Scripts
#####################################

def run_data_generators():
    """
    Run all data generation scripts before starting Kafka producer.
    """
    scripts = [
        "utils_generate_rafting_data.py",
        "utils_generate_river_flow.py",
        "utils_generate_weather_data.py"
    ]

    for script in scripts:
        script_path = pathlib.Path(__file__).parent.joinpath(script)

        if script_path.exists():
            logger.info(f"Generating data using {script_path}...")
            try:
                subprocess.run(["python", str(script_path)], check=True)
                logger.info(f"Data generation successful for {script}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to generate data from {script}: {e}")
                sys.exit(1)
        else:
            logger.error(f"Script {script_path} not found. Exiting.")
            sys.exit(1)

#####################################
# Getter Functions for .env Variables
#####################################

def get_kafka_topic() -> str:
    """Fetch Kafka topic from environment or use default."""
    topic = os.getenv("RAFTING_TOPIC", "rafting_feedback")
    logger.info(f"Kafka topic: {topic}")
    return topic

def get_message_interval() -> int:
    """Fetch message interval from environment or use default."""
    interval = int(os.getenv("RAFTING_INTERVAL_SECONDS", 2))
    logger.info(f"Message interval: {interval} seconds")
    return interval

#####################################
# Set up Paths
#####################################

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
logger.info(f"Project root: {PROJECT_ROOT}")

# Set directory where data is stored
DATA_FOLDER: pathlib.Path = PROJECT_ROOT.joinpath("data")
logger.info(f"Data folder: {DATA_FOLDER}")

# Define the JSON data file
DATA_FILE: pathlib.Path = DATA_FOLDER.joinpath("all_rafting_remarks.json")
logger.info(f"Data file: {DATA_FILE}")

#####################################
# Message Generator
#####################################

def generate_messages(file_path: pathlib.Path):
    """Read from a JSON file and yield messages one by one."""
    while True:
        try:
            logger.info(f"Opening data file: {DATA_FILE}")
            with open(DATA_FILE, "r", encoding="utf-8") as json_file:
                json_data: list = json.load(json_file)

                if not isinstance(json_data, list):
                    raise ValueError(f"Expected a list of JSON objects, got {type(json_data)}.")

                for remark in json_data:
                    yield remark
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}. Exiting.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in file: {file_path}. Error: {e}")
            sys.exit(2)
        except Exception as e:
            logger.error(f"Unexpected error in message generation: {e}")
            sys.exit(3)

#####################################
# Main Function
#####################################

def main():
    """
    Main entry point for the producer:
    - Runs all data generation scripts.
    - Ensures Kafka topic exists.
    - Creates Kafka producer.
    - Streams messages from JSON file to Kafka.
    """

    logger.info("START rafting producer.")

    # Step 1: Run all data generators
    run_data_generators()

    # Step 2: Verify Kafka Services
    verify_services()

    # Fetch .env settings
    topic = get_kafka_topic()
    interval_secs = get_message_interval()

    # Verify JSON data file exists
    if not DATA_FILE.exists():
        logger.error(f"Data file not found: {DATA_FILE}. Exiting.")
        sys.exit(1)

    # Create Kafka producer
    producer = create_kafka_producer(
        value_serializer=lambda x: json.dumps(x).encode("utf-8")
    )
    if not producer:
        logger.error("Failed to create Kafka producer. Exiting...")
        sys.exit(3)

    # Create Kafka topic if it doesn't exist
    try:
        create_kafka_topic(topic)
        logger.info(f"Kafka topic '{topic}' is ready.")
    except Exception as e:
        logger.error(f"Failed to create or verify topic '{topic}': {e}")
        sys.exit(1)

    # Generate and send messages
    logger.info(f"Starting message production to topic '{topic}'...")
    try:
        for message_dict in generate_messages(DATA_FILE):
            producer.send(topic, value=message_dict)
            logger.info(f"Sent message to topic '{topic}': {message_dict}")
            time.sleep(interval_secs)
    except KeyboardInterrupt:
        logger.warning("Producer interrupted by user.")
    except Exception as e:
        logger.error(f"Error during message production: {e}")
    finally:
        producer.close()
        logger.info("Kafka producer closed.")

    logger.info("END rafting producer.")

#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()
