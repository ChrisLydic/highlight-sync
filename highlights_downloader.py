import sys
import os
import json

from instapaper import Instapaper

class Highlights():
    def __init__(self):
        key = os.environ["INSTAPAPER_KEY"]
        secret = os.environ["INSTAPAPER_SECRET"]
        login = os.environ["INSTAPAPER_LOGIN"]
        password = os.environ["INSTAPAPER_PASSWORD"]
        self.client = Instapaper(key, secret)
        self.client.login(login, password)

    def get_folder_highlights(self, name):
        results = []
        folders = self.client.folders()
        notion_folder = next((x for x in folders if x.get('title') == name))
        if notion_folder is None:
            return []
        bookmarks = self.client.bookmarks(folder=notion_folder.get('folder_id'), limit=50)
        for bookmark in bookmarks:
            highlights = bookmark.get_highlights()
            if len(highlights) > 0:
                results.append(self.parse_highlights(bookmark, highlights))
            bookmark.archive()
        return results

    def parse_highlights(self, bookmark, highlights):
        highlights_json = json.loads(highlights)
        result = {
            'title': bookmark.title,
            'source': bookmark.url,
            'liked': bookmark.starred,
            'highlights': []
        }
        for highlight in highlights_json:
            highlights_dict = {
                "text": highlight['text']
            }
            if highlight.get('note') is not None:
                highlights_dict['note'] = highlight['note']
            result['highlights'].append(highlights_dict)
        return result

if __name__ == '__main__':
    folder_name = sys.argv[1]
    instapaper_client = Highlights()
    print(instapaper_client.get_folder_highlights(folder_name))