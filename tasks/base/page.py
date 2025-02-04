import traceback

from tasks.base.assets.assets_base_page import *


class Page:
    # Key: str, page name like "page_main"
    # Value: Page, page instance
    all_pages = {}

    @classmethod
    def clear_connection(cls):
        for page in cls.all_pages.values():
            page.parent = None

    @classmethod
    def init_connection(cls, destination):
        """
        Initialize an A* path finding among pages.

        Args:
            destination (Page):
        """
        cls.clear_connection()

        visited = [destination]
        visited = set(visited)
        while 1:
            new = visited.copy()
            for page in visited:
                for link in cls.iter_pages():
                    if link in visited:
                        continue
                    if page in link.links:
                        link.parent = page
                        new.add(link)
            if len(new) == len(visited):
                break
            visited = new

    @classmethod
    def iter_pages(cls):
        return cls.all_pages.values()

    @classmethod
    def iter_check_buttons(cls):
        for page in cls.all_pages.values():
            yield page.check_button

    def __init__(self, check_button):
        self.check_button = check_button
        self.links = {}
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self.name = text[:text.find('=')].strip()
        self.parent = None
        Page.all_pages[self.name] = self

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def link(self, button, destination):
        self.links[destination] = button


# Main page
page_main = Page(MAIN_GOTO_CHARACTER)

# Menu, entered from phone
page_menu = Page(MENU_CHECK)
page_menu.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_MENU, destination=page_menu)

# Character
page_character = Page(CHARACTER_CHECK)
page_character.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_CHARACTER, destination=page_character)

# Team
page_team = Page(TEAM_CHECK)
page_team.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_TEAM, destination=page_team)

# Item, storage
page_item = Page(ITEM_CHECK)
page_item.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_ITEM, destination=page_item)

# Guide, which includes beginners' guide, daily missions and dungeons
page_guide = Page(GUIDE_CHECK)
page_guide.link(GUIDE_CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_GUIDE, destination=page_guide)

# Gacha
page_gacha = Page(GACHA_CHECK)
page_gacha.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_GACHA, destination=page_gacha)

# Battle Pass
page_battle_pass = Page(BATTLE_PASS_CHECK)
page_battle_pass.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_BATTLE_PASS, destination=page_battle_pass)

# Event
page_event = Page(EVENT_CHECK)
page_event.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_EVENT, destination=page_event)

# Tutorial
page_tutorial = Page(TUTORIAL_CHECK)
page_tutorial.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_TUTORIAL, destination=page_tutorial)

# Mission
page_mission = Page(MISSION_CHECK)
page_mission.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_MISSION, destination=page_mission)

# Message
page_message = Page(MESSAGE_CLOSE)
page_message.link(MESSAGE_CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_MESSAGE, destination=page_message)
