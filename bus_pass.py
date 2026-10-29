import os
from datetime import date, timedelta

FILE_NAME = "buspass.txt"
FIRST_ID = 101
STUDENT_DISCOUNT = 0.25

PASS_TYPES = {
    "Monthly": {"days": 30, "fee": 500},
    "Quarterly": {"days": 90, "fee": 1350},
    "Yearly": {"days": 365, "fee": 4800}
}

CATEGORIES = ["General", "Student"]
passes = []


def banner():
    print("\n" + "=" * 50)
    print("       BUS PASS MANAGEMENT SYSTEM")
    print(" Rungta International Skills University")
    print("=" * 50)


def menu():
    print("\n1. Issue New Pass")
    print("2. Renew Existing Pass")
    print("3. Search Pass by ID")
    print("4. View All Passes")
    print("5. Exit")


def line_of(p):
    return (
        f"ID: {p['id']} | Name: {p['name']} | "
        f"Route: {p['route']} | Type: {p['type']} | "
        f"Fee: Rs. {p['fee']:.2f}"
    )


def save_passes():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for p in passes:
            f.write(
                f"{p['id']}|{p['name']}|{p['route']}|"
                f"{p['type']}|{p['fee']}|{p['category']}|"
                f"{p['issued']}|{p['expiry']}\n"
            )


def load_passes():
    passes.clear()

    if not os.path.exists(FILE_NAME):
        return

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        for raw in f:
            parts = raw.strip().split("|")
            if len(parts) != 8:
                continue

            try:
                fee = float(parts[4])
            except ValueError:
                continue

            passes.append({
                "id": parts[0],
                "name": parts[1],
                "route": parts[2],
                "type": parts[3],
                "fee": fee,
                "category": parts[5],
                "issued": parts[6],
                "expiry": parts[7]
            })


def next_id():
    numbers = []

    for p in passes:
        digits = p["id"].replace("BP", "")
        if digits.isdigit():
            numbers.append(int(digits))

    return f"BP{max(numbers) + 1 if numbers else FIRST_ID}"


def normalize(value, options):
    for option in options:
        if value.strip().lower() == option.lower():
            return option
    return None


def calculate_fee(pass_type, category):
    fee = PASS_TYPES[pass_type]["fee"]

    if category == "Student":
        fee *= (1 - STUDENT_DISCOUNT)

    return round(fee, 2)


def find_pass(pass_id):
    for p in passes:
        if p["id"].upper() == pass_id.strip().upper():
            return p
    return None


def issue_pass():
    print("\n--- ISSUE NEW PASS ---")

    name = input("Name: ").strip()
    route = input("Route: ").strip()
    type_input = input("Type (Monthly/Quarterly/Yearly): ").strip()
    category_input = input("Category (General/Student): ").strip()

    if not name or not route:
        print("ERROR: Name and Route cannot be empty. Pass not issued.")
        return

    pass_type = normalize(type_input, PASS_TYPES)
    if pass_type is None:
        print("ERROR: Invalid pass type. Pass not issued.")
        return

    category = normalize(category_input, CATEGORIES)
    if category is None:
        print("ERROR: Invalid category. Pass not issued.")
        return

    today = date.today()
    days = PASS_TYPES[pass_type]["days"]

    new_pass = {
        "id": next_id(),
        "name": name,
        "route": route,
        "type": pass_type,
        "fee": calculate_fee(pass_type, category),
        "category": category,
        "issued": str(today),
        "expiry": str(today + timedelta(days=days))
    }

    passes.append(new_pass)
    save_passes()

    print(f"SUCCESS: Pass issued. ID: {new_pass['id']}")
    print(f"Name     : {name}")
    print(f"Route    : {route}")
    print(f"Type     : {pass_type}")
    print(f"Fee      : Rs. {new_pass['fee']:.2f}")

    if category == "Student":
        print("Student discount: 25% applied.")

    print(f"Valid for: {days} days")
    print(f"Expiry   : {new_pass['expiry']}")


def renew_pass():
    print("\n--- RENEW PASS ---")
    pid = input("Enter Pass ID: ").strip()
    p = find_pass(pid)

    if p is None:
        print("ERROR: Pass not found.")
        return

    type_input = input(
        "Renew as (Monthly/Quarterly/Yearly), Enter to keep same: "
    ).strip()

    pass_type = p["type"] if not type_input else normalize(
        type_input, PASS_TYPES
    )

    if pass_type is None:
        print("ERROR: Invalid pass type. Pass not renewed.")
        return

    try:
        old_expiry = date.fromisoformat(p["expiry"])
    except ValueError:
        old_expiry = date.today()

    start = max(date.today(), old_expiry)
    p["type"] = pass_type
    p["fee"] = calculate_fee(pass_type, p["category"])
    p["expiry"] = str(
        start + timedelta(days=PASS_TYPES[pass_type]["days"])
    )

    save_passes()
    print("SUCCESS: Pass renewed.")
    print(line_of(p))
    print(f"New expiry: {p['expiry']}")


def search_pass():
    print("\n--- SEARCH PASS ---")
    pid = input("Enter Pass ID: ").strip()
    p = find_pass(pid)

    if p is None:
        print("ERROR: Pass not found.")
        return

    print(line_of(p))
    print(f"Category : {p['category']}")
    print(f"Issued   : {p['issued']}")
    print(f"Expiry   : {p['expiry']}")


def view_all():
    print("\n--- ALL PASSES ---")

    if not passes:
        print("No passes issued yet.")
        return

    print("-" * 90)
    total = 0

    for p in passes:
        print(line_of(p))
        print(f"Category: {p['category']} | Expiry: {p['expiry']}")
        total += p["fee"]

    print("-" * 90)
    print(f"Total passes: {len(passes)}")
    print(f"Total collection: Rs. {total:.2f}")


def main():
    load_passes()
    banner()

    while True:
        menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            issue_pass()
        elif choice == "2":
            renew_pass()
        elif choice == "3":
            search_pass()
        elif choice == "4":
            view_all()
        elif choice == "5":
            print("Thank you for using Bus Pass Management System.")
            break
        else:
            print("ERROR: Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()