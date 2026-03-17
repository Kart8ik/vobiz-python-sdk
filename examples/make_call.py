# -*- coding: utf-8 -*-
"""
examples/make_call.py — Vobiz Live Call Demo

Triggers a real outbound call using the Vobiz Python SDK.
Reads credentials and phone numbers from .env.

Prerequisites:
    1. pip install -r requirements.txt
    2. Start examples/server.py
    3. Start ngrok: ngrok http 5000
    4. Update .env: ANSWER_URL=https://<ngrok-id>.ngrok.io/answer
    5. Run: python examples/make_call.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
import vobiz

load_dotenv()

FROM_NUMBER = os.environ.get('FROM_PHONE_NUMBER')
TO_NUMBER   = os.environ.get('TO_PHONE_NUMBER')
ANSWER_URL  = os.environ.get('ANSWER_URL')

HANGUP_URL  = ANSWER_URL.replace('/answer', '/hangup') if ANSWER_URL else None


def sep(title=''):
    print(f"\n{'='*60}")
    if title:
        print(f"  {title}")
        print(f"{'='*60}")


def ok(label, value=''):
    print(f"  [OK] {label}: {value}" if value else f"  [OK] {label}")


def fail(label, err):
    print(f"  [FAIL] {label}: {err}")


def main():
    sep('Vobiz Live Call Demo')

    # Validate env
    missing = [k for k, v in {
        'FROM_PHONE_NUMBER': FROM_NUMBER,
        'TO_PHONE_NUMBER': TO_NUMBER,
        'ANSWER_URL': ANSWER_URL,
    }.items() if not v]

    if missing:
        print(f"\n  Missing required .env variables: {', '.join(missing)}")
        print(f"  Please update your .env file and re-run.\n")
        sys.exit(1)

    if '<your-ngrok-id>' in ANSWER_URL:
        print(f"\n  ANSWER_URL still contains placeholder: {ANSWER_URL}")
        print(f"  Please start ngrok and update ANSWER_URL in .env\n")
        sys.exit(1)

    print(f"\n  From       : {FROM_NUMBER}")
    print(f"  To         : {TO_NUMBER}")
    print(f"  Answer URL : {ANSWER_URL}")
    print(f"  Hangup URL : {HANGUP_URL}")

    # Create client (reads VOBIZ_AUTH_ID + VOBIZ_AUTH_TOKEN from .env)
    client = vobiz.RestClient()
    ok('Client created', f"Auth ID: {client.auth_id}")

    # -----------------------------------------------------------
    # Step 1: Create the call
    # -----------------------------------------------------------
    sep('Step 1: Create Call')
    call_uuid = None
    try:
        resp = client.calls.create(
            from_=FROM_NUMBER,
            to_=TO_NUMBER,
            answer_url=ANSWER_URL,
            answer_method='GET',
            hangup_url=HANGUP_URL,
            hangup_method='GET',
        )
        call_uuid = getattr(resp, 'request_uuid', None) or getattr(resp, 'call_uuid', None)
        ok('Call created', str(resp))
        print(f"  Call UUID  : {call_uuid}")
    except Exception as e:
        fail('Create call', e)
        sys.exit(1)

    # -----------------------------------------------------------
    # Step 2: List live calls (call should appear here briefly)
    # -----------------------------------------------------------
    sep('Step 2: List Live Calls')
    try:
        live = client.calls.list_live()
        ok('List live calls', str(live))
    except Exception as e:
        fail('List live calls', e)

    # -----------------------------------------------------------
    # Step 3: List queued calls
    # -----------------------------------------------------------
    sep('Step 3: List Queued Calls')
    try:
        queued = client.calls.list_queued()
        ok('List queued calls', str(queued))
    except Exception as e:
        fail('List queued calls', e)

    # -----------------------------------------------------------
    # Step 4: Send DTMF digits (after a short wait for the call to connect)
    # -----------------------------------------------------------
    sep('Step 4: Send DTMF Digits')
    if call_uuid:
        print('  Waiting 5 seconds for call to connect...')
        time.sleep(5)
        try:
            dtmf_resp = client.calls.send_digits(call_uuid, digits='1', leg='aleg')
            ok('Send DTMF', str(dtmf_resp))
        except Exception as e:
            fail('Send DTMF', e)

    # -----------------------------------------------------------
    # Step 7: Hangup
    # -----------------------------------------------------------
    sep('Step 5: Hangup Call')
    if call_uuid:
        print('  Waiting 3 more seconds before hangup...')
        time.sleep(3)
        try:
            client.calls.hangup(call_uuid)
            ok('Call hung up', call_uuid)
        except Exception as e:
            fail('Hangup', e)

    sep('Done')
    print('  Live call demo complete.\n')


if __name__ == '__main__':
    main()
