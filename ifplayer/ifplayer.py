import eel
import xml.etree.ElementTree as ET
import sys
import os

eel.init('web')

class Story:
    def __init__(self, file_path):
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        self.current_page = None

    def get_page(self, page_id):
        return self.root.find(f".//part[@id='{page_id}']")

    def get_intro(self):
        intro = self.root.find("intro")
        if intro is not None:
            return {
                "title": intro.findtext("title", "Untitled Story"),
                "author": intro.findtext("author", "Anonymous"),
                "image": intro.findtext("image", ""),
                "audio": {
                    "src": intro.findtext("audio", ""),
                    "autoplay": intro.find("audio").get("autoplay", "false").lower() == "true" if intro.find("audio") is not None else False
                } if intro.find("audio") is not None else None,
                "choices": [{"text": choice.get("text"), "action": choice.get("action")} 
                            for choice in intro.findall("choice")]
            }
        return None

    def start(self):
        self.current_page = self.get_page("page_1")
        return self.get_current_content()

    def get_current_content(self):
        if self.current_page is None:
            return None

        content = {
            "id": self.current_page.get("id"),
            "text": self.current_page.findtext("text", ""),
            "choices": [{"text": choice.get("text"), "next": choice.get("next")} 
                        for choice in self.current_page.findall("choice")],
            "image": self.current_page.findtext("image", ""),
            "audio": self.current_page.findtext("audio", ""),
            "video": None
        }

        video_elem = self.current_page.find("video")
        if video_elem is not None:
            content["video"] = {
                "src": video_elem.text,
                "autoplay": video_elem.get("autoplay", "false").lower() == "true"
            }

        return content

    def make_choice(self, next_id):
        self.current_page = self.get_page(next_id)
        return self.get_current_content()

story = Story("story.ifg")
  
@eel.expose
def get_intro():
    return story.get_intro()

@eel.expose
def start_story():
    return story.start()

@eel.expose
def make_choice(next_id):
    return story.make_choice(next_id)

@eel.expose
def exit_app():
    sys.exit()

eel.start('index.html', size=(800, 600), block=False)

while True:
    eel.sleep(1.0)
    if not eel._shutdown:
        continue
    else:
        break
