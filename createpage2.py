# Import Notion Modules
from notionapi import blocks
from notionapi import property
from notionapi import notion


class NotionAPI:
    def __init__(self, DATABASE_ID,HEADERS):
        self.database_id = DATABASE_ID
        self.headers = HEADERS
    
    def check_connection(self):
        response_data = notion.get_database(self.database_id,self.headers)
        return response_data
    
    def create_movie_property(self,program,title,genre,homepage,release_date):
        Title = property.title(title)
        Genre = property.multi_select(genre)
        Program =  property.select(program)
        Homepage = property.url(homepage) if homepage != '' else None
        Release_date = property.date(release_date) if release_date is not None else None

        property_field = {
            "Name": Title,
            "Genre": Genre,
            "Program": Program,
            **({"Homepage": Homepage} if Homepage is not None else {}),
            **({"Release Date": Release_date} if Release_date is not None else {}),
        }

        return property_field
    
    def create_movie_format(self,synopsis,poster):
        """Create movie page in Notion DB

        Args:
            synopsis (str): overview of the movie
            poster (str): url link to poster
            provider (str): provider of movie

        Returns:
            str: Notion page ID
        """

        Review = blocks.heading_1("Overall Review")
        Callout = blocks.callout("")
        Movie_poster = blocks.image(poster)
        Left_column = blocks.column(Movie_poster)
        Synopsis = blocks.main_paragraph(synopsis)
        Right_column = blocks.column(Synopsis)
        Colomn_list = blocks.column_list(Left_column,Right_column)
        content = notion.content_format(Review,Callout,Colomn_list)

        return content
    
    def create_movie_page(self,property_field,provider,content):
        provider_pagecover_mapping = {
            "Netflix": "https://i.pcmag.com/imagery/reviews/05cItXL96l4LE9n02WfDR0h-5..v1582751026.png",
            "Amazon Prime Video": "https://www.recode.id/wp-content/uploads/2023/01/prime-video.jpg",
            "Amazon Video": "https://www.recode.id/wp-content/uploads/2023/01/prime-video.jpg",
            "Apple TV": "https://images.unsplash.com/photo-1608446781624-bb081c6c0e18?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDJ8fGFwcGxlJTIwdHZ8ZW58MHx8fHwxNjkyNTg3OTYzfDA&ixlib=rb-4.0.3&q=80&w=200",
            "Apple TV+": "https://images.unsplash.com/photo-1608446781624-bb081c6c0e18?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDJ8fGFwcGxlJTIwdHZ8ZW58MHx8fHwxNjkyNTg3OTYzfDA&ixlib=rb-4.0.3&q=80&w=200",
            "Disney Plus": "https://www.comingsoon.net/wp-content/uploads/sites/3/2023/08/Disney-Plus-Price-Increase-2023.jpg?w=1024",
            "HBO": "https://assets.beartai.com/uploads/2023/06/hbo-go.jpg"
        }

        default_url = "https://images.unsplash.com/photo-1595769816263-9b910be24d5f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDd8fGNpbmVtYXxlbnwwfHx8fDE2OTI1NzAyODB8MA&ixlib=rb-4.0.3&q=80&w=200"
        pagecover = provider_pagecover_mapping.get(provider, default_url)

        page_id = notion.create_page(
            self.database_id, self.headers, property_field, content, pagecover,
        )

        return page_id
    
    def create_series_property(self,program,season_name,title,genre,homepage,release_date):
        Title = property.title(f"{title} ({season_name})")
        Genre = property.multi_select(genre)
        Program =  property.select(program)
        Homepage = property.url(homepage) if homepage != '' else None
        Release_date = property.date(release_date) if release_date is not None else None

        property_field = {
            "Name": Title,
            "Genre": Genre,
            "Program": Program,
            **({"Homepage": Homepage} if Homepage is not None else {}),
            **({"Release Date": Release_date} if Release_date is not None else {}),
        }

        return property_field

    def create_series_format(self,episode_array,synopsis,poster):
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
        return content

    
    def create_series_page(self,property_field,provider,content):
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
        provider_pagecover_mapping = {
            "Netflix": "https://i.pcmag.com/imagery/reviews/05cItXL96l4LE9n02WfDR0h-5..v1582751026.png",
            "Amazon Prime Video": "https://www.recode.id/wp-content/uploads/2023/01/prime-video.jpg",
            "Amazon Video": "https://www.recode.id/wp-content/uploads/2023/01/prime-video.jpg",
            "Apple TV": "https://images.unsplash.com/photo-1608446781624-bb081c6c0e18?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDJ8fGFwcGxlJTIwdHZ8ZW58MHx8fHwxNjkyNTg3OTYzfDA&ixlib=rb-4.0.3&q=80&w=200",
            "Apple TV+": "https://images.unsplash.com/photo-1608446781624-bb081c6c0e18?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDJ8fGFwcGxlJTIwdHZ8ZW58MHx8fHwxNjkyNTg3OTYzfDA&ixlib=rb-4.0.3&q=80&w=200",
            "Disney Plus": "https://www.comingsoon.net/wp-content/uploads/sites/3/2023/08/Disney-Plus-Price-Increase-2023.jpg?w=1024",
            "HBO": "https://assets.beartai.com/uploads/2023/06/hbo-go.jpg"
        }

        default_url = "https://images.unsplash.com/photo-1595769816263-9b910be24d5f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDd8fGNpbmVtYXxlbnwwfHx8fDE2OTI1NzAyODB8MA&ixlib=rb-4.0.3&q=80&w=200"
        pagecover = provider_pagecover_mapping.get(provider, default_url)


        page_id = notion.create_page(
            self.database_id, self.headers, property_field, content, pagecover ,
        )

        return page_id
    