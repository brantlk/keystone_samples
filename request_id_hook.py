# This sample shows how to set a hook on the session to get the request ID.
# Requires: keystoneauth1, python-keystoneclient, requests


import argparse

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
import requests


def log_request(r, *args, **kwargs):
    request_id = r.headers.get('x-openstack-request-id')
    print('%s %s %s' % (r.status_code, r.url, request_id))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth-url', default='http://localhost/identity')
    parser.add_argument('--password')
    args = parser.parse_args()

    requests_session = requests.Session()
    requests_session.hooks = {'response': log_request}

    auth = v3.Password(auth_url='%s/v3' % args.auth_url,
                       username='admin',
                       password=args.password,
                       project_name='admin',
                       user_domain_name='Default',
                       project_domain_name='Default')
    ksa_session = session.Session(auth=auth, session=requests_session)
    ks = client.Client(session=ksa_session)
    ks.users.list()


main()
