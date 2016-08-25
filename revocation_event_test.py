# Get a token and then revoke it. Use this to get some revocation events!

import argparse
import datetime
import json
import uuid

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
                    'name': args.project,
                    'domain': {'name': 'Default'}
                }
            }
        }
    }

    start = datetime.datetime.utcnow()
    r = requests.post(
        '%s/v3/auth/tokens' % args.url,
        verify=not args.insecure,
        headers={'Content-Type': 'application/json'},
        data=json.dumps(payload))
    r.raise_for_status()
    end = datetime.datetime.utcnow()

    token = r.headers['X-Subject-Token']

    print("Token in %s: %s" % (end - start, token))
    return token


def validate_token(args, token):
    start = datetime.datetime.utcnow()
    r = requests.get(
        '%s/v3/auth/tokens' % args.url,
        verify=not args.insecure,
        headers={'X-Auth-Token': token, 'X-Subject-Token': token}
    )
    r.raise_for_status()
    end = datetime.datetime.utcnow()

    print("Token validated in %s." % (end - start))


def delete_token(args, token):
    revoke_start = datetime.datetime.utcnow()
    r = requests.delete(
        '%s/v3/auth/tokens' % args.url,
        verify=not args.insecure,
        headers={'X-Auth-Token': token, 'X-Subject-Token': token}
    )
    r.raise_for_status()
    end = datetime.datetime.utcnow()

    print("Token revoked in %s." % (end - revoke_start))


def create_delete_user(args):
    token = get_token(args)
    payload = {
        'user': {
            'name': uuid.uuid4().hex,
            'password': uuid.uuid4().hex,
        }
    }
    r = requests.post(
        '%s/v3/users' % args.url,
        verify=not args.insecure,
        headers={'Content-Type': 'application/json', 'X-Auth-Token': token},
        data=json.dumps(payload))
    r.raise_for_status()

    user_id = r.json()['user']['id']
    print("Created user %s" % user_id)

    requests.get('%s/v3/users/%s' % (args.url, user_id),
                 verify=not args.insecure,
                 headers={'X-Auth-Token': token})
    r.raise_for_status()

    requests.delete('%s/v3/users/%s' % (args.url, user_id),
                    verify=not args.insecure,
                    headers={'X-Auth-Token': token})
    r.raise_for_status()
    print("Deleted user %s" % user_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://localhost/identity')
    parser.add_argument('--password', required=True)
    parser.add_argument('--project', default='admin')
    parser.add_argument('--insecure', default=False, action='store_const',
                        const=True)
    args = parser.parse_args()

    while True:
        token = get_token(args)
        for i in range(5):
            validate_token(args, token)
            validate_token(args, token)
        # delete_token(args, token)

        create_delete_user(args)


main()
