# py-task-manager

py-task-manager is a Django-based web service for managing tasks. Unlike file-based task managers, all tasks are stored in a database. The application provides a modern, responsive web interface for adding, viewing, marking as complete, and deleting tasks.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Usage](#usage)
- [Example](#example)
- [Contributing](#contributing)
- [Contact Information](#contact-information)

---

## Project Overview
py-task-manager is a robust Django application that enables users to manage their daily tasks through a web interface. Key aspects of this project include:
- **Database-backed storage:** All tasks are stored in a database (SQLite by default), not in a file.
- **Web service:** The application is designed to be accessed via a web browser and can be deployed to production servers.

---

## Features
- **Task Creation:** Create new tasks by providing a description and a mandatory deadline.
- **Task Listing:** View all tasks in a clean, user-friendly interface.
- **Task Completion:** Mark tasks as completed; the interface clearly indicates their status.
- **Task Deletion:** Remove tasks from the database when they are no longer needed.
- **User Management:** Access the Django admin interface for managing tasks and users.
- **Environment Configuration:** All sensitive settings (e.g., `SECRET_KEY`, `DEBUG`, database configurations) are managed via an environment file.

---

## Requirements
- **Python 3.x**
- **Django** (see `requirements.txt` for the full list of dependencies)
- A supported database engine (by default, SQLite is used)

---

# Installation

Clone the repository by running the command:

```sh
git clone https://github.com/taraskhom/py-task-manager.git
```

Change to the project directory:

```sh
cd py-task-manager
```

If necessary, switch to the `develop` branch:

```sh
git checkout develop
```

Create a virtual environment:

```sh
python -m venv venv
```

Activate the virtual environment:

- On Linux/MacOS:

  ```sh
  source venv/bin/activate
  ```

- On Windows:

  ```sh
  venv\Scripts\activate
  ```

Install the required dependencies:

```sh
pip install -r requirements.txt
```

## Environment Configuration

Copy the sample environment file:

```sh
cp .env.sample .env
```

Open the `.env` file in your preferred text editor and update the settings. You must set:

- `SECRET_KEY`: Your Django secret key.
- `DEBUG`: `True` for development or `False` for production.
- `DATABASE_URL`: Specify your database connection (SQLite is used by default, but you can update it for other databases).

Update any other required environment variables as needed.

## Usage

Apply database migrations:

```sh
python manage.py migrate
```

Start the Django development server:

```sh
python manage.py runserver
```

Access the application in your web browser at:

```sh
http://127.0.0.1:8000/
```

## Example

When using the web interface, the **deadline** field is mandatory when adding a new task.
For example, if you add a task with the description "Finish report," you must provide a deadline.
The form validates that the deadline is provided and correctly formatted before saving the task to the database. In a typical workflow:

1. Navigate to the **Assign Task** page.
2. Fill all required fields.
3. Submit the form.
4. The task will be displayed on the tasks pages with its current status.

## Contributing

If you wish to contribute:

1. Fork the repository.
2. Create a new branch named to reflect your feature or fix:

   ```sh
   git checkout -b feature-branch-name
   ```

3. Make your changes and commit them with a clear message:

   ```sh
   git commit -m "Add detailed task filtering"
   ```

4. Push your branch:

   ```sh
   git push origin feature-branch-name
   ```

5. Open a pull request describing your changes.


## Contact Information

For any questions or suggestions, please contact us via email at:

```sh
khomenkotaras1305@gmail.com
```
