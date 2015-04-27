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

log = logging.getLogger('hummingbird_movies')

class HummingbirdMovies(object):
    """Creates an entry for each item in your hummingbird.me list.
    Syntax:
    hummingbird_movies:
      username: <value>
      lists: 
      	- <currently-watching|plan-to-watch|completed|on-hold|dropped>
      	- <currently-watching|plan-to-watch|completed|on-hold|dropped>
    """

    schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'lists': {'type': 'array', 'items': {'type': 'string'}},
        },
        'required': ['username'],
        'additionalProperties': False,
    }

    @cached('hummingbird_movies', persist='2 hours')
    def on_task_input(self, task, config):

        url = "http://hummingbird.me/api/v1/users/%s/library" % (config['username'])
        try:
            data = json.load(urllib2.urlopen(url))
        except ValueError:
            raise plugin.PluginError('Error getting list from hummingbird.')

        if not data:
            return

        entries = []
        chosen_lists = config['lists']
        for item in data:
            if item['status'] not in chosen_lists:
                continue
            if item['anime']['show_type'] != 'Movie':
                continue 
            entry = Entry()
            entry['title'] = item['anime']['title']
            entry['url'] = ''
            if entry.isvalid():
                entries.append(entry)

        return entries


@event('plugin.register')
def register_plugin():
    plugin.register(HummingbirdMovies, 'hummingbird_movies', api_ver=2)