#!/usr/bin/env python2.7
# pylint: disable=too-few-public-methods
""" Classes that import from HttpRequest to use requests package """
import requests

class HttpRequest(object):
    pass

class SteamRequest(HttpRequest):
    def __init__(self, logger):
        self.key = 'E3973E62088C5C78E02E446D4A8491A8'
        self.logger = logger

    def _execute_request(self, args, url):
        args['key'] = self.key
        response = requests.get(url, params=args)
        if response.status_code == 200:
            self.logger.info('Successful query using %s to Steam API.' %
                             type(self))
            return response.json()
        else:
            self.logger.error('Error calling Steam API. %s:%s',
                              response.status_code, response.text)
            raise Exception('Error retrieving data from Steam API. %s:%s' % (
                response.status_code, response.text))

class GetMatchHistoryRequest(SteamRequest):
    def __init__(self, logger):
        self.url = 'https://api.steampowered.com/IDOTA2Match_570/' \
            'GetMatchHistoryBySequenceNum/v0001'
        super(GetMatchHistoryRequest, self).__init__(logger)

    def query_api(self, sequence_num, matches_requested=None):
        args = {}
        args['sequence_num'] = sequence_num
        if matches_requested != None:
            args['matches_requested'] = matches_requested

        return self._execute_request(args, self.url)

class GetHeroesRequest(SteamRequest):
    def __init__(self, logger):
        self.url = 'https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001'
        super(GetHeroesRequest, self).__init__(logger)

    def query_api(self):
        args = {}
        return self._execute_request(args, self.url)
