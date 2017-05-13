#    Copyright 2017 Starbot Discord Project
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
'''Wikia API'''
import urllib.request
import json

class Wikia:
    wiki_name = ""

    def __init__(self, wiki):
        self.wiki_name = wiki

    def wikia_search(self, term, limit=1):
        '''Search for a page on Wikia'''
        # TODO: make limits over 1 return an array
        search_term = term.replace(" ", "+")
        url = "http://{}.wikia.com/api/v1/Search/List?query={}&limit=1&minArticleQuality=10&batch=1&namespaces=0%2C14"
        url.format(self.wiki_name, search_term)

        json_string = urllib.request.urlopen(url).read().decode("utf-8")
        json_d = json.loads(json_string)

        return json_d['items']

    def wikia_getpage(self, page_id):
        '''Get a page on Wikia based on the page ID'''
        url = "http://{}.wikia.com/api/v1/Articles/AsSimpleJson?id={}".format(self.wiki_name, page_id)

        json_string = urllib.request.urlopen(url).read().decode("utf-8")
        json_d = json.loads(json_string)

        return json_d['sections']

    def wikia_getdetails(self, page_id):
        '''Get details of a wikia page based on a page ID'''
        url = "http://{}.wikia.com/api/v1/Articles/Details?ids={}&abstract=100&width=200&height=200"
        url.format(self.wiki_name, page_id)

        json_string = urllib.request.urlopen(url).read().decode("utf-8")
        json_d = json.loads(json_string)

        return json_d['items']
