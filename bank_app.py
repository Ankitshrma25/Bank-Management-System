import json
import random
import string
from pathlib import Path
import streamlit as st

class Bank:
    def __init__(self, database='data.json'):
        self.database = Path(database)
        self.data = self.load_data()

    def load_data(self):
        if self.database.exists():
            try:
                with open(self.database, 'r') as fs:
                    return json.load(fs)
            except json.JSONDecodeError:
                return []
        return []

    def save_data(self):
        with open(self.database, 'w') as fs:
            json.dump(self.data, fs, indent=4)

    def generate_account_number(self):
        aplpha = random.choices(string.ascii_uppercase, k=3)
        num = random.choices(string.digits, k=3)
        spchr = random.choices("!@#$%^&*()_+", k=1)
        acc_id = aplpha + num + spchr
        random.shuffle(acc_id)
        return "".join(acc_id)

    def create_account(self, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4 or not str(pin).isdigit():
            return "❌ You must be at least 18 and PIN must be 4 digits."

        new_account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": int(pin),
            "accountNo.": self.generate_account_number(),
            "balance": 0
        }

        self.data.append(new_account)
        self.save_data()
        return f"✅ Account created successfully!\nYour Account No: {new_account['accountNo.']}"

    def find_user(self, account_no, pin):
        return [i for i in self.data if i['accountNo.'] == account_no and i['pin'] == pin]

    def deposit(self, account_no, pin, amount):
        user = self.find_user(account_no, pin)
        if not user:
            return "❌ Invalid account or PIN!"
        if amount <= 0 or amount > 10000:
            return "❌ Amount must be between 1 and 10,000!"
        user[0]['balance'] += amount
        self.save_data()
        return f"💰 Deposited {amount}. New Balance: {user[0]['balance']}"

    def withdraw(self, account_no, pin, amount):
        user = self.find_user(account_no, pin)
        if not user:
            return "❌ Invalid account or PIN!"
        if user[0]['balance'] < amount:
            return "❌ Insufficient funds!"
        user[0]['balance'] -= amount
        self.save_data()
        return f"💸 Withdrawn {amount}. New Balance: {user[0]['balance']}"

    def show_details(self, account_no, pin):
        user = self.find_user(account_no, pin)
        if not user:
            return "❌ Invalid account or PIN!"
        return user[0]

    def update_details(self, account_no, pin, new_name=None, new_email=None, new_pin=None):
        user = self.find_user(account_no, pin)
        if not user:
            return "❌ Invalid account or PIN!"
        
        if new_name:
            user[0]['name'] = new_name
        if new_email:
            user[0]['email'] = new_email
        if new_pin and new_pin.isdigit() and len(new_pin) == 4:
            user[0]['pin'] = int(new_pin)
        elif new_pin:
            return "❌ PIN must be 4 digits!"
        
        self.save_data()
        return "✅ Details updated successfully!"

    def delete_account(self, account_no, pin):
        user = self.find_user(account_no, pin)
        if not user:
            return "❌ Invalid account or PIN!"
        self.data.remove(user[0])
        self.save_data()
        return "🗑️ Account deleted successfully!"

# --- Streamlit App ---
st.set_page_config(page_title="Bank Management System", layout="centered")
st.title("🏦 Bank Management System")

bank = Bank()

menu = st.sidebar.radio("Select Option", [
    "Create Account", "Deposit Money", "Withdraw Money", 
    "Show Account Details", "Update Details", "Delete Account"
])

if menu == "Create Account":
    st.subheader("Create a New Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    email = st.text_input("Email")
    pin = st.text_input("4-Digit PIN", type="password")
    if st.button("Create"):
        st.success(bank.create_account(name, age, email, pin))

elif menu == "Deposit Money":
    st.subheader("Deposit Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)
    if st.button("Deposit"):
        st.success(bank.deposit(acc_no, int(pin), amount))

elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)
    if st.button("Withdraw"):
        st.success(bank.withdraw(acc_no, int(pin), amount))

elif menu == "Show Account Details":
    st.subheader("Account Details")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Show"):
        details = bank.show_details(acc_no, int(pin))
        if isinstance(details, dict):
            st.json(details)
        else:
            st.error(details)

elif menu == "Update Details":
    st.subheader("Update Account Details")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    new_name = st.text_input("New Name (optional)")
    new_email = st.text_input("New Email (optional)")
    new_pin = st.text_input("New 4-Digit PIN (optional)", type="password")
    if st.button("Update"):
        st.success(bank.update_details(acc_no, int(pin), new_name, new_email, new_pin))

elif menu == "Delete Account":
    st.subheader("Delete Account")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Delete"):
        st.warning(bank.delete_account(acc_no, int(pin)))
