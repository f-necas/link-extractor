import re, sys, argparse, requests

body = """
{
  "aggregations": {},
  "from": 0,
  "size": 10000,
  "sort": [{"_score": "desc"}],
  "query": {
    "bool": {
      "must": [],
      "must_not": {"terms": {"resourceType": ["service","map","map/static","mapDigital"]}},
      "should": [],
      "filter": [{"terms": {"isTemplate": ["n"]}}]
    }
  },
  "track_total_hits": true,
  "_source": ["link.urlObject.default"]
}
"""

parser = argparse.ArgumentParser(description='')
parser.add_argument('-g', '--gn-url', type=str, help='URL to search for e.g. https://dev.georchestra.org/geonetwork', required=True)
parser.add_argument('-t', '--tpl', type=str, help='Custom output template, must contain DOMAIN_TPL and EXTENSION_TPL string inside', default='template_output.txt')
parser.add_argument('-wr', '--write-response', type=bool, help='Write response in file', default=False, const=True, nargs='?')
args = parser.parse_args()

with open(args.tpl, 'r') as f:
    template = f.read()

def apply_template(value: str):
    return (template
            .replace('DOMAIN_TPL', value.split(".")[0])
            .replace('EXTENSION_TPL', value.split(".")[1]))

def get_domain(domain_pattern: str, url: str):
    if domain_pattern.search(url):
        return domain_pattern.findall(url)[0]
    return None

def main():
    res = requests.post(args.gn_url + '/srv/api/search/records/_search?bucket=bucket', data=body, headers={'Content-Type': 'application/json', "accept": "application/json"})

    if args.write_response:
        with open('body_response.json', 'w') as wf:
            wf.write(str(res.json()))

    with open('results.txt', 'w') as wf:
        content = str(res.json())
        url_pattern = re.compile(r'default[\s:\']*https?://([^/"\']*)')
        domain_pattern = re.compile(r'([^\.]+\.[a-z]+)[:\d]*$')
        urls = set(list(filter(None, url_pattern.findall(content))))
        domains = set(filter(None, [get_domain(domain_pattern, url) for url in urls]))
        for domain in domains:
            wf.write(apply_template(domain))

    print('Done with', domains.__len__(), 'unique domains')

if __name__ == '__main__':
    sys.exit(main())




