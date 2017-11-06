import json, requests as req
from time import sleep

def urljoin(*parts):
    return '/'.join(s.strip('/') for s in parts)

class Tracker():
    def __init__(self, cfg_location, callback):
        cfg = get_cfg(cfg_location)
        self.callback = callback
        self.jira = Jira(cfg['url'], req.auth.HTTPBasicAuth(cfg['username'], cfg['password']))
        self.wait_time = cfg['wait_time_s']
        self.filter = cfg['filter']
        self.wip_limit = cfg['wip_limit']
        self.running = False
    def run(self):
        self.running = True
        jql = 'status = "In progress" AND {}'.format(self.jira.get_filter(self.filter)['jql'])
        while self.running:
            search = self.jira.search(jql)
            issues = len(search['issues'])
            self.callback(issues <= self.wip_limit)
            sleep(self.wait_time)
    def stop(self):
        self.running = False

class Jira():
    def __init__(self, url, auth):
        self.auth = auth
        self.url = url
    def get_filter(self, filter_id):
        url = urljoin(self.url, 'rest/api/2/filter/{}'.format(filter_id))
        resp = req.request('GET', url, auth=self.auth)
        return resp.json()
    def search(self, jql):
        url = urljoin(self.url, '/rest/api/2/search')
        resp = req.request('GET', url, auth=self.auth, params={'jql':jql, 'validateQuery':'false', 'expand': []})
        return resp.json()

def get_cfg(cfg_location):
    with open(cfg_location) as cfg_file:
        return json.load(cfg_file)
