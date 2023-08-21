# MovieDBxNotion

A simple command line tool which fetches series and movie data from Movie DB to be formatted as a Notion page.

## Installing required modules

    pip install -r requirements.txt

## Make API Keys

### Notion

    MY_NOTION_TOKEN =""
    DATABASE_ID = ""

Follow [Notion - Getting Started](https://developers.notion.com/docs/create-a-notion-integration#getting-started) to create a new integration.
Note: Remember to grant permissions to the integration in your database

### Movie DB

    API_READ_ACCESS_TOKEN = ""

Follow [Movie DB - Getting Started](https://developer.themoviedb.org/reference/intro/getting-started) to create a new API key.

## How it works

Click module was used in making the command line. See more information below.
[Click - Quick Start](https://click.palletsprojects.com/en/8.1.x/api/)

### Commands available

- movie
- series

### Basic User Flow

1. Prompted to enter movie/series title
2. Displays available movies/series queried from MovieDB API
3. Choose movie/series
4. If it is a series, you are prompted to choose season number
5. Based on data available, create a page in your Notion Database
6. Press any button not within the list of choices inorder to quit
