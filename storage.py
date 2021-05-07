"module building all data to be stored"
import os
from types import SimpleNamespace
import json
from dotenv import load_dotenv
import requests
from jinja2 import Template


class InfoController():
    def __init__(self, source, category):
        self.source = source
        self.category = category

    def create_if_none(self, ctx):
        if self.category not in self.source[str(ctx.channel.id)]:
            self.source[str(ctx.channel.id)][self.category] = []

    async def add(self, ctx, *args):
        self.create_if_none(ctx)
        for item in args[0]:
            self.source[str(ctx.channel.id)][self.category].append(item)

    async def remove(self, ctx, *args):
        self.create_if_none(ctx)

        for item in args[0]:
            self.source[str(ctx.channel.id)][self.category].remove(item)

    async def clear(self, ctx, *args):
        self.create_if_none(ctx)

        self.source[str(ctx.channel.id)][self.category].clear()

    async def lst(self, ctx, *args):
        self.create_if_none(ctx)

        with open('templates/json.md') as file_:
            template = Template(file_.read())

            await ctx.send(
                template.render(data=json.dumps(
                    self.source[str(ctx.channel.id)][self.category], indent=2))
            )

    async def get_data(self, channel_id):
        if self.category in self.source[str(channel_id)]:
            return self.source[str(channel_id)][self.category]
        return None


class Storage():
    def __init__(self, unique_tag='Dark_info:'):
        self.unique_tag = unique_tag
        self.settings = self.load_env_settings()
        self.channels = self.load_channel_settings()

        self.base = InfoController(self.channels, 'base')
        self.system = InfoController(self.channels, 'system')
        self.region = InfoController(self.channels, 'region')
        self.friend = InfoController(self.channels, 'friend')
        self.enemy = InfoController(self.channels, 'enemy')

    def load_env_settings(self) -> SimpleNamespace:
        "loading settings from os environment"
        load_dotenv()

        output = SimpleNamespace()
        for item, value in os.environ.items():
            setattr(output, item, value)
        return output

    def load_channel_settings(self) -> dict:
        """loadding perssistent settings
        set by users about channels"""
        output = {}
        try:
            with open('channels.json', 'r') as file_:
                output = json.loads(file_.read())
        except FileNotFoundError:
            print('ERR failed to load channels.json')
        return output

    def save_channel_settings(self) -> None:
        """loadding perssistent settings
        set by users about channels"""
        try:
            with open('channels.json', 'w') as file_:
                file_.write(json.dumps(self.channels, indent=2))
        except OSError:
            print('ERR failed to save channels.json')

    def get_game_data(self) -> SimpleNamespace:
        output = SimpleNamespace()
        output.players = requests.get(self.settings.player_request_url).json()
        output.bases = requests.get(self.settings.base_request_url).json()
        return output

    def base_add(self, name):
        print('adding the base')

    # def get_channel_data(self, key) -> SimpleNamespace:
    #     return deepcopy(self.storage.channels[key])
