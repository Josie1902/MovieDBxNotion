# Module for CLI
import click

# Import API modules
from mdb2 import MovieDB
from createpage2 import NotionAPI

# Import secret
import os
from dotenv import load_dotenv

# Load secrets
# Get the base path of the executable
base_path = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the .env file
env_path = os.path.join(base_path, '.env')

# Load environment variables from the .env file
load_dotenv(env_path)
API_READ_ACCESS_TOKEN = os.getenv("API_READ_ACCESS_TOKEN")

# Construct the headers
MOVIEDBHEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_READ_ACCESS_TOKEN}"
}

MY_NOTION_TOKEN = os.getenv("MY_NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

NOTIONHEADERS = {
    "Authorization": f"Bearer {MY_NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}



@click.group()
def cli():
    """A simple CLI for MovieDB x NotionAPI"""
    pass

@click.command(help='check connections')
def connection():
    click.echo(click.style("-------------------- \nChecking Connections\n--------------------", fg='yellow'))
    moviedbconnection = MovieDB(MOVIEDBHEADERS).check_connection()
    click.echo(f"MovieDB: {moviedbconnection}")
    notionapiconnection = NotionAPI(DATABASE_ID,NOTIONHEADERS).check_connection()
    click.echo(f"NotionAPI: {notionapiconnection}")

@click.command(help='search for movies')
@click.option('--title', prompt=click.style('\nEnter Title of Movie', fg='cyan'), help="Title of the movie to search for.")
def movie(title):
    moviedb = MovieDB(MOVIEDBHEADERS)
    top_5 =  moviedb.search_movie(title)
    if len(top_5) == 0:
        click.echo(click.style("No movies found. Choose a different title", fg='red'))
    else:
        for idx, film in enumerate(top_5, start=1):
                print(f"{idx}. {film['title']} ({film['release_date']})")
        
        selection = click.prompt('Choose a movie (enter the number)', type=click.IntRange(1, len(top_5)),err=True,)
        chosen_movie = top_5[selection - 1]
        id = chosen_movie['id']
        title = chosen_movie['title']
        synopsis = chosen_movie['overview']
        poster = "https://image.tmdb.org/t/p/original" + chosen_movie['poster_path']
        release_date = chosen_movie['release_date']
        details = moviedb.get_movie_details(id)
        genre = [genre["name"] for genre in  details["genres"]]
        homepage = details["homepage"]
        provider = moviedb.get_movie_provider(id)
        click.echo(click.style("-------------- \nMovie details:\n--------------", fg='blue'))
        print(f"Title: {title}")
        print(f"Overview: {synopsis}")
        click.confirm(click.style('\nDo you want to continue?', fg='cyan'), abort=True)
        notionapi = NotionAPI(DATABASE_ID,NOTIONHEADERS)
        property_field = notionapi.create_movie_property("Movie",title,genre,homepage,release_date)
        movie_content = notionapi.create_movie_format(synopsis,poster)
        page_id = notionapi.create_movie_page(property_field,provider,movie_content)
        if page_id != None:
            click.echo(click.style(f"\n🅂 🅄 🄲 🄲 🄴 🅂 🅂 🄵 🅄 🄻  🅁 🄴 🅂 🄿 🄾 🄽 🅂 🄴 ! Page Created @ {page_id}\n", fg='green'))
        else:
            click.echo(click.style(f"\n🅂 🄾 🄼 🄴 🅃 🄷 🄸 🄽 🄶  🅆 🄴 🄽 🅃  🅆 🅁 🄾 🄽 🄶 ! D:", fg='red'))

@click.command(help='search for series')
@click.option('--title', prompt=click.style('\nEnter Title of Series', fg='cyan'), help="Title of the series to search for.")
def series(title):
    moviedb = MovieDB(MOVIEDBHEADERS)
    top_5 =  moviedb.search_series(title)
    if len(top_5) == 0:
        click.echo(click.style("No series found. Choose a different title", fg='red'))
    else:
        for idx, film in enumerate(top_5, start=1):
            print(f"{idx}. {film['original_name']} ({film['first_air_date']})")

        selection = click.prompt('Choose a series (enter the number)', type=click.IntRange(1, len(top_5)))
        chosen_series = top_5[selection - 1]
        id = chosen_series['id']
        title = chosen_series['original_name']
        synopsis = chosen_series['overview']
        base_poster_path = "https://image.tmdb.org/t/p/original"
        poster_path = chosen_series['poster_path']
        details = moviedb.get_series_details(id)
        genre = [genre["name"] for genre in  details["genres"]]
        homepage = details["homepage"]
        provider = details['networks'][0]['name']
        seasons = [(season["season_number"],season["name"]) for season in details["seasons"]]
        click.echo(click.style("--------------- \nSeries details:\n---------------", fg='blue'))
        print(f"Title: {title}")
        print(f"Overview: {synopsis}")
        click.echo(click.style("------------------ \nSeasons Available:\n------------------", fg='magenta'))
        for idx, (season_number,season_name) in enumerate(seasons):
            print(f"{season_number}. {season_name}")
        first_season = seasons[0][0]
        last_season = seasons[len(seasons)-1][0]
        season_selection = click.prompt('Choose a season (enter the number)', type=click.IntRange(first_season, last_season))
        season_details = moviedb.get_season_details(id,season_selection)
        release_date = season_details["air_date"]
        season_name = season_details["name"]
        season_poster_path = season_details['poster_path'] if season_details['poster_path'] is not None else poster_path
        poster = base_poster_path + season_poster_path
        episode_array = []
        for episode in season_details["episodes"]:
            if episode['still_path'] != None:
                episode_img = "https://image.tmdb.org/t/p/original" + episode['still_path'] 
            else:
                episode_img = "https://www.pulsecarshalton.co.uk/wp-content/uploads/2016/08/jk-placeholder-image.jpg"
            episode_array.append([episode['episode_number'],episode['name'],episode['overview'],episode_img])

        click.confirm(click.style('\nDo you want to continue?', fg='cyan'), abort=True)
        notionapi = NotionAPI(DATABASE_ID,NOTIONHEADERS)
        property_field = notionapi.create_series_property("Series",season_name,title,genre,homepage,release_date)
        series_content = notionapi.create_series_format(episode_array,synopsis,poster)
        page_id = notionapi.create_series_page(property_field,provider,series_content)
        if page_id != None:
            click.echo(click.style(f"\n🅂 🅄 🄲 🄲 🄴 🅂 🅂 🄵 🅄 🄻  🅁 🄴 🅂 🄿 🄾 🄽 🅂 🄴 ! Page Created @ {page_id}\n", fg='green'))
        else:
            click.echo(click.style(f"\n🅂 🄾 🄼 🄴 🅃 🄷 🄸 🄽 🄶  🅆 🄴 🄽 🅃  🅆 🅁 🄾 🄽 🄶 ! D:", fg='red'))

cli.add_command(movie)
cli.add_command(connection)
cli.add_command(series)
    
if __name__ == '__main__':
    cli()
