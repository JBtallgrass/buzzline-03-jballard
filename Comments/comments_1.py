from datetime import datetime, timedelta
import random
import json
import uuid
import pathlib

# Define file path for the JSON output
data_folder = pathlib.Path("data")
data_folder.mkdir(exist_ok=True)  # Ensure the directory exists
data_file = data_folder / "all_rafting_remarks.json"

# Define rafting guides
guides = ["Jake", "Samantha", "Carlos", "Emily", "Tyler", "Ava", "Liam", "Sophia", "Mason", "Olivia"]

# Define possible rafting trip times
trip_types = ["Half Day", "Full Day"]

# Define the date range (Memorial Day 2024 to Labor Day 2024)
memorial_day_2024 = datetime(2024, 5, 27)  # Memorial Day (last Monday in May)
labor_day_2024 = datetime(2024, 9, 2)  # Labor Day (first Monday in September)
date_range = (labor_day_2024 - memorial_day_2024).days

# Define positive customer comments
positive_comments = [
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
negative_comments = [
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

# Generate 150 positive and 20 negative comments
customer_remarks = [
    {
        "comment": random.choice(positive_comments),
        "guide": random.choice(guides),
        "uuid": str(uuid.uuid4()),
        "date": (memorial_day_2024 + timedelta(days=random.randint(0, date_range))).strftime("%Y-%m-%d"),
        "trip_type": random.choice(trip_types),
        "timestamp": datetime.utcnow().isoformat(),
        "is_negative": False,
    }
    for _ in range(150)
] + [
    {
        "comment": random.choice(negative_comments),
        "guide": random.choice(guides),
        "uuid": str(uuid.uuid4()),
        "date": (memorial_day_2024 + timedelta(days=random.randint(0, date_range))).strftime("%Y-%m-%d"),
        "trip_type": random.choice(trip_types),
        "timestamp": datetime.utcnow().isoformat(),
        "is_negative": True,
    }
    for _ in range(20)
]

# Save to a JSON file
with open(data_file, "w", encoding="utf-8") as f:
    json.dump(customer_remarks, f, indent=4)

# Confirm file creation
data_file
