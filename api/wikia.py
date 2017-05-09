import urllib.request
import json

class Wikia:
    wiki_name = ""

    def __init__(self, wiki):
        self.wiki_name = wiki

    def search(self, term, limit=1):
        # Search for a page on Wikia
        # TODO: make limits over 1 return an array
        searchTerm = term.replace(" ", "+")
        url = "http://starvstheforcesofevil.wikia.com/api/v1/Search/List?query={}&limit=1&minArticleQuality=10&batch=1&namespaces=0%2C14".format(searchTerm)

        jsonString = urllib.request.urlopen(url).read().decode("utf-8")
        json_d = json.loads(jsonString)

        return json_d['items']

    def getPage(self, page_id):
        # Get a page on Wikia based on the page ID
        url = "http://starvstheforcesofevil.wikia.com/api/v1/Articles/AsSimpleJson?id={}".format(page_id)

        jsonString = urllib.request.urlopen(url).read().decode("utf-8")
        json_d = json.loads(jsonString)

        return json_d['sections']