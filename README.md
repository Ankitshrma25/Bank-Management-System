# Bank Management System

A simple Bank Management System web app built with Python and Streamlit. It allows users to create accounts, deposit and withdraw money, view and update account details, and delete accounts. All data is stored in a local JSON file.

## Features
- Create a new bank account (with age and PIN validation)
- Deposit money (limit: 1 to 10,000 per transaction)
- Withdraw money (with balance check)
- View account details
- Update account information (name, email, PIN)
- Delete account

## Technologies Used
- Python 3
- Streamlit (for the web interface)
- JSON (for data storage)

## File Structure
- `bank_app.py`: Main application file containing the Bank class and Streamlit UI
- `data.json`: Stores account data

## Getting Started

### Prerequisites
- Python 3 installed
- Streamlit installed (`pip install streamlit`)

### How to Run
1. Open a terminal in the project directory.
2. Run the following command:
   ```powershell
   streamlit run bank_app.py
   ```
3. The app will open in your browser.

## Usage
- Use the sidebar to select an operation (Create Account, Deposit, Withdraw, etc.).
- Fill in the required details and click the corresponding button.
- Account numbers are randomly generated and shown after account creation.

## Notes
- PIN must be a 4-digit number.
- Minimum age to create an account is 18.
- Maximum deposit per transaction is 10,000.
- All data is stored locally in `data.json`.

## License
This project is for educational purposes.
