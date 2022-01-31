import argparse
import json
import requests

DEFAULT_DATA_FILE_PATH = '.github/data/pull_requests.json'
JS_FILE_PATH = '.github/js/data_url.js'


def write_js_variable(path):
    import os; print(os.getcwd())
    js_content = "<script>const DATA_URL = '%(path)s'</script>" % path
    open(JS_FILE_PATH, 'w+').write(js_content)
    return


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

    data = json.loads(open(args.data_file_path, 'w+').read() or '{}')
    data.setdefault(pull_request_number, {})
    data[pull_request_number] = res.json()
    json.dump(data, open(args.data_file_path, 'w+'), indent=4, default=str)
    write_js_variable({"path": args.data_file_path})
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", help="GitHub owner/repo combination", type=str)
    parser.add_argument("pull_request_number", help="Number of the Pull Request in the specified owner/repo", type=str)
    parser.add_argument('-d', '--data_file_path', help="File Path to output the Pull Requests to", type=str, default=DEFAULT_DATA_FILE_PATH)
    args = parser.parse_args()
    main(args)
