import csv
import os
import random

CSV_FILE = "notes.csv"
MAX_NUMBER = 3800


# ---------- Persistence ----------
def initialize_csv():
    if os.path.exists(CSV_FILE):
        return

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["number", "status"])
        for i in range(1, MAX_NUMBER + 1):
            writer.writerow([i, "false"])


def load_data():
    data = {}
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[int(row["number"])] = row["status"] == "true"
    return data


def save_data(data):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["number", "status"])
        for i in range(1, MAX_NUMBER + 1):
            writer.writerow([i, str(data[i]).lower()])


# ---------- Operations ----------
def random_false(data, n):
    false_numbers = [k for k, v in data.items() if not v]
    if n > len(false_numbers):
        print("❌ Not enough false numbers available.")
        return
    result = sorted(random.sample(false_numbers, n))
    print("🎲 Random false numbers:")
    print(result)


def toggle_number(data):
    try:
        num = int(input("Enter number to toggle (1-3800): "))
        if num < 1 or num > MAX_NUMBER:
            raise ValueError
        data[num] = not data[num]
        save_data(data)
        print(f"✅ {num} is now {'TRUE' if data[num] else 'FALSE'}")
    except ValueError:
        print("❌ Invalid number")


def check_status(data):
    try:
        num = int(input("Enter number to check (1-3800): "))
        if num < 1 or num > MAX_NUMBER:
            raise ValueError
        print(f"ℹ️ {num} is {'TRUE' if data[num] else 'FALSE'}")
    except ValueError:
        print("❌ Invalid number")


def show_stats(data):
    true_count = sum(data.values())
    false_count = MAX_NUMBER - true_count
    print("📊 Stats")
    print(f"True : {true_count}")
    print(f"False: {false_count}")


# ---------- UI ----------
def menu():
    print("\n==== Number Tracker App ====")
    print("1. Get random false numbers")
    print("2. Toggle a number")
    print("3. Check number status")
    print("4. Show stats")
    print("5. Exit")
    print()


def main():
    initialize_csv()
    data = load_data()

    menu()
    while True:
        choice = input(">>").strip()

        if choice == "1":
            try:
                n = int(input("How many random false numbers? "))
                random_false(data, n)
            except ValueError:
                print("❌ Enter a valid number")

        elif choice == "2":
            toggle_number(data)

        elif choice == "3":
            check_status(data)

        elif choice == "4":
            show_stats(data)

        elif choice == "5":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()
