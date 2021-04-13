import sys
from highlights_downloader import Highlights
from notion_uploader import Notion

if len(sys.argv) < 3:
    print("usage: main.py <instapaper_folder_name> <notion_database_url>")
    exit()
folder_name = sys.argv[1]
database_url= sys.argv[2]
highlights = Highlights()
notion = Notion(database_url)
notion_articles = highlights.get_folder_highlights(folder_name)
for article in notion_articles:
    print(f"Processing article: {article.title}")
    notion.add_page(article)