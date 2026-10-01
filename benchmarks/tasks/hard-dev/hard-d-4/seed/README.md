# webhook_auth

Verifies an inbound webhook's signature before the rest of the service
trusts its payload.

```python
from webhook_auth import verify_webhook

verify_webhook(raw_body_bytes, request_headers, shared_secret)
# -> True, or raises webhook_auth.WebhookVerificationError
```

`headers` is a plain `dict` with the exact keys `"X-Signature"` (of the form
`"sha256=<hex hmac>"`) and `"X-Timestamp"` (seconds since the epoch, as a
string).

Run the visible tests: `python -m unittest discover -s tests`
