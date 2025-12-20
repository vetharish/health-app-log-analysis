# ================================
# Health App Log Analysis Project
# Pure Python (NO ML, NO pandas)
# ================================

import re

# -------------------------------
# 1. Read & Parse Log File
# -------------------------------

def read_logs(file_name):
    logs = []

    with open(file_name, "r") as file:
        for line in file:
            match = re.match(r"(.*?),(.*?),(.*?),(.*)", line.strip())
            if match:
                date, user, action, value = match.groups()
                logs.append({
                    "date": date,
                    "user": user,
                    "action": action,
                    "value": value
                })

    return logs


logs = read_logs("health_logs.txt")

# -------------------------------
# 2. Analysis Functions
# -------------------------------

def total_users(logs):
    users = set()
    for log in logs:
        users.add(log["user"])
    return len(users)


def successful_logins(logs):
    count = 0
    for log in logs:
        if log["action"] == "LOGIN" and log["value"] == "success":
            count += 1
    return count


def average_heart_rate(logs):
    rates = []
    for log in logs:
        if log["action"] == "HEART_RATE":
            rates.append(int(log["value"]))

    if len(rates) == 0:
        return 0

    return sum(rates) / len(rates)


# -------------------------------
# 3. Display Results
# -------------------------------

print("----- Health App Log Report -----")
print("Total Users:", total_users(logs))
print("Successful Logins:", successful_logins(logs))
print("Average Heart Rate:", round(average_heart_rate(logs), 2))

# -------------------------------
# 4. User-wise Heart Rate
# -------------------------------

user_heart_rate = {}

for log in logs:
    if log["action"] == "HEART_RATE":
        user = log["user"]
        rate = int(log["value"])

        if user not in user_heart_rate:
            user_heart_rate[user] = []

        user_heart_rate[user].append(rate)

print("\nUser-wise Heart Rate:")
for user in user_heart_rate:
    avg = sum(user_heart_rate[user]) / len(user_heart_rate[user])
    print(user, "->", round(avg, 2))
