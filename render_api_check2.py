import json
import urllib.request
import urllib.error

TOKEN = 'rnd_aRgBV2BdGIcfhMN5JDN2IiRMIYSH'
headers = {'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/json'}
urls = ['https://api.render.com/v1/owners', 'https://api.render.com/v1/services?limit=20']
for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
        print('URL', url)
        if isinstance(data, list):
            print('LENGTH', len(data))
            for item in data[:5]:
                print({k: v for k, v in item.items() if k in ('id', 'name', 'slug', 'type', 'ownerId')})
        else:
            print('OBJECT KEYS', list(data.keys()))
            if 'services' in data:
                print('services count', len(data['services']))
                for item in data['services'][:5]:
                    print({k: v for k, v in item.items() if k in ('id', 'name', 'slug', 'type', 'ownerId')})
            else:
                print(data)
    except urllib.error.HTTPError as e:
        print('URL', url, 'HTTP', e.code, e.reason)
        try:
            print(e.read().decode('utf-8'))
        except Exception:
            pass
    except Exception as e:
        print('URL', url, 'ERROR', e)
