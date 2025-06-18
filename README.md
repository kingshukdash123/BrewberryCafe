# ☕ BrewBerry Cafe – Streamlit Web App

Welcome to **BrewBerry Cafe**, a modern Streamlit-based web app that lets users **sign up**, **sign in**, and **order delicious food and cold drinks** – all powered by **Google Sheets as the database**.

This app is built for small cafes, college canteens, or personal projects where managing users and orders can be done easily without a dedicated backend.

---

## 🚀 Features

- 👤 User Sign Up with details (username, password, contact, email)
- 🔐 Secure Sign In with password verification
- 🍽️ Dynamic Food & Cold Drink Menu with prices
- 🧾 Auto-generated Bill on order
- 📄 View Registered Users
- ☁️ Google Sheets as a database (using `streamlit_gsheets`)
- ✅ Interactive UI with Streamlit

---

## 🛠️ Technologies Used

| Tool | Description |
|------|-------------|
| **Python 3.x** | Core programming language |
| **Streamlit** | UI Framework |
| **Pandas** | Data manipulation |
| **Google Sheets API** | Backend database |
| **streamlit_gsheets** | Bridge between Streamlit and Sheets |

---

## 📁 Project Structure

brewberry-cafe/
│
├── app.py # Main Streamlit app
├── item.py # Menu items as Python dictionaries
├── requirements.txt # All dependencies
├── README.md # Project documentation
└── .streamlit/
└── secrets.toml # Google API credentials (DO NOT share)