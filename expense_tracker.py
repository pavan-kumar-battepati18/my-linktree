import csv
import os
import requests
from datetime import datetime

# ─────────────────────────────────────────
#  CONFIG — paste your values here
# ─────────────────────────────────────────
BOT_TOKEN = "8920467465:AAG1ybVrreFXfK70HvGXbteTcPqbIjCqfQM"       # from @BotFather
CHAT_ID   = "6811760708"         # from @userinfobot
CSV_FILE  = "expenses.csv"
# ─────────────────────────────────────────


# ── Telegram ──────────────────────────────
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")


# ── CSV helpers ───────────────────────────
def init_csv():
    """Create CSV with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Time", "Type", "Category", "Amount", "Note"])


def save_transaction(type_, category, amount, note):
    """Save one transaction row to CSV."""
    now = datetime.now()
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%I:%M %p"),
            type_,
            category,
            amount,
            note
        ])


def load_transactions():
    """Return all transactions as list of dicts."""
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


# ── Core actions ──────────────────────────
def add_expense():
    print("\n── Add Expense ──")
    category = input("Category (Food/Travel/Bills/Other): ").strip() or "Other"
    amount   = float(input("Amount (₹): "))
    note     = input("Note (optional): ").strip()

    save_transaction("EXPENSE", category, amount, note)

    msg = (
        f"🔴 *Expense Recorded*\n"
        f"💸 Amount   : ₹{amount}\n"
        f"📂 Category : {category}\n"
        f"📝 Note     : {note or '—'}\n"
        f"🕐 Time     : {datetime.now().strftime('%I:%M %p, %d %b %Y')}"
    )
    send_telegram(msg)
    print("✅ Expense saved and notification sent!")


def add_income():
    print("\n── Add Income ──")
    sender   = input("Received from: ").strip() or "Unknown"
    amount   = float(input("Amount (₹): "))
    note     = input("Note (optional): ").strip()

    save_transaction("INCOME", sender, amount, note)

    msg = (
        f"🟢 *Money Received*\n"
        f"💰 Amount : ₹{amount}\n"
        f"👤 From   : {sender}\n"
        f"📝 Note   : {note or '—'}\n"
        f"🕐 Time   : {datetime.now().strftime('%I:%M %p, %d %b %Y')}"
    )
    send_telegram(msg)
    print("✅ Income saved and notification sent!")


def view_all():
    print("\n── All Transactions ──")
    transactions = load_transactions()
    if not transactions:
        print("No transactions yet.")
        return
    print(f"\n{'Date':<12} {'Time':<10} {'Type':<8} {'Category':<12} {'Amount':>8}  Note")
    print("-" * 65)
    for t in transactions:
        print(f"{t['Date']:<12} {t['Time']:<10} {t['Type']:<8} {t['Category']:<12} ₹{float(t['Amount']):>7.2f}  {t['Note']}")


def summary():
    print("\n── Summary ──")
    transactions = load_transactions()
    if not transactions:
        print("No transactions yet.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%Y-%m")

    total_expense = total_income = 0
    today_expense = today_income = 0

    for t in transactions:
        amt = float(t["Amount"])
        if t["Type"] == "EXPENSE":
            total_expense += amt
            if t["Date"] == today:
                today_expense += amt
        else:
            total_income += amt
            if t["Date"] == today:
                today_income += amt

    print(f"\n  Today's spending  : ₹{today_expense:.2f}")
    print(f"  Today's income    : ₹{today_income:.2f}")
    print(f"\n  Total spent       : ₹{total_expense:.2f}")
    print(f"  Total received    : ₹{total_income:.2f}")
    print(f"  Balance           : ₹{total_income - total_expense:.2f}")


# ── Main menu ─────────────────────────────
def main():
    init_csv()
    print("\n💰 Daily Expense Tracker")

    while True:
        print("\n1. Add Expense")
        print("2. Add Income")
        print("3. View All Transactions")
        print("4. Summary")
        print("5. Exit")

        choice = input("\nChoose (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            add_income()
        elif choice == "3":
            view_all()
        elif choice == "4":
            summary()
        elif choice == "5":
            print("Bye! 👋")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
