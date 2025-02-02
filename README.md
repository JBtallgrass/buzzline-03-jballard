🌊 Rafting Feedback Streaming Project
This project streams and processes customer feedback from rafting trips on the French Broad River, NC using Apache Kafka. It integrates real-time rafting feedback with weather and river flow conditions, providing insights into customer experiences and environmental factors.

📌 Overview

🎯 Goal: Stream structured (CSV) and semi-structured (JSON) data for real-time processing.

🚣 Data Source: Customer rafting feedback, weather conditions, and river flow levels.

⚡ Technologies: Kafka, Python, VS Code, .env Configurations.

📊 Insights: Understand trip satisfaction, guide performance, and impact of environmental conditions.

## 🛠️ Setup & Requirements

The following document outlines the setup tasks

➡️[Kafka Install Guide](Jballard_docs\kafka-install-guide.md)

Tthe following documents provided the detailed setup instructions

https://github.com/denisecase/buzzline-01-case

https://github.com/denisecase/buzzline-02-case

✅ Python 3.11 required.
✅ Kafka & Zookeeper must be installed and running.

➡️ Clone or Fork This Project
Copy this project into your GitHub account and rename it to make it your own.
Example:
 
## 📄 Project Documentation

For a detailed overview of the project, see:

➡️ [Project Overview](Jballard_docs\project_overview.md)

📢 Streaming JSON Data (Rafting Feedback)
 Start the JSON Producer
This producer reads rafting feedback and sends it to Kafka.
✅ Open a terminal and run:

```bash
.venv\Scripts\activate  # Windows
py -m producers.rafting_producer
```

📌 Topic Name: rafting_feedback (See .env for customization.)

🔹 Consumer Insights:
✅ 🛑 Flags negative feedback with a STOP emoji.
✅ ⛅ Logs weather conditions (rain, wind, temperature).
✅ 🌊 Logs river flow & water levels.
✅ 📜 Saves negative comments in negative_feedback.json.

📊 Additional Data Processing
## Generate Weather & River Flow Data
To compare rafting experiences with environmental conditions, generate synthetic data.

    ✅ Generate Weather Data:

    ✅ Generate River Flow Data:

    ✅ Check the Files:🔹 These files are loaded into the consumer for real-time analysis.

## 📌 Understanding the Data

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
 To conduct analysis on generated data please consider the following file

 [Automated Analysis](Jballard_docs\Automate_analysi.md)

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

 [Automated Analysis](Jballard_docs\Automate_analysi.md)





