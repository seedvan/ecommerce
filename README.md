To successfully run this application, follow the steps below:
    1. Download the project directory onto a Unix-based operating system with the latest version of Python downloaded.
    2. Open the terminal in the project directory
    3. Activate the virtual environment using the following command "source venv/bin/activate"
    4. Install the project dependencies by using the command "pip install -r requirements.txt"
    4. Run the web application using the command "gunicorn ecommerce.wsgi:application -c gunicorn.config.py"