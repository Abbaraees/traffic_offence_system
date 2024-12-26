# Traffic Offence Management System

This is a web application for managing traffic offences, offenders, and payments. The system allows administrators to manage offences, offenders, and their relationships, as well as track payments.

## Features

- Manage Offences
- Manage Offenders
- Manage Violation Records (Offender-Offence Relationships)
- Manage Payments
- Dashboard with statistics and quick links

## Technologies Used

- Flask (Python web framework)
- SQLAlchemy (ORM for database interactions)
- Flask-Migrate (Database migrations)
- Flask-Login (User authentication)
- Jinja2 (Templating engine)
- Tailwind CSS (CSS framework)
- SQLite (Database)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Abbaraees/traffic_offence_system.git
    cd traffic_offence_system
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Initialize the database:

    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. Create an admin user:

    ```sh
    python startup.py
    ```

6. Run the application:

    ```sh
    flask run
    ```

## Usage

- Access the application at `http://127.0.0.1:5000/`.
- Log in with the admin credentials (`admin@example.com` / `admin123`).
- Use the dashboard to navigate to different management sections.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
