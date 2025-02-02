🌊 Rafting Feedback Streaming Project
This project streams and processes customer feedback from rafting trips on the French Broad River, NC using Apache Kafka. It integrates real-time rafting feedback with weather and river flow conditions, providing insights into customer experiences and environmental factors.

📌 Overview
🎯 Goal: Stream structured (CSV) and semi-structured (JSON) data for real-time processing.
🚣 Data Source: Customer rafting feedback, weather conditions, and river flow levels.
⚡ Technologies: Kafka, Python, VS Code, .env Configurations.
📊 Insights: Understand trip satisfaction, guide performance, and impact of environmental conditions.
🛠️ Setup & Requirements
1️⃣ Install Dependencies
Before starting, ensure you have completed the setup tasks in:

https://github.com/denisecase/buzzline-01-case
https://github.com/denisecase/buzzline-02-case
✅ Python 3.11 required.
✅ Kafka & Zookeeper must be installed and running.

2️⃣ Clone or Fork This Project
Copy this project into your GitHub account and rename it to make it your own.
Example:

📢 Streaming JSON Data (Rafting Feedback)
5️⃣ Start the JSON Producer
This producer reads rafting feedback and sends it to Kafka.
✅ Open a terminal and run:

```bash
.venv\Scripts\activate  # Windows
py -m producers.rafting_producer
```

📌 Topic Name: rafting_feedback (See .env for customization.)

6️⃣ Start the JSON Consumer
The consumer listens for rafting feedback, logs negative comments, and cross-references weather & river flow data.

✅ Open a new terminal and run:

```bash
Copy
Edit
.venv\Scripts\activate  # Windows
py -m consumers.rafting_consumer
```

🔹 Consumer Insights:
✅ 🛑 Flags negative feedback with a STOP emoji.
✅ ⛅ Logs weather conditions (rain, wind, temperature).
✅ 🌊 Logs river flow & water levels.
✅ 📜 Saves negative comments in negative_feedback.json.

📊 Additional Data Processing
7️⃣ Generate Weather & River Flow Data
To compare rafting experiences with environmental conditions, generate synthetic data.

✅ Generate Weather Data:

```bash
python -m utils.utils_generate_weather_data
```

✅ Generate River Flow Data:

```bash
python -m utils.utils_generate_river_flow
```

✅ Check the Files:

```bash
cat data/weather_conditions.json
cat data/river_flow.json
```
🔹 These files are loaded into the consumer for real-time analysis.

🔄 CSV Data Processing (Optional)
This project also supports CSV streaming, similar to the JSON processing.

📌 Understanding the Data
📜 JSON (Rafting Feedback)
Example streaming JSON message:

json
Copy
Edit
{
    "comment": "Loved the rapids, best trip ever!",
    "guide": "Samantha",
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "date": "2024-07-04",
    "trip_type": "Full Day",
    "timestamp": "2024-07-04T14:30:00Z",
    "is_negative": false
}
📜 Weather Data (for Comparison)

```json
{
    "date": "2024-07-04",
    "temperature": 85,
    "weather_condition": "Sunny",
    "wind_speed": 10,
    "precipitation": 0.0
}
📜 River Flow Data (for Comparison)
 ```json
{
    "date": "2024-07-04",
    "river_flow": 1200,
    "water_level": 3.5,
    "water_temperature": 68
}

🛑 Logging Negative Feedback
✅ If a customer submits a negative comment, the consumer logs it with weather & river details.

Example Negative Review Log:

```bash
WARNING: Negative feedback for Emily on 2024-07-04: 🛑 Guide was uninterested and barely spoke.
WARNING: ⛅ Sunny | 🌡 85°F | 💨 Wind 10 mph | 🌧 No Rain
WARNING: 🌊 Flow 1200 cfs | 📏 Water Level 3.5 ft | 🌡 Water Temp 68°F
INFO: Negative feedback log saved to negative_feedback.json
```

💡 Now you can analyze patterns! Are negative reviews more common on stormy days? Are higher river flows linked to safety concerns?

🔄 Resuming Work
Each time you restart your project: 1️⃣ Open the folder in VS Code.
2️⃣ Start Zookeeper & Kafka.
3️⃣ Activate your virtual environment (.venv).
4️⃣ Restart your producer & consumer scripts.

🛠 Saving Disk Space
To free up space, delete your .venv folder when inactive.
To restart, recreate .venv, install dependencies, and continue working seamlessly.

📜 License
This project is open-source under the MIT License.
You are free to modify, fork, and experiment with this code.
See the LICENSE for details.

🚀 Next Steps
📊 Analyze correlations between rafting feedback & environment.
📈 Visualize data using Tableau, Matplotlib, or Pandas.
🧠 Apply AI for sentiment analysis or predictive modeling.
Happy coding! 🚣‍♂️💨 Enjoy building real-time analytics for adventure tourism! 🎉







