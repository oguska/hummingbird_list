from __future__ import unicode_literals, division, absolute_import
import logging
import re
import json
import urllib.request as urllib2
import requests

from requests import RequestException

from flexget import plugin
from flexget.entry import Entry
from flexget.event import event
from flexget.utils.cached_input import cached

log = logging.getLogger('hummingbird_list')

class HummingbirdList(object):
    """Creates an entry for each item in your hummingbird.me list.
    Syntax:
    hummingbird_list:
      username: <value>
      lists: 
      	- <currently-watching|plan-to-watch|completed|on-hold|dropped>
      	- <currently-watching|plan-to-watch|completed|on-hold|dropped>
      latest: <yes|no>
      currentonly: <yes|no>
      finishedonly: <yes|no>
    """

    schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'lists': {'type': 'array', 'items': {'type': 'string'}},
            'latest': {'type': 'boolean', 'default': False},
            'currentonly': {'type': 'boolean', 'default': False},
            'finishedonly': {'type': 'boolean', 'default': False}
        },
        'required': ['username'],
        'additionalProperties': False,
    }

    @cached('hummingbird_list', persist='2 hours')
    def on_task_input(self, task, config):

        url = "http://hummingbird.me/api/v1/users/%s/library" % (config['username'])
        try:
            data = requests.get(url).json()
        except ValueError:
            raise plugin.PluginError('Error getting list from hummingbird.')

        if not data:
            return

        entries = []
        chosen_lists = config['lists']
        for item in data:
            if item['status'] not in chosen_lists:
                continue
            if item['anime']['show_type'] == 'Movie':
                continue
            if config.get('currentonly') and item['anime']['status'] != 'Currently Airing':
                continue
            if config.get('finishedonly') and item['anime']['status'] != 'Finished Airing':
                continue    
            entry = Entry()
            entry['title'] = item['anime']['title']
            entry['url'] = ''
            if entry.isvalid():
                if config.get('latest'):
                    entry['series_episode'] = item['episodes_watched']
                    entry['series_id_type'] = 'sequence'
                    entry['title'] += ' ' + str(entry['series_episode'])
                entries.append(entry)

        return entries


@event('plugin.register')
def register_plugin():
    plugin.register(HummingbirdList, 'hummingbird_list', api_ver=2)
