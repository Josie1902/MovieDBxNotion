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

def create_page(season_name,title,synopsis,poster,release_date,genre,homepage,provider,episode_array):
    """Create series page in Notion DB

    Args:
        season_selection (int): season number
        title (str): title of the series
        synopsis (str): overview of the series
        poster (str): url link to poster
        release_date (str): in ISO 860 format
        genre (list): list of genre
        homepage (str): url link to homepage
        provider (str): provider of series
        episode_array (list): list of episodes (contains: episode number, title, synopsis and image)

    Returns:
        str: Notion page ID
    """

    Title = property.title(f"{title} ({season_name})")
    Genre = property.multi_select(genre)
    Program =  property.select("Movie")
    Homepage = property.url(homepage)
    Release_date = property.date(release_date) if release_date is not None else None


    if provider == "Netflix":
        Pagecover = "https://i.pcmag.com/imagery/reviews/05cItXL96l4LE9n02WfDR0h-5..v1582751026.png"
    elif provider == "Amazon Prime Video" or provider == "Amazon Video":
        Pagecover = "https://www.recode.id/wp-content/uploads/2023/01/prime-video.jpg"
    elif provider == "Apple TV" or provider == "Apple TV+":
        Pagecover = "https://images.unsplash.com/photo-1608446781624-bb081c6c0e18?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDJ8fGFwcGxlJTIwdHZ8ZW58MHx8fHwxNjkyNTg3OTYzfDA&ixlib=rb-4.0.3&q=80&w=200"
    elif provider == "Disney Plus":
        Pagecover = "https://www.comingsoon.net/wp-content/uploads/sites/3/2023/08/Disney-Plus-Price-Increase-2023.jpg?w=1024"
    elif provider == "HBO":
        Pagecover = "https://uploads.dailydot.com/2020/05/hbo-max.png"
    else:
        Pagecover = "https://images.unsplash.com/photo-1595769816263-9b910be24d5f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDd8fGNpbmVtYXxlbnwwfHx8fDE2OTI1NzAyODB8MA&ixlib=rb-4.0.3&q=80&w=200"
    

    property_field = {
        "Name": Title,
        "Genre": Genre,
        "Program": Program,
        "Homepage": Homepage,
        **({"Release Date": Release_date} if Release_date is not None else {}),
    }

    episode_blocks = []
    if len(episode_array) != 0:
        for episode in episode_array:
            episode_title = f"{episode[0]}. {episode[1]}"
            episode_synopsis = blocks.main_paragraph(episode[2])
            episode_image = blocks.image(episode[3])
            toggle = blocks.toggle(episode_title, episode_synopsis, episode_image)
            episode_blocks.append(toggle)
    else:
        pending_release = blocks.main_paragraph("--- Pending Release ---")
        episode_blocks.append(pending_release)
    
    batch_size = 100
    episode_batches = [episode_blocks[i:i + batch_size] for i in range(0, len(episode_blocks), batch_size)]

    Review = blocks.heading_1("Overall Review")
    Callout = blocks.callout("")
    General = blocks.heading_1("Overview")
    Synopsis = blocks.main_paragraph(synopsis)
    Movie_poster = blocks.image(poster)
    Left_column = blocks.column(Movie_poster)
    Right_column = blocks.modifiedcolumn(episode_batches[0])
    Colomn_list = blocks.column_list(Left_column,Right_column)
    try:
        Left_episode_column = blocks.modifiedcolumn(episode_batches[1])
    except:
        filler = blocks.main_paragraph("")
        Left_episode_column = blocks.column(filler)
    try:
        Right_episode_column = blocks.modifiedcolumn(episode_batches[2])
    except:
        filler = blocks.main_paragraph("")
        Right_episode_column = blocks.column(filler)
    More_episodes = blocks.column_list(Left_episode_column,Right_episode_column)
    content = notion.content_format(Review,Callout,General,Synopsis,Colomn_list,More_episodes)

    page_id = notion.create_page(
        database_id, headers, property_field, content, Pagecover,
    )

    return page_id







