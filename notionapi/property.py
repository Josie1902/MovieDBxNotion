def title(content):
    """Insert title

    Args:
        content (str):Insert what you want to type

    Returns:
        dict: Placeholder dictionary for title to be used in "properties"
    """
    title_structure = ({"title": [{"text": {"content": content}}]},)
    return title_structure[0]

def text(
    content,
):
    """Insert text 

    Args:
        content (str): Insert what you want to type

    Returns:
        dict: Placeholder dictionary for text to be used in "properties"
    """
    text_structure = {
        "rich_text": [
            {
                "text": {"content": content},
            }
        ]
    }
    return text_structure

def select(name):
    """Select a tag

    Args:
        name (str): Give the tag a name

    Returns:
        dict: Placeholder dictionary for select to be used in "properties"
    """
    select_structure = {"select": {"name": name}}
    return select_structure

def multi_select(tags):
    """Select multiple tags

    Args:
        *names (str): Make multiple tags

    Returns:
        dict: Placeholder dictionary for multi-select to be used in "properties"
    """
    multi_tags = []
    for tag in tags:
        multi_tags.append({"name": tag})
    multi_select_structure = {"multi_select": multi_tags}
    return multi_select_structure

def url(url):
    """Insert url

    Args:
        url (str): Insert url 

    Returns:
         dict: Placeholder dictionary for url to be used in "properties"
    """
    url_structure = {"url": url}
    return url_structure

def date(date):
    """Insert date

    Args:
        date (str): in ISO8601 format

    Returns:
          dict: Placeholder dictionary for date to be used in "properties"
    """
    date_structure ={"date": {
      "start": date
    }}
    return date_structure
                     