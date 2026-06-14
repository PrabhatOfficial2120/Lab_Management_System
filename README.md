# Computer Laboratory Management System

This project is a simple Flask web application for managing a college computer lab. The main idea is to keep track of teachers, batches, computers, students, and lab experiments all in one place.

The full project report is in `Final Draft 8.pdf`, and this README summarizes the app and how it works.

## What the App Does

The app helps an administrator manage lab data, including:
- Adding and updating teachers
- Adding and updating batches
- Adding and updating computer systems
- Adding and updating students
- Adding and updating experiments
- Deleting records when needed
- Viewing student entries

The app uses Flask for the web interface and SQLAlchemy to connect with a MySQL database.

## Project Layout

- `project/main.py` - the Flask app and route definitions
- `project/templates/` - HTML pages for login, admin, add/update/delete forms, and tables
- `project/templates/static/` - static assets like CSS, JavaScript, and images
- `config.json` - admin login credentials used by the app
- `Final Draft 8.pdf` - project report with design diagrams and screenshots
- `docs/pdf_pages/` - PNG images generated from the PDF pages

## Main Technologies

- Python 3.9+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- MySQL
- SQLAlchemy
- HTML/CSS/Bootstrap

## Important Dependencies

The project uses a lot of packages, but the main ones for this app are:
- Flask==2.2.2
- Flask-Login==0.6.2
- Flask-SQLAlchemy==3.0.2
- SQLAlchemy==1.4.45
- `pymysql` for the MySQL connection string

## Database Tables

Complete database schema is documented in [`schema.sql`](schema.sql). The app defines these core tables:

- **Teacher**
  - `t_id` (primary key)
  - `t_name` — teacher name
  - `sub_code` — subject code
  - `sub_name` — subject name
  - `dob` — date of birth

- **Batch**
  - `b_id` (primary key)
  - `day` — batch day
  - `time_in` — start time
  - `time_out` — end time
  - `t_id` (foreign key → Teacher)

- **System**
  - `sys_id` (primary key)
  - `status` — computer system status

- **Student**
  - `s_id` (primary key)
  - `s_name` — student name
  - `dob` — date of birth
  - `b_id` (foreign key → Batch)
  - `sys_id` (foreign key → System)
  - `email` — student email

- **Experiment**
  - `e_id` (primary key)
  - `title` — experiment title
  - `doe` — date of experiment
  - `t_id` (foreign key → Teacher)

## What You Can Do in the App

- Log in as admin using the credentials in `config.json`
- Add new teachers, batches, systems, students, and experiments
- Update records for each of those entities
- Delete records when they are no longer needed
- See student data in a table view

## Report Images

The project report includes design diagrams and interface screenshots. I extracted the important image assets from `Final Draft 3.docx` and placed them in `docs/ScreenShots/`.

### ER and Schema Diagrams

![ER diagram](docs/ScreenShots/image3.jpeg)

*Figure 1: ER diagram showing Teacher, Student, Batch, System, and Experiment relationships*

![Relational schema diagram](docs/ScreenShots/image4.png)

*Figure 2: relational schema diagram and table mappings*

### Important Screenshots

![Admin homepage menu](docs/ScreenShots/image32.png)

*Figure 3: admin navigation menu for forms and tables*

![Login and landing page](docs/ScreenShots/image26.png)

*Figure 4: homepage with login section*

![Add Teacher screen](docs/ScreenShots/image27.png)

*Figure 5: add teacher form*

![Add Batch screen](docs/ScreenShots/image28.png)

*Figure 6: add batch form*

![Add Student screen](docs/ScreenShots/image29.png)

*Figure 7: add student form*

![Add Experiment screen](docs/ScreenShots/image30.png)

*Figure 8: add experiment form*

## How to Run It

### Quick Start (Automatic Setup)

1. **Install Python 3.9 or newer.**

2. **Activate the virtual environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install the dependencies:**
   ```powershell
   python -m pip install -r requirements.txt
   ```

4. **Run the app (database will auto-create on first startup):**
   ```powershell
   python .\project\main.py
   ```

5. **Open the app in your browser:**
   - Homepage: `http://127.0.0.1:5000/`
   - Admin login: `http://127.0.0.1:5000/adminlogin`

6. **Log in with default admin credentials:**
   ```
   Username: Admin
   Password: Admin123
   ```

### Database Details

- **By default**, the app uses **SQLite** (`lab.db`) for local development — no MySQL installation needed.
- Database tables are **automatically created** on first app startup.
- To use MySQL instead, set the `DATABASE_URL` environment variable:
  ```powershell
  $env:DATABASE_URL="mysql+pymysql://username:password@localhost/lab"
  ```

### Configuration

- **Admin credentials** are stored in `config.json`
- **Database schema** is defined in SQLAlchemy models in `project/main.py` and documented in `schema.sql`

## Notes About the Code

- Some routes use raw SQL `INSERT` statements instead of full ORM methods.
- Many admin pages are not fully protected by session checks in the current code.
- The main entities are `Teacher`, `Batch`, `Student`, `System`, and `Experiment`.

## Why This Project Exists

This project is meant to replace manual lab record-keeping with a simple digital system. It helps organize lab data, makes it easier to retrieve information, and reduces the time needed to manage teachers, students, batches, systems, and experiments.

## References

- `Final Draft 8.pdf`
- `config.json`
- `project/main.py`
- `project/templates/`
