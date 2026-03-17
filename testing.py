# -*- coding: utf-8 -*-
"""
testing.py — Vobiz SDK end-to-end sanity test

Reads credentials from .env and exercises every major resource.
Run:
    python testing.py
"""

import os
import sys
import traceback

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))
import vobiz


# ── helpers ────────────────────────────────────────────────────────────────────

PASS  = "[PASS]"
FAIL  = "[FAIL]"
SKIP  = "[SKIP]"
SEP   = "─" * 60

results = []   # (label, status, detail)


def section(title):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)


def run(label, fn):
    try:
        result = fn()
        detail = repr(result)[:120] if result is not None else "(no content)"
        print(f"  {PASS}  {label}")
        print(f"         {detail}")
        results.append((label, "PASS", ""))
        return result
    except Exception as e:
        msg = str(e)
        print(f"  {FAIL}  {label}")
        print(f"         {msg}")
        results.append((label, "FAIL", msg))
        return None


def skip(label, reason):
    print(f"  {SKIP}  {label}  ({reason})")
    results.append((label, "SKIP", reason))


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'═'*60}")
    print("  Vobiz SDK — End-to-End Test")
    print(f"{'═'*60}")

    auth_id    = os.environ.get("VOBIZ_AUTH_ID")
    auth_token = os.environ.get("VOBIZ_AUTH_TOKEN")

    if not auth_id or not auth_token:
        print("\n  ERROR: VOBIZ_AUTH_ID / VOBIZ_AUTH_TOKEN not set in .env")
        sys.exit(1)

    print(f"\n  Auth ID   : {auth_id}")
    print(f"  Auth Token: {'*' * 8}{auth_token[-6:]}")

    client = vobiz.RestClient(auth_id=auth_id, auth_token=auth_token)

    # ── 1. Account ──────────────────────────────────────────────────────────────
    section("1. Account")
    run("GET  /auth/me",              lambda: client.accounts.get())
    run("GET  get_balance(INR)",      lambda: client.accounts.get_balance(auth_id, "INR"))
    run("GET  get_transactions()",    lambda: client.accounts.get_transactions(auth_id, limit=5, offset=0))
    run("GET  get_concurrency()",     lambda: client.accounts.get_concurrency(auth_id))

    # ── 2. Calls ────────────────────────────────────────────────────────────────
    section("2. Calls")
    run("GET  list_live()",     lambda: client.calls.list_live())
    run("GET  list_queued()",   lambda: client.calls.list_queued())

    # ── 3. Applications ─────────────────────────────────────────────────────────
    section("3. Applications")
    app_result = run("POST create application",
        lambda: client.applications.create(
            name="SDK-Test-App",
            answer_url="https://example.com/answer",
            hangup_url="https://example.com/hangup",
            application_type="XML",
        )
    )

    app_id = None
    if app_result is not None:
        app_id = getattr(app_result, "app_id", None) or getattr(app_result, "id", None)

    run("GET  list applications", lambda: client.applications.list())

    if app_id:
        run(f"GET  get application {app_id}",
            lambda: client.applications.get(app_id))
        run(f"PUT  update application {app_id}",
            lambda: client.applications.update(app_id, name="SDK-Test-App-Updated"))
        run(f"DEL  delete application {app_id}",
            lambda: client.applications.delete(app_id))
    else:
        skip("GET/PUT/DEL application by id", "create did not return app_id")

    # ── 4. Phone Numbers (inventory) ────────────────────────────────────────────
    section("4. Phone Numbers")
    run("GET  list_inventory(IN)",
        lambda: client.phone_numbers.list_inventory(country="IN", page=1, per_page=10))

    # ── 5. SIP Endpoints ────────────────────────────────────────────────────────
    section("5. SIP Endpoints")
    ep_result = run("POST create endpoint",
        lambda: client.endpoints.create(
            username="sdktestuser",
            password="TestPass@123",
            alias="SDK Test User",
        )
    )

    ep_id = None
    if ep_result is not None:
        ep_id = (getattr(ep_result, "endpoint_id", None)
                 or getattr(ep_result, "id", None))

    run("GET  list endpoints", lambda: client.endpoints.list())

    if ep_id:
        run(f"GET  get endpoint {ep_id}",
            lambda: client.endpoints.get(ep_id))
        run(f"POST update endpoint {ep_id}",
            lambda: client.endpoints.update(ep_id, alias="SDK Test User Updated"))
        run(f"DEL  delete endpoint {ep_id}",
            lambda: client.endpoints.delete(ep_id))
    else:
        skip("GET/POST/DEL endpoint by id", "create did not return endpoint_id")

    # ── 6. SIP Trunks ───────────────────────────────────────────────────────────
    section("6. SIP Trunks")
    trunks_result = run("GET  list sip_trunks", lambda: client.sip_trunks.list())

    trunk_id = None
    if trunks_result is not None:
        objs = getattr(trunks_result, "objects", None) or (
            list(trunks_result) if hasattr(trunks_result, "__iter__") else []
        )
        if objs:
            trunk_id = getattr(objs[0], "id", None) or getattr(objs[0], "trunk_id", None)

    if trunk_id:
        run(f"GET  get trunk {trunk_id}",
            lambda: client.sip_trunks.get(trunk_id))
    else:
        skip("GET trunk by id", "no trunks found or list failed")

    # ── 7. Credentials ──────────────────────────────────────────────────────────
    section("7. Credentials")
    run("GET  list credentials", lambda: client.credentials.list())

    # ── 8. IP ACLs ──────────────────────────────────────────────────────────────
    section("8. IP Access Control Lists")
    acl_result = run("POST create ip-acl",
        lambda: client.ip_access_control_lists.create(
            ip_address="8.8.8.8",
            description="SDK test ACL",
        )
    )

    acl_id = None
    if acl_result is not None:
        acl_id = getattr(acl_result, "id", None) or getattr(acl_result, "acl_id", None)

    run("GET  list ip-acls", lambda: client.ip_access_control_lists.list())

    if acl_id:
        # Note: single-item GET not supported by Vobiz API for ip-acl
        run(f"DEL  delete acl {acl_id}",
            lambda: client.ip_access_control_lists.delete(acl_id))
    else:
        skip("DEL ip-acl by id", "create did not return id")

    # ── 9. Origination URIs ─────────────────────────────────────────────────────
    section("9. Origination URIs")
    run("GET  list origination_uris",
        lambda: client.origination_uris.list())

    # ── 10. Recordings ──────────────────────────────────────────────────────────
    section("10. Recordings")
    run("GET  list recordings", lambda: client.recordings.list())

    # ── 11. CDRs ────────────────────────────────────────────────────────────────
    section("11. CDRs")
    run("GET  list cdrs", lambda: client.cdrs.list())

    # ── Summary ─────────────────────────────────────────────────────────────────
    print(f"\n{'═'*60}")
    print("  Summary")
    print(f"{'═'*60}")

    passed = sum(1 for _, s, _ in results if s == "PASS")
    failed = sum(1 for _, s, _ in results if s == "FAIL")
    skipped = sum(1 for _, s, _ in results if s == "SKIP")

    print(f"\n  Total : {len(results)}")
    print(f"  Pass  : {passed}")
    print(f"  Fail  : {failed}")
    print(f"  Skip  : {skipped}")

    if failed:
        print(f"\n  Failed tests:")
        for label, status, detail in results:
            if status == "FAIL":
                print(f"    - {label}: {detail}")

    print()
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
