
import re
import json
import os
from datetime import datetime

FILE = "spam_history.json"

PATTERNS = {
    "prize or reward": r"\b(?:won|winner|prize|lottery|reward|gift|congratulations)\b",
    "urgent language": r"\b(?:urgent|act now|limited time|immediately|hurry)\b",
    "money offer": r"\b(?:free money|cash bonus|earn money|guaranteed income)\b",
    "suspicious action": r"\b(?:click here|verify your account|claim now|send otp|share your password)\b",
    "promotional wording": r"\b(?:exclusive offer|buy now|discount|100% free)\b",
    "web link": r"https?://\S+|www\.\S+"
}

def load_history():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []

def save_history(history):
    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)

def detect_spam(message):
    matches = [
        name
        for name, pattern in PATTERNS.items()
        if re.search(pattern, message, re.IGNORECASE)
    ]

    score = len(matches)

    return ("SPAM" if score >= 2 else "NOT SPAM"), matches

def main():
    history = load_history()

    while True:
        print("\n===== SPAM MESSAGE DETECTOR =====")
        print("1. Check Message")
        print("2. View History")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            message = input("Enter message: ").strip()

            if not message:
                print("Message cannot be empty.")
                continue

            result, matches = detect_spam(message)

            record = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message": message,
                "result": result,
                "matched_rules": matches
            }

            history.append(record)

            print("Result:", result)
            print(
                "Matched rules:",
                ", ".join(matches) if matches else "None"
            )

            try:
                save_history(history)
                print("Saved to", FILE)
            except OSError as error:
                print("Could not save history:", error)

        elif choice == "2":
            if not history:
                print("No history available.")

            for index, record in enumerate(history, 1):
                print(
                    f"{index}. [{record['result']}] "
                    f"{record['message']}"
                )

        elif choice == "3":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
