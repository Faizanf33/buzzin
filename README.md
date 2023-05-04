# buzzin
An AI powered news aggregator that brings just the news to you

#### How to run:
```
# Clone the repository
$ git clone https://github.com/Faizanf33/buzzin.git

# Go to the project folder
$ cd buzzin

# Create a virtual environment
$ python3 -m venv venv

# Activate the virtual environment
$ source venv/bin/activate

# Install the dependencies
$ pip install --upgrade pip
$ pip install -r requirements.txt

# Create database
$ python manage.py create-db

# Seed database
$ python manage.py seed-db

# Run the server
$ python manage.py run