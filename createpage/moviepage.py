# Import Notion Modules
from notionapi import blocks
from notionapi import property
from notionapi import notion

# Load global variables
from createpage import config
MY_NOTION_TOKEN =config.MY_NOTION_TOKEN
database_id = config.DATABASE_ID
headers = config.HEADERS

# Checks whether database is successfully paired
# notion.get_database(database_id, headers)

def create_page(title,synopsis,poster,release_date,genre,homepage,provider):
    """Create movie page in Notion DB

    Args:
        title (str): title of the movie
        synopsis (str): overview of the movie
        poster (str): url link to poster
        release_date (str): in ISO 860 format
        genre (list): list of genre
        homepage (str): url link to homepage
        provider (str): provider of movie

    Returns:
        str: Notion page ID
    """

    Title = property.title(title)
    Genre = property.multi_select(genre)
    Program =  property.select("Movie")
    Homepage = property.url(homepage)
    Release_date = property.date(release_date)

    if provider == "Netflix":
        Pagecover = "https://i.pcmag.com/imagery/reviews/05cItXL96l4LE9n02WfDR0h-5..v1582751026.png"
    elif provider == "Amazon Prime Video" or provider == "Amazon Video":
        Pagecover = "https://www.recode.id/wp-content/uploads/2023/01/prime-video.jpg"
    elif provider == "Apple TV" or provider == "Apple TV+":
        Pagecover = "https://images.unsplash.com/photo-1608446781624-bb081c6c0e18?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDJ8fGFwcGxlJTIwdHZ8ZW58MHx8fHwxNjkyNTg3OTYzfDA&ixlib=rb-4.0.3&q=80&w=200"
    elif provider == "Disney Plus":
        Pagecover = "https://www.comingsoon.net/wp-content/uploads/sites/3/2023/08/Disney-Plus-Price-Increase-2023.jpg?w=1024"
    else:
        Pagecover = "https://images.unsplash.com/photo-1595769816263-9b910be24d5f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDd8fGNpbmVtYXxlbnwwfHx8fDE2OTI1NzAyODB8MA&ixlib=rb-4.0.3&q=80&w=200"
    

    property_field = {
        "Name": Title,
        "Genre": Genre,
        "Program": Program,
        "Homepage": Homepage,
        "Release Date": Release_date,
    }

    Review = blocks.heading_1("Overall Review")
    Callout = blocks.callout("")
    Movie_poster = blocks.image(poster)
    Left_column = blocks.column(Movie_poster)
    Synopsis = blocks.main_paragraph(synopsis)
    Right_column = blocks.column(Synopsis)
    Colomn_list = blocks.column_list(Left_column,Right_column)
    content = notion.content_format(Review,Callout,Colomn_list)

    page_id = notion.create_page(
        database_id, headers, property_field, content, Pagecover,
    )

    return page_id



