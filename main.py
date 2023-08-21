import click
from scrape import mdb
from createpage import moviepage
from createpage import seriespage

@click.group()
def cli():
    pass

@click.command(help='search for movies')
@click.option('--title', prompt="Enter Title of the Movie", help="Title of the movie to search for.")
def movie(title):
    top_5 =  mdb.search_movie(title)
    for idx, film in enumerate(top_5, start=1):
            print(f"{idx}. {film['title']} ({film['release_date']})")
    selection = click.prompt('Choose a movie (enter the number)', type=int)
    if 1 <= selection <= 5:
        chosen_movie = top_5[selection - 1]
        id = chosen_movie['id']
        title = chosen_movie['title']
        synopsis = chosen_movie['overview']
        poster = "https://image.tmdb.org/t/p/original" + chosen_movie['poster_path']
        release_date = chosen_movie['release_date']
        details = mdb.get_movie_details(id)
        genre = [genre["name"] for genre in  details["genres"]]
        homepage = details["homepage"]
        provider = mdb.get_movie_provider(id)
        click.echo(click.style("-------------- \nMovie details:\n--------------", fg='blue'))
        print(f"Title: {title}")
        print(f"Overview: {synopsis}")
        page_id = moviepage.create_page(title,synopsis,poster,release_date,genre,homepage,provider)
        click.echo(click.style(f"\n🅂 🅄 🄲 🄲 🄴 🅂 🅂 🄵 🅄 🄻  🅁 🄴 🅂 🄿 🄾 🄽 🅂 🄴 ! Page Created @ {page_id}\n", fg='green'))
    else:
        print("Invalid selection.")

@click.command(help='search for series')
@click.option('--title', prompt="Enter Title of the Series", help="Title of the series to search for.")
def series(title):
    top_5 = mdb.search_series(title)
    for idx, film in enumerate(top_5, start=1):
            print(f"{idx}. {film['original_name']} ({film['first_air_date']})")
    selection = click.prompt('Choose a series (enter the number)', type=int)
    if 1 <= selection <= 5:
        chosen_series = top_5[selection - 1]
        id = chosen_series['id']
        title = chosen_series['original_name']
        synopsis = chosen_series['overview']
        base_poster_path = "https://image.tmdb.org/t/p/original"
        poster_path = chosen_series['poster_path']
        details = mdb.get_series_details(id)
        genre = [genre["name"] for genre in  details["genres"]]
        homepage = details["homepage"]
        provider = details['networks'][0]['name']
        print("ID: ",id)
        seasons = [season["name"] for season in details["seasons"]]
        click.echo(click.style("--------------- \nSeries details:\n---------------", fg='blue'))
        print(f"Title: {title}")
        print(f"Overview: {synopsis}")
        click.echo(click.style("------------------ \nSeasons Available:\n------------------", fg='magenta'))
        for idx, season_name in enumerate(seasons):
            print(f"{idx}. {season_name}")
        season_selection = click.prompt('Choose a season (enter the number)', type=int)
        if 0 <= season_selection <= len(seasons):
            season_details = mdb.get_season_details(id,season_selection)
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
            
            page_id = seriespage.create_page(season_name,title,synopsis,poster,release_date,genre,homepage,provider,episode_array)
            if page_id != None:
                click.echo(click.style(f"\n🅂 🅄 🄲 🄲 🄴 🅂 🅂 🄵 🅄 🄻  🅁 🄴 🅂 🄿 🄾 🄽 🅂 🄴 ! Page Created @ {page_id}\n", fg='green'))
            else:
                 click.echo(click.style(f"\n🅂 🄾 🄼 🄴 🅃 🄷 🄸 🄽 🄶  🅆 🄴 🄽 🅃  🅆 🅁 🄾 🄽 🄶 ! D:", fg='red'))
        else:
            print("Invalid season selection.")

cli.add_command(movie)
cli.add_command(series)
    
if __name__ == '__main__':
    cli()
