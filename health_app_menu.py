# ==========================================
# Health App Log Analysis
# Pandas + Charts + Menu Driven Program
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Load Data
# -------------------------------

df = pd.read_csv(
    "health_logs.txt",
    header=None,
    names=["date", "user", "action", "value"]
)

df["date"] = pd.to_datetime(df["date"])

df.loc[df["action"] == "HEART_RATE", "value"] = pd.to_numeric(
    df.loc[df["action"] == "HEART_RATE", "value"]
)

# -------------------------------
# Functions
# -------------------------------

def show_summary():
    total_users = df["user"].nunique()
    success_logins = df[
        (df["action"] == "LOGIN") & (df["value"] == "success")
    ].shape[0]
    avg_hr = df[df["action"] == "HEART_RATE"]["value"].mean()

    print("\n--- Summary Report ---")
    print("Total Users:", total_users)
    print("Successful Logins:", success_logins)
    print("Average Heart Rate:", round(avg_hr, 2))


def user_wise_heart_rate():
    print("\n--- User-wise Average Heart Rate ---")
    result = (
        df[df["action"] == "HEART_RATE"]
        .groupby("user")["value"]
        .mean()
    )
    print(result)


def heart_rate_chart():
    hr_df = df[df["action"] == "HEART_RATE"]

    plt.figure()
    plt.plot(hr_df["date"], hr_df["value"])
    plt.xlabel("Date")
    plt.ylabel("Heart Rate")
    plt.title("Heart Rate Trend")
    plt.show()


def user_heart_rate_bar():
    user_avg = (
        df[df["action"] == "HEART_RATE"]
        .groupby("user")["value"]
        .mean()
    )

    plt.figure()
    user_avg.plot(kind="bar")
    plt.xlabel("User")
    plt.ylabel("Average Heart Rate")
    plt.title("User-wise Average Heart Rate")
    plt.show()


# -------------------------------
# Menu Driven Program
# -------------------------------

while True:
    print("\n===== Health App Log Menu =====")
    print("1. Show Summary")
    print("2. User-wise Heart Rate")
    print("3. Heart Rate Trend Chart")
    print("4. User-wise Heart Rate Bar Chart")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        show_summary()
    elif choice == "2":
        user_wise_heart_rate()
    elif choice == "3":
        heart_rate_chart()
    elif choice == "4":
        user_heart_rate_bar()
    elif choice == "5":
        print("Exiting program...")
        break
    else:
        print("Invalid choice! Try again.")
