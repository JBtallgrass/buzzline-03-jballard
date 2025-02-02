import subprocess
import pathlib
import sys
from utils.utils_logger import logger  # Ensure logger is set up in utils.utils_logger

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
            logger.info(f"Running data generator: {script_path}")
            try:
                # Run the script and check for errors
                subprocess.run(["python", str(script_path)], check=True)
                logger.info(f"✅ Data generation successful: {script}")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to generate data from {script}: {e}")
                sys.exit(1)  # Exit if a script fails
        else:
            logger.error(f"❌ Script not found: {script_path}. Exiting.")
            sys.exit(1)  # Exit if the script is missing
