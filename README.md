Castle Chess

Castle Chess is a standalone Python application designed to manage chess tournaments. The application includes features
for managing clubs, players, and tournaments, including matchmaking, score tracking, and reporting.
Table of Contents

    Installation
    Usage
    Features
    Dependencies
   

Installation

To set up the project, follow these steps:

    Clone the repository:


git clone <https://github.com/gonzalezedgarphone/P3-Application-Developer-Skills-Bootcamp.git>

cd <repository_name> This will be the directory where you save the clone repository

Create and activate a virtual environment:


python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

Install dependencies:


    pip install -r requirements.txt


To run the application, use the following command in the console:


python manage_clubs.py


### Models

This package contains the models already defined by the application:
* `Player` is a class that represents a chess player
* `Club` is a class that represents a chess club (including `Player`s)
* `ClubManager` is a manager class that allows to manage all clubs (and create new ones)
* `Tournament` is a class that helps create instances of a tournament 
The methods in the tournament help serialize data into json file
* `TournamentOperation` is a class that helps pair players, keep scores, and display rankings

### Main application

The main application is controlled by `manage_clubs.py`. Based on the current Context instance, it instantiates the 
screens and run them. The command returned by the screen is then executed to obtain the next context.

The main application is an infinite loop and stops when a context has the attribute `run` set to False.

Managing Clubs and Players

### Data files

There are data files provided:
- JSON files for the chess clubs of Springfield and Cornville
- JSON files for two tournaments: one completed, and one in progress

The program uses JSON data files for the clubs, located in the data/clubs folder. Each club has an associated JSON file
containing information about registered players.
Tournaments

Tournament data is stored in JSON files in the data/tournaments folder. Tournaments include attributes such 
as name, venue, dates, players, rounds, and current round.
Features

### Screens

This package contains classes that are used by the application to display information from the models on the screen.
Each screen returns a Command instance (= the action to be carried on).

Main Screen

    Displays a list of ongoing tournaments sorted by start date.
    Allows the user to select a tournament or create a new one.


### Commands

This package contains "commands" - instances of classes that are used to perform operations from the program.
Commands follow a *template pattern*. They **must** define the `execute` method.
When executed, a command returns a context.

View/Manage Tournament

    Displays tournament details (name, dates, rounds, players).
    Allows registration of players, entering match results, advancing rounds, and generating reports.

Register a Player

    View a list of available players.
    Search for players by Chess Identifier or name.
    Select and register players for the tournament.

Enter Results

    Displays matches for the current round.
    Allows entering match results (winner/loser or tie).
    Updates tournament points based on results.

Advance to the Next Round

    Confirms advancing to the next round.
    Generates new pairings or closes the tournament if it's the last round.

Tournament Reports

    Displays a report of the tournament, including participants sorted by points and match details for each round.

Dependencies

The project uses the following dependencies:

    Faker==25.2.0
    certifi==2024.7.4
    charset-normalizer==3.3.2
    django-commands==0.7
    googlemaps==4.10.0
    idna==3.7
    numpy==2.0.0
    pandas==2.2.2
    pip==24.1.1
    python-dateutil==2.9.0.post0
    pytz==2024.1
    requests==2.32.3
    setuptools==70.2.0
    six==1.16.0
    tzdata==2024.1
    urllib3==2.2.2

To install the required dependencies, use:

pip install -r requirements.tx

Faker==25.2.0
certifi==2024.7.4
charset-normalizer==3.3.2
django-commands==0.7
googlemaps==4.10.0
idna==3.7
numpy==2.0.0
pandas==2.2.2
pip==24.1.1
python-dateutil==2.9.0.post0
pytz==2024.1
requests==2.32.3
setuptools==70.2.0
six==1.16.0
tzdata==2024.1
urllib3==2.2.2

