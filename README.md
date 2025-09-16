# Call Journal

A lightweight web-based application for recording, organizing, and reviewing call details. This project provides a simple interface to log caller information, call duration, purpose, and additional notes, ensuring that important conversations are documented and easy to retrieve.  

---

## Features
- Add and manage call records with details such as name, number, date, and notes  
- Simple, user-friendly web interface  
- Search and review past call logs  
- Organized data storage for better tracking  

---

## Tech Stack
- **Backend**: Python, Flask  
- **Frontend**: HTML, CSS (Tailwind)  
- **Data Handling**: CSV, Pandas  

---

## Project Structure

```
Call-Journal/
│
├── .venv/              # Virtual environment (local only, not pushed to GitHub)
├── static/             # Static assets (CSS, JS, images)
├── templates/          # HTML templates for frontend
│
├── .env                # Environment variables (excluded via .gitignore)
├── app.py              # Main Flask application
├── call_analysis.csv   # Example dataset for call logs
├── requirements.txt    # Project dependencies
├── .gitignore          # Git ignore rules
├── README.md           # Project documentation
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ipsita-23/Call-Journal.git
   cd Call-Journal
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file for configuration (example: API keys, database URL).  
   > Important: Do not commit `.env` to GitHub.

5. Run the application:
   ```bash
   flask run
   ```

---

## Usage
1. Open the app in your browser at `http://127.0.0.1:5000/`.  
2. Add new call entries with details such as name, phone number, date, and notes.  
3. View, search, and review saved call logs.  

---

## Future Enhancements
- Filtering and sorting call records  
- Analytics and visualizations for call data  
- Export to CSV or Excel  
- Authentication and user management  

---

## License
This project is licensed under the MIT License.  
