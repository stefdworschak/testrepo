import argparse
import json
import requests

def main(args):
    request_params = {}
    pull_request_number = str(args.pull_request_number)
    url_params = {
        'repository': args.repository,
        'pull_request_number': pull_request_number,
    }
    url = 'https://api.github.com/repos/%(repository)s/pulls/%(pull_request_number)s' % url_params
    res = requests.get(url, params=request_params)
    if res.status_code != 200:
        raise Exception(res.content)
    
    data = json.load(open('../data/data.json'))
    data.setdefault(pull_request_number, {})
    data[pull_request_number] = res.json()
    json.dump(data, open('data.json', 'w+'), indent=4, default=str)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", help="GitHub owner/repo combination", type=str)
    parser.add_argument("pull_request_number", help="Number of the Pull Request in the specified owner/repo", type=str)
    args = parser.parse_args()
    main(args)