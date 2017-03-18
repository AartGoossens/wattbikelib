import json

import vcr

from params import (OVERWRITE_EXISTING_CASSETTES, RECORD_CASSETTES,
                    USE_CASSETTES)

BODY_REPLACEMENTS = (
    # (('nested...', 'dict...', 'keys...'), 'replacement'),
    (('username',), 'USERNAME'),
    (('password',), 'PASSWORD'),
    (('vanityName',), 'VANITY_NAME'),
    (('displayName',), 'DISPLAY_NAME'),
    (('firstName',), 'FIRST_NAME'),
    (('lastName',), 'LAST_NAME'),
    (('birthDate', 'iso',), 'BIRTH_DATE'),
    (('email',), 'arnold@extremelyfit.com'),
    (('sessionToken',), 'r:abbcdefghikjlmnopqrstuvwxyz012345'),
    (('authData', 'strava', 'id',), 'STRAVA_ID'),
    (('authData', 'strava', 'access_token',), 'STRAVA_ACCESS_TOKEN'))


def replace_single(body, replacement):
    if not isinstance(body, dict):
        return replacement[1]
    elif not replacement[0][0] in body.keys():
        return body
    else:
        body[replacement[0][0]] = replace_single(
            body=body[replacement[0][0]],
            replacement=(replacement[0][1:], replacement[1]))
        return body


def replace_nested_dict(body, replacements):
    for rep in replacements:
        body = replace_single(body, rep)
    return body


def body_scrub(body):
    if not body:
        return body

    try:
        body_dict = json.loads(body)
    except json.decoder.JSONDecodeError:
        return body

    body_dict = replace_nested_dict(
        body_dict, BODY_REPLACEMENTS)

    return json.dumps(body_dict).encode()


def scrub_response(response):
    response['body']['string'] = body_scrub(response['body']['string'])
    return response


def scrub_request(request):
    if not USE_CASSETTES:
        return None
    request.body = body_scrub(request.body)
    return request


def determine_record_mode():
    if not RECORD_CASSETTES:
        return 'none'
    elif OVERWRITE_EXISTING_CASSETTES:
        return 'all'
    else:
        return 'once'


custom_vcr = vcr.VCR(
    before_record_request=scrub_request,
    before_record_response=scrub_response,
    decode_compressed_response=True,
    cassette_library_dir='fixtures/vcr_cassettes',
    record_mode=determine_record_mode(),
    filter_headers=[('_SessionToken', 'SESSION_TOKEN')])
