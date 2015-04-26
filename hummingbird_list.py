from __future__ import unicode_literals, division, absolute_import
import logging
import re
import json
import urllib2

from requests import RequestException

from flexget import plugin
from flexget.entry import Entry
from flexget.event import event
from flexget.utils.cached_input import cached


class HummingbirdList(object):
    """Creates an entry for each item in your hummingbird.me list.
    Syntax:
    trakt_list:
      username: <value>
      type: <shows|movies|all>
      list: <currently-watching|plan-to-watch|completed|on-hold|dropped|all>
      latest: <yes|no>
      currentonly: <yes|no>
    """

    schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'type': {'type': 'string', 'enum': ['shows', 'movies', 'all']},
            'list': {'type': 'string', 'enum': ['currently-watching', 'plan-to-watch', 'completed', 'on-hold', 'dropped', 'all']},
            'latest': {'type': 'boolean', 'default': False},
            'currentonly': {'type': 'boolean', 'default': False}
        },
        'required': ['username', 'type', 'list'],
        'additionalProperties': False
    }

    @cached('hummingbird_list', persist='2 hours')
    def on_task_input(self, task, config):

        url = "http://hummingbird.me/api/v1/users/%s/library" % (config['username'])
        try:
            data = json.load(urllib2.urlopen(url))
        except ValueError:
            raise plugin.PluginError('Error getting list from hummingbird.')

        if not data:
            return

        entries = []
        list_type = (config['type']).rstrip('s')
        chosen_list = config['list']
        for item in data:
            if chosen_list != 'all' and item['status'] != chosen_list:
                continue
            if list_type == 'movie':
                if 'show_type' in item and item['anime']['show_type'] != 'Movie':
                    continue
            else:
                if list_type == 'show' and 'show_type' in item and item['anime']['show_type'] == 'Movie':
                    continue
            if config.get('currentonly') and item['anime']['show_type'] != 'Movie' and item['anime']['status'] != 'Currently Airing':
                continue
            entry = Entry()
            entry['title'] = item['anime']['title']
            entry['url'] = ''
            if entry.isvalid():
                if config.get('latest') and item['anime']['show_type'] != 'Movie':
                    entry['url'] = item['anime']['url']
                    entry['series_episode'] = item['episodes_watched']
                    entry['series_id_type'] = 'sequence'
                    entry['title'] += ' ' + str(entry['series_episode'])
                entries.append(entry)

        return entries


@event('plugin.register')
def register_plugin():
    plugin.register(HummingbirdList, 'hummingbird_list', api_ver=2)