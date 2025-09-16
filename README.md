Call Journal

A lightweight web-based application for recording, organizing, and reviewing call details. This project provides a simple interface to log caller information, call duration, purpose, and additional notes, ensuring that important conversations are documented and easy to retrieve.

Features

Add and manage call records with details such as name, number, date, and notes

Simple, user-friendly web interface

Search and review past call logs

Organized data storage for better tracking

Tech Stack

Backend: Python, Flask

Frontend: HTML, CSS (Tailwind)

Data Handling: CSV, Pandas

Project Structure
Call-Journal/
│
├── .venv/              # Virtual environment (not pushed to GitHub)
├── static/             # Static files (images, CSS, JS)
├── templates/          # HTML templates for rendering UI
├── .env                # Environment variables (API keys, configs)
├── app.py              # Main Flask application
├── call_analysis.csv   # Example dataset for call logs
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignored files (e.g., .env, venv, cache)
├── README.md           # Project documentation

Installation

Clone the repository:

git clone https://github.com/ipsita-23/Call-Journal.git
cd Call-Journal


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # for Linux/Mac
venv\Scripts\activate      # for Windows


Install dependencies:

pip install -r requirements.txt


Set up a .env file for configuration (keep it local and do not commit to GitHub).

Run the application:

flask run

Future Enhancements

Filtering and sorting call records

Analytics and visualizations for call data

Export to CSV or Excel

Authentication and user management
