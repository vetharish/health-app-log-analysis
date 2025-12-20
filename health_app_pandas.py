# ===================================
# Health App Log Analysis - Pandas
# ===================================

import pandas as pd

# -------------------------------
# 1. Load Log File
# -------------------------------

df = pd.read_csv(
    "health_logs.txt",
    header=None,
    names=["date", "user", "action", "value"]
)

# -------------------------------
# 2. Data Cleaning
# -------------------------------

df["date"] = pd.to_datetime(df["date"])

df.loc[df["action"] == "HEART_RATE", "value"] = pd.to_numeric(
    df.loc[df["action"] == "HEART_RATE", "value"]
)

# -------------------------------
# 3. Analysis
# -------------------------------

total_users = df["user"].nunique()

successful_logins = df[
    (df["action"] == "LOGIN") & (df["value"] == "success")
].shape[0]

average_heart_rate = df[df["action"] == "HEART_RATE"]["value"].mean()

# -------------------------------
# 4. User-wise Heart Rate
# -------------------------------

user_avg_hr = (
    df[df["action"] == "HEART_RATE"]
    .groupby("user")["value"]
    .mean()
)

# -------------------------------
# 5. Output
# -------------------------------

print("----- Health App Log Report -----")
print("Total Users:", total_users)
print("Successful Logins:", successful_logins)
print("Average Heart Rate:", round(average_heart_rate, 2))

print("\nUser-wise Average Heart Rate:")
print(user_avg_hr)

# -------------------------------
# 6. Save Cleaned Data
# -------------------------------

df.to_csv("cleaned_health_logs.csv", index=False)
