import os

import vobiz


def main() -> None:
    # Use explicit credentials or rely on VOBIZ_AUTH_ID / VOBIZ_AUTH_TOKEN
    client = vobiz.RestClient(
        auth_id=os.environ.get("VOBIZ_AUTH_ID", "MA_TEST"),
        auth_token=os.environ.get("VOBIZ_AUTH_TOKEN", "TOKEN"),
    )

    # # Calls
    # call = client.calls.create(
    #     from_="911171366943",
    #     to_="917348860185",
    #     answer_url="https://example.com/answer.xml",
    # )
    # print("Created call:", getattr(call, "__dict__", call))

    live = client.calls.list_live()
    print("Live calls:", getattr(live, "__dict__", live))

    queued = client.calls.list_queued()
    print("Queued calls:", getattr(queued, "__dict__", queued))

    # Accounts
    me = client.accounts.get()
    print("Account:", getattr(me, "__dict__", me))

    # Applications
    # app = client.applications.create(
    #     name="My App",
    #     answer_url="https://example.com/answer.xml",
    # )
    # print("Application:", getattr(app, "__dict__", app))

    # Phone numbers - inventory and purchase example
    inventory = client.phone_numbers.list_inventory(country="IN", page=1, per_page=25)
    print("Inventory numbers:", getattr(inventory, "__dict__", inventory))

    # Endpoints
    endpoints = client.endpoints.list()
    print("Endpoints:", getattr(endpoints, "__dict__", endpoints))

    # SIP trunks - retrieve all
    trunks = client.sip_trunks.list()
    print("All SIP trunks:", getattr(trunks, "__dict__", trunks))

    # Credentials - retrieve all
    all_creds = client.credentials.list()
    print("All Credentials:", getattr(all_creds, "__dict__", all_creds))

    # IP Access Control Lists
    # IP Access Control Lists - retrieve all
    all_acls = client.ip_access_control_lists.list()
    print("All IP ACLs:", getattr(all_acls, "__dict__", all_acls))

    # Origination URIs - retrieve all (requires trunk_id)
    # Here we're using the first trunk from previously retrieved trunks, if any
    trunk_id = "f34cc125-7e76-4e6e-bd35-e0dda3a1b19f"
    # if hasattr(trunks, "__iter__") and len(trunks) > 0:
    #     trunk_id = getattr(trunks[0], "id", None)
    # elif hasattr(trunks, "objects") and hasattr(trunks.objects, "__iter__") and len(trunks.objects) > 0:
    #     trunk_id = getattr(trunks.objects[0], "id", None)
    # # Only perform the origination_uris.list() if we have a trunk_id
    if trunk_id:
        all_uris = client.origination_uris.list(trunk_id=trunk_id)
        print("All origination URIs for trunk:", getattr(all_uris, "__dict__", all_uris))
    else:
        print("No trunk_id found, cannot list origination URIs.")


if __name__ == "__main__":
    main()