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

The app defines these tables in `project/main.py`:

- `Teacher`
  - `t_id` (primary key)
  - `t_name`
  - `sub_code`
  - `sub_name`
  - `dob`

- `Batch`
  - `b_id` (primary key)
  - `day`
  - `time_in`
  - `time_out`
  - `t_id`

- `System`
  - `sys_id` (primary key)
  - `status`

- `Student`
  - `s_id` (primary key)
  - `s_name`
  - `dob`
  - `b_id`
  - `sys_id`
  - `email`

- `Experiment`
  - `e_id` (primary key)
  - `title`
  - `doe`
  - `t_id`

## What You Can Do in the App

- Log in as admin using the credentials in `config.json`
- Add new teachers, batches, systems, students, and experiments
- Update records for each of those entities
- Delete records when they are no longer needed
- See student data in a table view

## Report Images

The project report includes design diagrams and interface screenshots. I extracted the important image assets from `Final Draft 3.docx` and placed them in `docs/docx_images/`.

### ER and Schema Diagrams

![ER diagram](docs/docx_images/image3.jpeg)

*Figure 1: ER diagram showing Teacher, Student, Batch, System, and Experiment relationships*

![Relational schema diagram](docs/docx_images/image4.png)

*Figure 2: relational schema diagram and table mappings*

### Important Screenshots

![Admin homepage menu](docs/docx_images/image32.png)

*Figure 3: admin navigation menu for forms and tables*

![Login and landing page](docs/docx_images/image26.png)

*Figure 4: homepage with login section*

![Add Teacher screen](docs/docx_images/image27.png)

*Figure 5: add teacher form*

![Add Batch screen](docs/docx_images/image28.png)

*Figure 6: add batch form*

![Add Student screen](docs/docx_images/image29.png)

*Figure 7: add student form*

![Add Experiment screen](docs/docx_images/image30.png)

*Figure 8: add experiment form*

## How to Run It

1. Install Python 3.9 or newer.
2. Install MySQL and create a database named `lab`.
3. Activate the virtual environment if you have one.
4. Install the dependencies:
   ```powershell
   .\.venv\Scripts\python -m pip install -r requirements.txt
   .\.venv\Scripts\python -m pip install pymysql
   ```
5. Check the database connection in `project/main.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/lab'
   ```
6. Check `config.json` for admin login details:
   ```json
   {
       "params": {
           "user": "Admin",
           "password": "Admin123"
       }
   }
   ```
7. Run the app:
   ```powershell
   .\.venv\Scripts\python .\project\main.py
   ```
8. Open `http://127.0.0.1:5000/` in your browser.
9. Go to `http://127.0.0.1:5000/adminlogin` to sign in.

## Note on the Database

The app expects the `lab` database and the tables to already exist. The PDF report has screenshots and examples of how the tables are set up. If the tables are missing, you will need to create them manually.

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
