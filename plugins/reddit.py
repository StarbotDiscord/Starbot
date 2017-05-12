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

import json
import random
import urllib.error
import urllib.request
import urllib.parse

from api import command, message, plugin, caching

# Commands.
STARCMD = "star"

def onInit(plugin_in):
    star_command = command.command(plugin_in, STARCMD, shortdesc="Star")
    return plugin.plugin(plugin_in, "reddit", [star_command])

async def onCommand(message_in):
    if message_in.command == STARCMD:
        # Get JSON from Reddit API.
        r_json = caching.getJson("https://www.reddit.com/r/StarVSTheForcesOfEvil/top.json?sort=top&t=week&limit=100",
                                 save=False)
        posts = json.loads(r_json)["data"]["children"]

        # Get random post.
        post = posts[random.randint(0, len(posts) - 1)]["data"]

        # Store URL in here.
        url = None

        # Try to get URL to image, up to 10 times if needed.
        for i in range(0, 10):
            # If the preview is valid, use that.
            if "preview" in post:
                url = post["preview"]["images"][0]["source"]["url"]
            else:
                # Check if URL points to an image.
                ext_list = ["jpg", "jpeg", "png", "gif", "tiff", "tif"]
                ext = post["url"].split(".")[-1]
                if ext in ext_list:
                    url = post["url"]

            # If we have a URL, exit.
            if url:
                break

        if url:
            url_parsed = urllib.parse.urlparse(url)
            caching.downloadToCache(url, url_parsed.path.split("/")[-1], caller=STARCMD)

            return message.message(post["title"], file="cache/{}_{}".format(STARCMD, url_parsed.path.split("/")[-1]))
        else:
            # No URL could be found, return error message.
            return message.message("Whoops! I couldn't find any posts.")
