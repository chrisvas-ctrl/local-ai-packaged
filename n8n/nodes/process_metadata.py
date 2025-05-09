import re

cleaned_items = []

for item in _input.all():
    original_json = item.get("json", {})
    loc = original_json.get("loc", "")
    lastmod = original_json.get("lastmod", "")

    # Default values
    article_id = ""
    article_title = ""

    # Try to parse ID and title from the URL
    match = re.search(r"/articles/(\d+)-(.+)", loc)
    if match:
        article_id = match.group(1)
        # Replace hyphens with spaces and decode URL characters
        article_title = match.group(2).replace("-", " ")

    # Create filename by combining title and ID, replacing spaces with hyphens
    filename = f"{article_title.replace(' ', '-')}-{article_id}"

    cleaned_json = {
        "loc": loc,
        "lastmod": lastmod,
        "dataMetadata": {
            "url": loc,
            "articleId": article_id,
            "articleTitle": article_title,
            "filename": filename,
            "lastModified": lastmod,
            "language": "en-us",
        }
    }

    cleaned_items.append({ "json": cleaned_json })

return cleaned_items
