## Vobiz Python SDK

The **Vobiz Python SDK** makes it simple to integrate Vobiz voice and call-control
features into your Python applications. It provides a thin, well-typed wrapper
around the Vobiz REST API endpoints and XML response format.

### Installation

Install from your local clone:

```bash
pip install -e .
```

### Authentication

Vobiz uses account-scoped authentication via headers:

- `X-Auth-ID` – your account ID
- `X-Auth-Token` – your account token

The SDK reads these from the environment when possible:

- `VOBIZ_AUTH_ID`
- `VOBIZ_AUTH_TOKEN`

Example:

```python
import vobiz

client = vobiz.RestClient()  # uses VOBIZ_AUTH_ID / VOBIZ_AUTH_TOKEN
```

Or pass them explicitly:

```python
import vobiz

client = vobiz.RestClient(auth_id="MA_xxx", auth_token="xxx")
```

### Core resources

The main entrypoint is `vobiz.RestClient`, which exposes resources that closely
mirror the Vobiz API:

- `client.calls` – call creation, transfer, DTMF, live/queued listing
- `client.accounts` – account info, balance, concurrency, transactions
- `client.subaccounts` – sub-account management
- `client.applications` – inbound call applications
- `client.phone_numbers` – inventory, purchase, release, trunk assignment
- `client.endpoints` – SIP endpoints
- `client.sip_trunks` – SIP trunks
- `client.credentials` – SIP credentials
- `client.ip_access_control_lists` – IP ACLs
- `client.origination_uris` – origination URIs

Each resource has simple methods like `create`, `get`, `list`, `update`,
and `delete` (where applicable), which are tested to hit the exact URLs and
methods defined in the Vobiz endpoint PDFs.

### Vobiz XML

For building XML responses used in call control, import:

```python
from vobiz import vobizxml
```

### Testing locally

Install test dependencies and run:

```bash
pip install -r requirements.txt
pytest -q
```

The tests assert request construction (method, URL, headers, query string, and
JSON body) for all implemented resources, and validate XML output.

