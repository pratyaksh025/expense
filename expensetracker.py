import csv
import os
import streamlit as st
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

FILENAME = 'expenses.csv'

# Create the CSV file if it doesn't exist
if not os.path.exists(FILENAME):
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Note"])

def add_expense():
    st.subheader("Add Expense")
    date = st.date_input("📅 Enter date")
    category = st.text_input("📂 Enter category (e.g. Food, Travel)")
    amount = st.number_input("💸 Enter amount", min_value=0.0, step=0.01)
    note = st.text_area("📝 Enter a note (optional)")

    if st.button("Add Expense"):
        with open(FILENAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount, note])
        st.success("✅ Expense added!")

def view_expenses():
    st.subheader("View Expenses")
    total = 0
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                st.write(f"{' | '.join(row)}")
                st.write("-" * 40)
            else:
                st.write(f"{' | '.join(row)}")
                try:
                    total += float(row[2])
                except:
                    pass
    st.write(f"\n💰 Total Spent: ₹{total:.2f}\n")

def graphical_view():
    st.subheader("Graphical View of Your Expenses")
    dates = []
    amounts = []
    categories = []
    category_totals = defaultdict(float)

    with open(FILENAME, mode='r') as f:
        cont = f.readlines()
        for idx, line in enumerate(cont):
            if idx == 0:
                continue  # Skip header
            parts = line.strip().split(',')
            if len(parts) >= 4:
                date_str, category, amount_str, note = parts
                try:
                    amount = float(amount_str)
                except ValueError:
                    continue  # Skip invalid amount

                # Display in app
                # st.write(f"📅 {date_str} | 🗂️ {category} | 💸 ₹{amount} | 📝 {note}")

                # Accumulate for plots
                dates.append(datetime.strptime(date_str, r"%Y-%m-%d"))
                amounts.append(amount)
                categories.append(category)
                category_totals[category] += amount

    # Pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=140)
    ax1.set_title("Expense Distribution by Category")
    st.pyplot(fig1)

    # Histogram
    fig2, ax2 = plt.subplots()
    ax2.hist(amounts, bins=10, color='skyblue', edgecolor='black')
    ax2.set_title("Histogram of Expense Amounts")
    ax2.set_xlabel("Amount")
    ax2.set_ylabel("Frequency")
    ax2.grid(True)
    st.pyplot(fig2)

    # Line chart
    sorted_data = sorted(zip(dates, amounts))
    sorted_dates = [d for d, _ in sorted_data]
    sorted_amounts = [a for _, a in sorted_data]

    fig3, ax3 = plt.subplots(figsize=(12, 6))  # Increase figure size
    ax3.plot(sorted_dates, sorted_amounts, marker='o', linestyle='-', color='green')
    ax3.set_title("Expenses Over Time")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Amount")
    ax3.grid(True)
    fig3.autofmt_xdate()  # Automatically format date labels for better readability
    ax3.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m-%Y'))  # Format x-axis as day-month-year
    st.pyplot(fig3)

def clear_expenses():
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Note"])
    st.success("✅ All expenses cleared!")

def main():
    st.title("📘 Expense Tracker")
    menu = ["-select-", "Add Expense", "View Expenses", "Graphical View", "Exit"]
    choice = st.selectbox("Select an option", menu)

    if choice == "Add Expense":
        add_expense()
    elif choice == "View Expenses":
        view_expenses()
    elif choice == "Graphical View":
        graphical_view()
    elif choice == "Exit":
        clear_expenses()
        st.info("👋 Goodbye! The CSV file has been cleared for the next user.")

if __name__ == "__main__":
    main()
