# MovieDBxNotion

A simple command line tool which fetches series and movie data from Movie DB to be formatted as a Notion page.

## Installing required modules

    pip install -r requirements.txt

## Make API Keys

You should include these keys under your .env file.

### Notion

    MY_NOTION_TOKEN =""
    DATABASE_ID = ""

Follow [Notion - Getting Started](https://developers.notion.com/docs/create-a-notion-integration#getting-started) to create a new integration. Note: Remember to grant permissions to the integration in your database

! Your Notion DB headers should match the property you want to include. You can modify the property under createpage2.py.

### Movie DB

    API_READ_ACCESS_TOKEN = ""

Follow [Movie DB - Getting Started](https://developer.themoviedb.org/reference/intro/getting-started) to create a new API key.

## How it works

Click module was used in making the command line. See more information below.
[Click - Quick Start](https://click.palletsprojects.com/en/8.1.x/api/)

### Commands available

- connection: Checks connection to Notion database and MovieDB
- movie: Add movie page
- series: Add series page

### Basic User Flow

1. Prompted to enter movie/series title
2. Displays available movies/series queried from MovieDB API
3. Choose movie/series
4. If it is a series, you are prompted to choose season number
   \*\* Note: For Series, you are limited to 300 episodes per season
5. Based on data available, create a page in your Notion Database
6. Press ^C inorder to quit

### Page Formats

## Make this a global executable on your terminal

See Pyinstaller documentation: [Getting start](https://pyinstaller.org/en/stable/operating-mode.html)

    Mac: pyinstaller --onefile --add-data ".env:." main2.py
    Windows: pyinstaller --onefile --add-data ".env;." main2.py

1.  Bundle main.py using pyinstaller as seen above.
2.  main2.exe is created under dist folder. Copy it into the current directory and delete both the dist and build folders.
3.  Execute ./main2 in your current directory to check whether it is working
4.  `cp main2 ~/bin` (considering the fact that you already made a bin directory in your root ~)
    You might need to modify .zshrc or .bashrc to include a **PATH** to the bin
5.  You now have a global executable! :D

## Painful Realisations

### Odd pyinstaller-environment variables behaviour

Credits: [load-dotenv-not-working-when-running-pyinstaller](https://stackoverflow.com/questions/71245844/load-dotenv-env-not-working-when-running-pyinstaller-executable-from-path-searc)
A simple work around is to make sure we have an absolute path that points to the .env file.

    base_path  =  os.path.dirname(os.path.abspath(__file__))
    env_path  =  os.path.join(base_path,  '.env')
    load_dotenv(env_path)
