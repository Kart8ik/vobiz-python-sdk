import os

import vobiz


def main() -> None:
    # Use explicit credentials or rely on VOBIZ_AUTH_ID / VOBIZ_AUTH_TOKEN
    client = vobiz.RestClient(
        auth_id=os.environ.get("VOBIZ_AUTH_ID", "MA_TEST"),
        auth_token=os.environ.get("VOBIZ_AUTH_TOKEN", "TOKEN"),
    )

    # Calls
    call = client.calls.create(
        from_="911171366943",
        to_="917348860185",
        answer_url="https://example.com/answer.xml",
    )
    print("Created call:", getattr(call, "__dict__", call))

    live = client.calls.list_live()
    print("Live calls:", getattr(live, "__dict__", live))

    queued = client.calls.list_queued()
    print("Queued calls:", getattr(queued, "__dict__", queued))

    # Accounts
    me = client.accounts.get()
    print("Account:", getattr(me, "__dict__", me))

    # Applications
    app = client.applications.create(
        name="My App",
        answer_url="https://example.com/answer.xml",
    )
    print("Application:", getattr(app, "__dict__", app))

    # Phone numbers
    numbers = client.phone_numbers.search(country="US", type="local", pattern="415")
    print("Search numbers:", getattr(numbers, "__dict__", numbers))

    # Endpoints
    endpoint = client.endpoints.create(
        username="user1",
        password="secret",
        alias="Desk Phone",
    )
    print("Endpoint:", getattr(endpoint, "__dict__", endpoint))

    # SIP trunks
    trunk = client.sip_trunks.create(
        name="Main Trunk",
        inbound_uri="sip:inbound@example.com",
        outbound_uri="sip:outbound@example.com",
    )
    print("SIP trunk:", getattr(trunk, "__dict__", trunk))

    # Credentials
    cred = client.credentials.create(
        username="trunk-user",
        password="trunk-pass",
        trunk_id=getattr(trunk, "id", None),
    )
    print("Credential:", getattr(cred, "__dict__", cred))

    # IP Access Control Lists
    acl = client.ip_access_control_lists.create(
        name="Office IPs",
        description="Corporate offices",
        ip_addresses=["203.0.113.1/32"],
    )
    print("IP ACL:", getattr(acl, "__dict__", acl))

    # Origination URIs
    uri = client.origination_uris.create(
        uri="sip:carrier@example.com",
        trunk_id=getattr(trunk, "id", None),
        weight=10,
        priority=1,
    )
    print("Origination URI:", getattr(uri, "__dict__", uri))


if __name__ == "__main__":
    main()