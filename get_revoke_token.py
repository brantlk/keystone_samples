# Get a token and then revoke it. Use this to get some revocation events!

import argparse
import json

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://localhost/identity')
    parser.add_argument('--password', required=True)
    args = parser.parse_args()

    payload = {
        'auth': {
            'identity': {
                'methods': ['password'],
                'password': {
                    'user': {
                        'name': 'admin',
                        'domain': {'name': 'Default'},
                        'password': args.password
                    }
                }
            },
            'scope': {
                'project': {
                    'name': 'demo',
                    'domain': {'name': 'Default'}
                }
            }
        }
    }

    r = requests.post(
        '%s/v3/auth/tokens' % args.url,
        headers={'Content-Type': 'application/json'},
        data=json.dumps(payload))
    r.raise_for_status()

    token = r.headers['X-Subject-Token']

    print("Token: %s" % token)

    r = requests.delete(
        '%s/v3/auth/tokens' % args.url,
        headers={'X-Auth-Token': token, 'X-Subject-Token': token}
    )
    r.raise_for_status()

    print("Token revoked.")


main()
