# Get a token and then revoke it. Use this to get some revocation events!

import argparse
import datetime
import json

import requests


def get_token(args):
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

    while True:

        start = datetime.datetime.utcnow()
        r = requests.post(
            '%s/v3/auth/tokens' % args.url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload))
        r.raise_for_status()
        end = datetime.datetime.utcnow()

        token = r.headers['X-Subject-Token']

        print("Token in %s: %s" % (end - start, token))
        return token


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

    while True:

        token = get_token(args)

        revoke_start = datetime.datetime.utcnow()
        r = requests.delete(
            '%s/v3/auth/tokens' % args.url,
            headers={'X-Auth-Token': token, 'X-Subject-Token': token}
        )
        r.raise_for_status()
        end = datetime.datetime.utcnow()

        print("Token revoked in %s." % (end - revoke_start))


main()
