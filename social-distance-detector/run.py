import os

# Get the directory of the current script
project_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the project directory
os.chdir(project_dir)

# Run the Django server command
os.system("python manage.py runserver")