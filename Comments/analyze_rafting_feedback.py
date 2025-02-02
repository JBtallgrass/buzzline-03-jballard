"""
Analyze rafting feedback data (Positive & Negative) and generate visualizations.

This script:
- Loads both positive & negative feedback from `all_rafting_remarks.json`
- Analyzes guide performance trends for **positive & negative feedback**
- Examines weather & river impact on feedback
- Saves PNG visualizations in the `plots/` folder
"""

import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pathlib
from datetime import datetime

# Set up paths
DATA_FOLDER = pathlib.Path("data")
PLOTS_FOLDER = pathlib.Path("plots")
PLOTS_FOLDER.mkdir(exist_ok=True)  # Ensure plots folder exists

FEEDBACK_FILE = DATA_FOLDER / "all_rafting_remarks.json"  # Now includes both positive & negative feedback

#####################################
# Load and Preprocess Data
#####################################

def load_feedback_data():
    """Load rafting feedback JSON into a Pandas DataFrame."""
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return pd.DataFrame(data)
    except FileNotFoundError:
        print(f"Error: {FEEDBACK_FILE} not found.")
        return pd.DataFrame()
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return pd.DataFrame()

# Load the data
df = load_feedback_data()

if df.empty:
    print("No data available for analysis.")
    exit()

# Convert date columns
df["date"] = pd.to_datetime(df["date"])
df["year_week"] = df["date"].dt.strftime("%Y-W%W")  # Convert to Year-Week format

#####################################
# Data Visualization
#####################################

def save_plot(fig, filename):
    """Save a Matplotlib figure as a PNG file."""
    fig.savefig(PLOTS_FOLDER / filename, dpi=300, bbox_inches="tight")
    print(f"Saved plot: {filename}")

### 📊 1. Guide Performance - Positive vs. Negative Feedback
def plot_guide_performance():
    """Generate bar chart for guide feedback (positive & negative)."""
    guide_counts = df.groupby(["guide", "is_negative"]).size().reset_index(name="count")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="count", y="guide", hue="is_negative", data=guide_counts, palette=["green", "red"], ax=ax)
    ax.set_title("📊 Guide Performance: Positive vs. Negative Feedback")
    ax.legend(title="Feedback Type", labels=["Positive", "Negative"])
    save_plot(fig, "guide_feedback_comparison.png")

### 📈 2. Weekly Trend of Feedback
def plot_weekly_trend():
    """Generate line chart showing trends of positive & negative feedback over time."""
    weekly_trends = df.groupby(["year_week", "is_negative"]).size().reset_index(name="count")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=weekly_trends, x="year_week", y="count", hue="is_negative", marker="o", palette=["green", "red"], ax=ax)
    ax.set_title("📈 Weekly Trend of Positive & Negative Feedback")
    ax.legend(title="Feedback Type", labels=["Positive", "Negative"])
    plt.xticks(rotation=45)
    save_plot(fig, "weekly_feedback_trend.png")

### 🌦️ 3. Weather Impact on Feedback
def plot_weather_impact():
    """Generate a grouped bar plot showing weather conditions' impact on positive & negative feedback."""
    if "weather_summary" in df.columns:
        weather_counts = df.groupby(["weather_summary", "is_negative"]).size().reset_index(name="count")

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x="weather_summary", y="count", hue="is_negative", data=weather_counts, palette=["green", "red"], ax=ax)
        ax.set_title("🌦️ Impact of Weather Conditions on Feedback")
        ax.legend(title="Feedback Type", labels=["Positive", "Negative"])
        plt.xticks(rotation=30, ha="right")
        save_plot(fig, "weather_feedback_comparison.png")

### 🌊 4. River Flow Impact on Feedback
def plot_river_flow_impact():
    """Generate a scatter plot showing river flow vs. feedback (positive & negative)."""
    if "river_summary" in df.columns:
        df["river_flow"] = df["river_summary"].apply(lambda x: float(x.split(" ")[1]) if isinstance(x, str) else None)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x="river_flow", y="guide", hue="is_negative", palette=["green", "red"], ax=ax)
        ax.set_title("🌊 River Flow vs. Guide Feedback")
        ax.legend(title="Feedback Type", labels=["Positive", "Negative"])
        save_plot(fig, "river_flow_feedback_comparison.png")

#####################################
# Execute Analysis
#####################################

if __name__ == "__main__":
    print("🚀 Running Rafting Feedback Analysis...")
    plot_guide_performance()
    plot_weekly_trend()
    plot_weather_impact()
    plot_river_flow_impact()
    print("✅ Analysis complete. Plots saved in 'plots/' folder.")
