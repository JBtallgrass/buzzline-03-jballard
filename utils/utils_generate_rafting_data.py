"""
utils_generate_rafting_data.py

Utility for generating synthetic rafting feedback data.

This script generates and saves 170 rafting reviews (150 positive, 20 negative)
from Memorial Day to Labor Day 2024.

Usage:
    from utils.utils_generate_rafting_data import generate_rafting_feedback
    data_file = generate_rafting_feedback()
"""

from datetime import datetime, timedelta
import random
import json
import uuid
import pathlib

# Define rafting guides
GUIDES = ["Jake", "Samantha", "Carlos", "Emily", "Tyler", "Ava", "Liam", "Sophia", "Mason", "Olivia"]

# Define possible rafting trip times
TRIP_TYPES = ["Half Day", "Full Day"]

# Define the date range (Memorial Day 2024 to Labor Day 2024)
MEMORIAL_DAY_2024 = datetime(2024, 5, 27)
LABOR_DAY_2024 = datetime(2024, 9, 2)
DATE_RANGE = (LABOR_DAY_2024 - MEMORIAL_DAY_2024).days

# Define positive customer comments
POSITIVE_COMMENTS = [
    "An absolutely thrilling experience! Would do it again.",
    "Our guide was fantastic, made us feel safe the entire time.",
    "The rapids were intense! Such an adrenaline rush.",
    "A great weekend adventure, I highly recommend it.",
    "Loved the scenery, the river was beautiful.",
    "Best weekend trip I've had in years!",
    "We got completely soaked, but it was worth it!",
    "The guide was so knowledgeable, learned a lot about the river.",
    "Perfect mix of excitement and relaxation.",
    "Had a great time with family, will be back next year.",
]

# Define negative customer comments
NEGATIVE_COMMENTS = [
    "The water was too rough, not what I expected.",
    "Our guide seemed uninterested and didn't engage much.",
    "The equipment was old and worn out.",
    "Too many people on the raft, felt overcrowded.",
    "Not enough instructions given before the trip.",
    "The rapids were too intense for beginners.",
    "Felt unsafe at times, the guide wasn't very reassuring.",
    "Too expensive for what it was.",
    "Expected a longer trip, but it felt too short.",
    "The campsite was poorly maintained.",
]

def generate_rafting_feedback(output_file="data/all_rafting_remarks.json"):
    """
    Generate and save rafting customer feedback.

    Args:
        output_file (str): Path where the JSON file will be saved.

    Returns:
        pathlib.Path: The path to the generated JSON file.
    """
    data_folder = pathlib.Path(output_file).parent
    data_folder.mkdir(exist_ok=True)  # Ensure the directory exists
    data_file = pathlib.Path(output_file)

    # Generate 150 positive and 20 negative comments
    customer_remarks = [
        {
            "comment": random.choice(POSITIVE_COMMENTS),
            "guide": random.choice(GUIDES),
            "uuid": str(uuid.uuid4()),
            "date": (MEMORIAL_DAY_2024 + timedelta(days=random.randint(0, DATE_RANGE))).strftime("%Y-%m-%d"),
            "trip_type": random.choice(TRIP_TYPES),
            "timestamp": datetime.utcnow().isoformat(),
            "is_negative": False,
        }
        for _ in range(150)
    ] + [
        {
            "comment": random.choice(NEGATIVE_COMMENTS),
            "guide": random.choice(GUIDES),
            "uuid": str(uuid.uuid4()),
            "date": (MEMORIAL_DAY_2024 + timedelta(days=random.randint(0, DATE_RANGE))).strftime("%Y-%m-%d"),
            "trip_type": random.choice(TRIP_TYPES),
            "timestamp": datetime.utcnow().isoformat(),
            "is_negative": True,
        }
        for _ in range(20)
    ]

    # Save to a JSON file
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(customer_remarks, f, indent=4)

    # Log file creation
    print(f"Rafting feedback data saved to {data_file}")

    return data_file  # Return the path for use in other scripts
