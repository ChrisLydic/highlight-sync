import sys
import json
import os
from notion.client import NotionClient
from notion.block import TextBlock, BulletedListBlock

class Notion():
    def __init__(self, url):
        token = os.environ["NOTION_TOKEN"]
        client = NotionClient(token_v2=token)
        self.cv = client.get_collection_view(url)

    def add_page(self, article):
        row = self.cv.collection.add_row()
        row.name = article.get('title')
        row.tags = ["Highlights"]
        if article.get('authors') is not None:
            row.text_source = article.get('authors')
        if article.get('source') is not None:
            row.source = article.get('source')
        for highlight in article.get('highlights'):
            row.children.add_new(BulletedListBlock, title=highlight.get('text'))
            if highlight.get('note') is not None:
                row.children.add_new(TextBlock, title=highlight.get('note'))

if __name__ == '__main__':
    filename = sys.argv[1]
    url = sys.argv[2]
    with open(filename, 'r', encoding='utf8') as f:
        article = json.load(f)
    if article.get('highlights') is None:
        print("Error: input file does not have highlights")
        exit()
    notion_client = Notion(url)
    notion_client.add_page(article)