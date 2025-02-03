## 🌊 Rafting Feedback Streaming Project
This project is designed to **stream, process, and analyze real-time customer feedback** from rafting trips on the **French Broad River, NC** using **Apache Kafka**. It integrates customer reviews with **weather and river flow conditions**, providing valuable insights into trip experiences and environmental impacts.

## 📌 Project Overview

### 🎯 Goals
- **Real-time processing** of structured (CSV) and semi-structured (JSON) data.
- **Automated enrichment** of feedback with weather and river conditions.
- **Performance tracking** for rafting guides based on customer reviews.
- **Predictive insights** into trip satisfaction and environmental impact.

### 🚣 Data Sources
- **Customer Feedback**: Reviews from rafting trip participants.
- **Weather Conditions**: Temperature, wind speed, and precipitation.
- **River Flow Levels**: Water level, current speed, and temperature.

### ⚡ Technologies Used
- **Kafka**: Real-time message streaming and processing.
- **Python**: Data generation, transformation, and analytics.
- **VS Code**: Development environment.
- **.env Configurations**: Manage environment variables.

## 🛠️ Setup & Requirements

To set up the project, follow the guides below:

➡️ [Kafka Install Guide](Jballard_docs/kafka-install-guide.md)

Additional setup instructions:
- https://github.com/denisecase/buzzline-01-case
- https://github.com/denisecase/buzzline-02-case

### ✅ Prerequisites
- **Python 3.11+** is required.
- **Kafka & Zookeeper** must be installed and running.

### 📥 Clone or Fork This Project
To get started, copy this project into your GitHub account and rename it to make it your own.

---

## 📄 Project Documentation

For a detailed overview of the project, see:
➡️ [Project Overview](Jballard_docs/project_overview.md)

### 📢 Streaming JSON Data (Rafting Feedback)

**Producer:** Reads rafting feedback and streams it into Kafka.

**Kafka Topic:** `rafting_feedback` _(Configurable in .env)_

### 🔹 Key Consumer Insights
✅ 🛑 Flags negative feedback with a warning emoji.
✅ ⛅ Logs weather conditions (temperature, wind, precipitation).
✅ 🌊 Logs river flow & water levels.
✅ 📜 Saves negative feedback for sentiment analysis.

---

## 📊 Data Processing Workflow

### 🔄 Generating Synthetic Data
To compare rafting experiences with environmental conditions, synthetic data is generated for analysis.

✅ **Rafting Customer Feedback** (Positive & Negative)
✅ **Weather Data** (Temperature, Wind Speed, Rainfall)
✅ **River Flow Data** (Water Level, Flow Rate, Water Temperature)

These datasets are dynamically **loaded into Kafka consumers for real-time analytics**.

### 📌 Understanding the Data

#### 🛑 Logging Negative Feedback
If a customer submits a negative comment, the system logs it along with weather and river conditions.

**Example Negative Review Log:**
```bash
WARNING: Negative feedback for Emily on 2024-07-04: 🛑 Guide was uninterested and barely spoke.
WARNING: ⛅ Sunny | 🌡 85°F | 💨 Wind 10 mph | 🌧 No Rain
WARNING: 🌊 Flow 1200 cfs | 📏 Water Level 3.5 ft | 🌡 Water Temp 68°F
INFO: Negative feedback log saved to negative_feedback.json
```

💡 Now you can analyze patterns! Do negative reviews correlate with bad weather? Does high river flow impact trip satisfaction?

---

## 🔄 Automating Analysis

For automated insights, refer to:
➡️ [Automated Analysis](Jballard_docs/Automate_analysis.md)

## 🚀 Next Steps
📊 **Analyze correlations** between rafting feedback and environmental conditions.
📈 **Visualize** trends using Tableau, Matplotlib, or Pandas.
🧠 **Apply AI techniques** for sentiment analysis or predictive modeling.

➡️ [Automated Analysis](Jballard_docs/Automate_analysis.md)

🚣‍♂️💨 **Enjoy building real-time analytics for adventure tourism!** 🎉

---

## 📜 Disclaimer
This project was developed with the assistance of **Generative AI** to refine and structure original project ideas, ensuring a comprehensive and effective implementation of Kafka-based data streaming.
