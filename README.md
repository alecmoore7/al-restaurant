# 🌿 Happy Lawn Management Application

A full-featured Flask web app for managing employees, lawn jobs, and operations for a lawn care business. Built for speed, simplicity, and seasonal crews.

---

## 🚀 Features

- 👨‍🌾 **Employee Management**  
  Add, edit, and delete employees. Track job titles, contact info, and start dates.

- 🏡 **Lawn Job Scheduling**  
  Manage address, property type, size, and job notes. Create, edit, and delete lawn entries.

- 💾 **MariaDB Integration**  
  Data stored persistently in a relational SQL database. Secure form submissions and validation.

- 🧱 **Responsive Design**  
  Bootstrap 5 layout with custom CSS for a clean and mobile-friendly experience.

---

## 🛠️ Tech Stack

| Layer      | Technology           |
|------------|----------------------|
| Backend    | Python (Flask)       |
| Frontend   | HTML, Jinja2, Bootstrap 5 |
| Database   | MariaDB (SQL)        |
| Styling    | Custom CSS           |
| Dev Env    | VS Code + WSL (Ubuntu) |

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/alecmoore7/al-restaurant.git
cd al-restaurant
```

### 2. Set up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start your MariaDB server (if not already running)

For WSL/Ubuntu users:
```bash
sudo service mysql start
```

### 5. Set up the database

If the `lawncare` database doesn’t already exist, create it:

```bash
mysql -u root -p
```

Inside the MariaDB shell:

```sql
CREATE DATABASE lawncare;
EXIT;
```

Then import the table structure:

```bash
mysql -u root -p lawncare < project3.sql
```

### 6. Run the Flask app

Make sure you’re in the project directory and your virtual environment is activated.

Run:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

> On Windows (CMD), use `set` instead of `export`:
>
> ```cmd
> set FLASK_APP=app.py
> set FLASK_ENV=development
> flask run
> ```

Visit the app in your browser at:  
[http://localhost:5000](http://localhost:5000)

---

## 🗂️ Project Structure

```
al-restaurant/
├── app.py
├── config.py
├── database.py
├── project3.sql
├── requirements.txt
├── static/
│   ├── css/
│   │   └── styles.css
│   └── images/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── employees.html
│   ├── employee_form.html
│   └── lawn_form.html
└── README.md
```