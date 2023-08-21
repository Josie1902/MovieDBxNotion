import json
import requests

def display_json(res):
    """For error handling

    Args:
        res (response): response variable which gets/posts/patch from Notion API
    """
    # Retuns back a dictionary
    json_data = res.json()
    # Takes in dictionary and output formatted json
    formatted_json = json.dumps(json_data, indent=2)
    print(formatted_json)

def get_database(database_id, headers):
    """Checks whether we are connected to the database

    Args:
        database_id (str): Id from notioin database (can be found in url)
        headers (dict): Permissions to Notion API
    
    Returns: 
        dict: Accessible dicts to be modified by user
    """
    # Get a list of pages from databse
    database_url = f"https://api.notion.com/v1/databases/{database_id}/query"
    res = requests.post(database_url, headers=headers)
    # Make response editable as a json
    response_data = res.json()
    # Check for errors
    if res.status_code == 400 or res.status_code == 404 or res.status_code == 429:
        display_json(res)
    else:
        print(f"{res.status_code}: Successful response!")

    return response_data

# Data input
def content_format(*blocks):
    """In descending order of blocks to be formatted in Notion page

    Returns:
        list: blocks in a list
    """
    # List of main structure of the page
    main_children = []
    # Main structure of the page
    main_children.extend(blocks)
    return main_children

def create_page(
    database_id,
    headers,
    property_field,
    content_format=[],
    cover="https://www.shutterstock.com/blog/wp-content/uploads/sites/5/2020/02/Usign-Gradients-Featured-Image.jpg",
    emoji="🗿",
):
    """Add a Notion page to a database with given properties and blocks

    Args:
        database_id (str): Id from Notion database (can be found in url)
        headers (dict): Permissions to Notion API
        property_field (dict): Requires properties
        content_format (list, optional): Add content. Defaults to [].
        cover (str, optional): Add cover page. Defaults to "https://www.shutterstock.com/blog/wp-content/uploads/sites/5/2020/02/Usign-Gradients-Featured-Image.jpg".
        emoji (str, optional): Add cover emoji. Defaults to "🗿".
    
    Note:
        For properties, define them in the columns of your database first.
        If not, there would be a "property does not exist".
    """
    page_url = "https://api.notion.com/v1/pages"
    # Writing out the new page
    new_page = {
        "cover": {"type": "external", "external": {"url": cover}},
        "icon": {"type": "emoji", "emoji": emoji},
        "parent": {"type": "database_id", "database_id": database_id,},
        "properties": property_field,
        "children": content_format,
    }

    data = json.dumps(new_page)
    res = requests.post(page_url, headers=headers, data=data)
    # Check for errors
    if res.status_code == 400 or res.status_code == 404 or res.status_code == 429:
        display_json(res)
    else:
        response_data = res.json()
        page_id = response_data.get('id')
        return page_id
