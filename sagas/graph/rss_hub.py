import feedparser
import json
import urllib.request
import shutil
from requests import get  # to make GET request
from tqdm import tqdm

import json_utils
import sagas.graph.dgraph_helper as helper
import pydgraph

"""
# procs-rss.ipynb
"""

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

def print_entry_fields(entry):
    from dateutil.parser import parse

    print('♮id', entry.id) # corresponding to guid
    print('♮title', entry.title) # title
    print(parse(entry.published).isoformat())
    print('♮link', entry.link)
    print('♮summary', entry.summary) # corresponding to description

def iso_date(dt):
    from dateutil.parser import parse
    return parse(dt).isoformat()

def feed_jsonify(feed_data):
    cols=['title', 'link', 'subtitle', 'updated']
    return dict(zip(cols, [feed_data.title, feed_data.link, feed_data.subtitle,
      iso_date(feed_data.updated)]))

def entry_jsonify(entry, lang='ja'):
    import datetime
    if 'published' in entry.keys():
        pub_date=iso_date(entry.published)
    else:
        pub_date=datetime.datetime.now().isoformat()
    return {'id':entry.id, 'title@'+lang:entry.title,
           'published':pub_date,
           'link':entry.link,
           'summary':entry.summary}

feed_schema='''
title: string @index(exact, fulltext) .
link: string @index(exact) .
subtitle: string @index(fulltext) @lang .
updated: datetime .
entry: uid @count .
'''
entry_schema='''
id: string @index(exact) .
title: string @index(fulltext) @lang .
published: datetime .
link: string @index(exact) .
summary: string @index(fulltext) @lang .
'''

def overrides_schema(schema_map, schema):
    for term in schema.split('\n'):
        s=term.strip()
        if len(s)>0:
            parts=s.split(':')
            schema_map[parts[0]]=parts[1]

def build_schema(schema_map):
    rs=[]
    for k,v in schema_map.items():
        rs.append(k+': '+v)
    return '\n'.join(rs)

def set_json(client, val):
    txn = client.txn()
    return txn.mutate(pydgraph.Mutation(commit_now=True), set_obj=val)

def create_resource_digest(url_raw, data_file_prefix, lang='zh'):
    # https://rsshub.app/bilibili/bangumi/media/9192, ja
    parts=url_raw.split(',')
    url=parts[0]
    if len(parts)>1:
        lang=parts[1].strip()
    digest={'url':url}
    digest['file']=data_file_prefix+url.replace('https://rsshub.app/',"").replace('/','_')
    digest['lang']=lang
    return digest

def get_resources(data_file_prefix, url_conf):
    import io_utils
    urls = []
    for url in io_utils.lines(url_conf):
        url = url.strip()
        if len(url) > 0 and not url.startswith('#'):
            urls.append(url)
    # print(urls)
    resources = []
    for url in urls:
        resources.append(create_resource_digest(url, data_file_prefix))
    print(json.dumps(resources, indent=2))
    return resources

def short_url(url):
    return url.replace('https://rsshub.app/',"")

class RssHub(object):
    def __init__(self, data_prefix='data/rss/'):
        self.data_file_prefix = data_prefix

    def downloads(self):
        url = "https://rsshub.app/bilibili/user/video/286700005"
        file_name = "./data/rss/user_video_286700005.xml"
        download(url, file_name)

    def entry_keys(self, file_name):
        feed = feedparser.parse(file_name)
        entry = feed.entries[0]
        print(entry.keys())
        print_entry_fields(entry)

    def feed_data(self, file_name, jsonify=True):
        feed = feedparser.parse(file_name)
        feed_data = feed['feed']
        if jsonify:
            # print(json.dumps(feed_data, ensure_ascii=False, indent=2))
            print(feed_data.keys())
            print(json.dumps(feed_jsonify(feed_data), indent=2, ensure_ascii=False))
        else:
            print(feed_data.title, feed_data.link, feed_data.subtitle,
                  iso_date(feed_data.updated))

    def check_feeds(self, jsonify=False):
        """
        $ python -m sagas.graph.rss_hub check_feeds
        $ python -m sagas.graph.rss_hub check_feeds True
        :return:
        """
        from io_utils import list_with_suffix
        files = list_with_suffix('data/rss', '.xml')
        for file in files:
            print('.. check', file)
            self.feed_data(file, jsonify)

    def entry(self, file_name, index=0, jsonify=True):
        feed = feedparser.parse(file_name)
        entry = feed.entries[index]

        if jsonify:
            print(json.dumps(entry_jsonify(entry), indent=2, ensure_ascii=False))
        else:
            print_entry_fields(entry)

    def get_feed_json(self, file_name, lang='ja'):
        feed = feedparser.parse(file_name)
        feed_data = feed['feed']
        entries = []
        feed_json = feed_jsonify(feed_data)
        for entry in feed.entries:
            entries.append(entry_jsonify(entry, lang))
        feed_json['entry'] = entries
        return feed_json

    def write_feed_json(self, file_name, out_file_name, lang='ja'):
        import json_utils
        # out_file_name = "./data/rss/user_video_286700005.json"
        feed_json=self.get_feed_json(file_name, lang)

        # print(json.dumps(feed_json, indent=2, ensure_ascii=False))
        json_utils.write_json_to_file(out_file_name, feed_json)

    def get_schema_map(self):
        schema_map = {}
        overrides_schema(schema_map, feed_schema)
        overrides_schema(schema_map, entry_schema)
        return (build_schema(schema_map))

    def fill_feed(self, file_name):
        """
        $ python -m sagas.graph.rss_hub fill_feed "./data/rss/user_video_286700005.xml"
        :param file_name:
        :return:
        """
        feed_json = self.get_feed_json(file_name)
        schema_map=self.get_schema_map()
        client = helper.reset(schema_map)
        _ = set_json(client, feed_json)

    def some_query(self):
        """
        $ python -m sagas.graph.rss_hub some_query
        :return:
        """
        client = helper.create_client()
        helper.run_q(client, '''{
          data(func: alloftext(title, "bilibili")) {
             title@en:.
             link
          }
        }''')
        helper.run_q(client, '''{
          data(func: alloftext(title@zh, "长柄")) {
             title@zh
             link
          }
        }''')
        helper.run_q(client, '''{
          data(func: alloftext(title@ja, "卒業")) {
            title@ja
            link
          }
        }''')
        helper.run_q(client, '''{
          data(func: alloftext(title@ja, "夏色")) {
            title@ja
            link
          }
        }''')

    def proc_resources(self, url_conf='./data/rss/urls.txt'):
        """
        $ python -m sagas.graph.rss_hub proc_resources
        :param url_conf:
        :return:
        """
        import os
        resources=get_resources(self.data_file_prefix, url_conf)
        pbar = tqdm(resources)
        for res in pbar:
            path = res['file'] + '.xml'
            json_path = res['file'] + '.json'
            pbar.set_description("proc %s" % short_url(res['url']))
            if os.path.isfile(path):
                # print('%s exists'%path)
                pass
            else:
                download(res['url'], path)
            if not os.path.isfile(json_path):
                self.write_feed_json(path, json_path, lang=res['lang'])
        print('done')

    def load_resources(self):
        """
        $ python -m sagas.graph.rss_hub load_resources
        :return:
        """
        from io_utils import list_with_suffix
        schema_map = self.get_schema_map()
        client = helper.reset(schema_map)

        files = list_with_suffix('data/rss', '.json')
        for file in tqdm(files):
            feed_json = json_utils.read_json_file(file)
            # feed_json = self.get_feed_json(file)
            _ = set_json(client, feed_json)

if __name__ == '__main__':
    import fire
    fire.Fire(RssHub)

