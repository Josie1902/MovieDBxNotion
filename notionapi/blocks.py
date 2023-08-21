def heading_1(
    content,
    color="orange_background",
):
    """Heading 1

    Args:
        content (str): Insert what you want to type
        color (str, optional): Colour of text. Defaults to "orange_background".

    Returns:
        dict: dict: Placeholder dictionary for heading 1 to be used in "children"
    """
    heading_1_structure = {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": content},
                }
            ],
            "color": color,
        },
    }
    return heading_1_structure

def image(url):
    """Includes supported image urls (i.e. ending in .png, .jpg, .jpeg, .gif, .tif, .tiff, .bmp, .svg, or .heic)

    Args:
        url (str): Link address of image 

    Returns:
        dict: Placeholder dictionary for image to be used in "children"
    """
    image_structure = {
        "object": "block",
        "type": "image",
        "image": {"type": "external", "external": {"url": url},},
    }
    return image_structure

def callout(content, *nestedblocks, emoji="👀", color="gray_background"):
    """Callout block

    Args:
        content (str): Insert a paragraph
        emoji (str, optional): Choose an emoji. Defaults to "". 
        color (str, optional): Choose a colour. Defaults to "default".

    Returns:
        dict : Placeholder dictionary for callout to be used in "children"

    Notes:
        colors: "default", "gray", "brown", "orange", "yellow", "green", "blue", "purple", "pink", "red", 
        "gray_background", "brown_background", "orange_background", "yellow_background", "green_background", 
        "blue_background", "purple_background", "pink_background", "red_background"
    """
    children_blocks = []
    for nestedblock in nestedblocks:
        children_blocks.append(nestedblock)

    callout_structure = {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": content,},}],
            "icon": {"emoji": emoji},
            "color": color,
            "children": children_blocks,
        },
    }
    return callout_structure

def column_list(*columnblocks):
    """Columns read from right to left according to added arguments 

    Args:
        columnblock (var): A variable from column function 

    Returns:
        dict : Placeholder dictionary for column list to be used in "children"
    """
    column_list_children = []
    for column in columnblocks:
        column_list_children.append(column)

    column_list_structure = {
        "object": "block",
        "type": "column_list",
        "column_list": {"children": column_list_children},
    }
    return column_list_structure


def column(*nestedblocks):
    """A single column

    Returns:
       dict : Placeholder dictionary for column to be used in "children"
    """
    children_blocks = []
    for nestedblock in nestedblocks:
        children_blocks.append(nestedblock)

    column_structure = {
        "object": "block",
        "type": "column",
        "column": {"children": children_blocks},
    }
    return column_structure



def modifiedcolumn(children_blocks):
    """A single column that accepts array as a parameter

    Returns:
       dict : Placeholder dictionary for column to be used in "children"
    """

    column_structure = {
        "object": "block",
        "type": "column",
        "column": {"children": children_blocks},
    }
    return column_structure

def main_paragraph(
    content,
):
    """Main paragraph block

    Args:
        content (str): Insert what you want to type

    Returns:
        dict: Placeholder dictionary for paragraph to be used in "children"
    
    """
    main_paragraph_structure = {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": content},
                }
            ],
        },
    }
    return main_paragraph_structure

def toggle(
    content,
    *nestedblocks,
):
    """A simple toggle

    Args:
        content (str): Insert what you want to type

    Returns:
        dict: Placeholder dictionary for toggle to be used in "children"
    """
    children_blocks = []
    for nestedblock in nestedblocks:
        children_blocks.append(nestedblock)

    toggle_structure = {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": content},
                }
            ],
            "children": children_blocks,
        },
    }

    return toggle_structure