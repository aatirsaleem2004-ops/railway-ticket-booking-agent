# 🚂 Railway Ticket Booking Agent

A modern desktop railway ticket booking system built with **Python** and **CustomTkinter**. The application provides a complete railway reservation workflow, allowing users to search trains, book tickets, process payments, cancel bookings, view booking history, and submit complaints through an intuitive graphical user interface.

---

## 📖 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Core Functionality](#-core-functionality)
- [Future Improvements](#-future-improvements)
- [Author](#-author)
- [Connect with Me](#-connect-with-me)
- [License](#-license)

---

# ✨ Features

### 🚆 Search Trains
- Search trains by departure and destination city.
- Display available seats in real time.
- View train details before booking.

### 🎫 Book Tickets
- Book between **1–6 seats** in a single transaction.
- Passenger name validation.
- CNIC/Passport validation.
- Automatic seat deduction after successful booking.

### 💳 Payment System
Supports simulated payment methods:
- JazzCash
- EasyPaisa
- Credit/Debit Card
- Cash Counter

### ❌ Cancel Booking
- Cancel an existing reservation.
- Restore seats automatically.
- Display refund message for paid bookings.

### 📖 Booking Ledger
- View all bookings.
- Live search by passenger name.
- Color-coded booking status.
- Real-time updates.

### 📝 Complaint System
- Submit complaints for a booking.
- General complaints are also supported.

---

# 📸 Screenshots

## 🏠 Home Screen

![Home Screen](Assets/Home.png)

---

## 🔍 Search Trains

![Search Trains](Assets/Search_Trains.png)

---

## 🎫 Book Ticket

![Book Ticket](Assets/Book_Ticket.png)

---

## 💳 Payment

![Payment](Assets/Payment.png)

---

## 📖 Booking Ledger

![Booking Ledger](Assets/Booking_Ledger.png)

---

## ❌ Cancel Booking

![Cancel Booking](Assets/Cancel_Booking.png)

---

## 📝 Complaint Form

![Complaint Form](Assets/Complaint.png)

---

# 🛠️ Tech Stack

- Python 3
- CustomTkinter
- Tkinter
- Python Dictionaries
- Object-Oriented Programming (OOP)

---

# 📂 Project Structure

```text
Railway-Ticket-Booking-Agent/
│
├── App.py
├── Assets/
│   ├── Home.png
│   ├── Search_Trains.png
│   ├── Book_Ticket.png
│   ├── Payment.png
│   ├── Booking_Ledger.png
│   ├── Cancel_Booking.png
│   └── Complaint.png
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/aatirsaleem2004-ops/railway-ticket-booking-agent.git
```

Go to the project folder:

```bash
cd railway-ticket-booking-agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Usage

Run the application:

```bash
python App.py
```

---

# 🧠 Core Functionality

The application manages the complete railway booking lifecycle.

### Booking Process

- Search available trains.
- Select departure and destination.
- Enter passenger details.
- Validate CNIC/Passport.
- Reserve seats.
- Process payment.
- Generate booking information.

### Seat Management

- Prevents overbooking.
- Updates seat availability automatically.
- Restores seats after cancellation.

### Payment Workflow

- Multiple payment methods.
- Payment confirmation.
- Booking status updates.

### Booking Ledger

- Displays all reservations.
- Search bookings instantly.
- Track booking status.

### Complaint Management

- Submit booking-related complaints.
- Submit general service complaints.

---

# 🚀 Future Improvements

- Database integration (SQLite/MySQL)
- User authentication
- Online payment gateway integration
- PDF ticket generation
- Email ticket confirmation
- QR Code tickets
- Admin dashboard
- Train schedule management
- Dark Mode
- Passenger booking history

---

# 👨‍💻 Author

**Muhammad Aatir Saleem**

Software Engineering Student

---

# 🌐 Connect with Me

- **GitHub:** https://github.com/aatirsaleem2004-ops
- **LinkedIn:** https://www.linkedin.com/in/aatir-saleem-136ba9362/

---

# 📜 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute this project for educational purposes.

---
