# List compounds

`GET /v0/compounds`

> **Authentication:** every request must send `X-ConfidentLims-APIKey`, `X-ConfidentLims-Timestamp` (unix seconds) and `X-ConfidentLims-Signature`, an HMAC-SHA256 signature of the request. The examples below call `sign_request()` from the [Request Signing guide](https://api.confidentcannabis.com/v0/docs/request-signing.md) — read it first. Request bodies are form-encoded, never JSON.

Return every compound known to Confident, including synonyms and alternate spellings. Results are grouped by test category and sorted by name within each category.

Anything listed here can be submitted in test results using the `name` value. When `is_synonym` is true, `synonym_for_compound_name` gives the canonical compound the synonym maps to.

This response is cacheable and is served with a `Cache-Control: max-age=1800` header.

## Parameters

No parameters.

## Responses

### 200 Success

Fields (alongside the `success: true` envelope flag):

- `compounds` (array of objects)
  - `category` (string) — Test category under which this compound is normally tested
  - `name` (string) — Unique name used to identify the compound
  - `display_name` (string) — Display name for compound
  - `is_synonym` (boolean) — True if this is a synonym for another compound
  - `synonym_for_compound_name` (string) — Name of compound for which this is a synonym

Example:

```json
{
  "success": true,
  "compounds": [
    {
      "category": "cannabinoids",
      "name": "cbd",
      "display_name": "CBD",
      "is_synonym": false,
      "synonym_for_compound_name": ""
    },
    {
      "category": "cannabinoids",
      "name": "cannabidiol",
      "display_name": "Cannabidiol",
      "is_synonym": true,
      "synonym_for_compound_name": "cbd"
    }
  ]
}
```

### 400 Bad request

The request was malformed or failed validation. Validation failures include per-field messages in `error_details`. Possible `error_code` values: `invalid_request`, `request_too_old`.

### 401 Unauthorized

Authentication failed. Possible `error_code` values: `missing_api_key`, `invalid_api_key`, `invalid_credentials_type`, `api_access_restricted`, `api_access_denied`, `missing_signature`, `missing_timestamp`, `invalid_timestamp`, `invalid_signature`.

### 403 Permission denied

The API key is valid but does not have permission for this endpoint (for example, a client key calling a labs endpoint). Possible `error_code` values: `permission_denied`.

## Examples

### cURL

```bash
# X-ConfidentLims-Signature: see the Request Signing guide - https://api.confidentcannabis.com/v0/docs/request-signing.md
curl -X GET 'https://api.confidentcannabis.com/v0/compounds' \
  -H 'X-ConfidentLims-APIKey: YOUR_API_KEY' \
  -H 'X-ConfidentLims-Timestamp: UNIX_TIMESTAMP' \
  -H 'X-ConfidentLims-Signature: REQUEST_SIGNATURE'
```

### Python

```python
import time
import requests

# sign_request() is defined in the Request Signing guide:
# https://api.confidentcannabis.com/v0/docs/request-signing.md
from sign_request import sign_request

API_KEY = 'YOUR_API_KEY'
API_SECRET = 'YOUR_API_SECRET'
path = '/v0/compounds'

headers = {'X-ConfidentLims-Timestamp': str(int(time.time()))}
headers['X-ConfidentLims-Signature'] = sign_request(
    'GET', path, headers, {}, API_KEY, API_SECRET)
headers['X-ConfidentLims-APIKey'] = API_KEY

response = requests.get(
    'https://api.confidentcannabis.com' + path,
    headers=headers,
)
print(response.json())
```

### JavaScript

```javascript
// signRequest() is defined in the Request Signing guide:
// https://api.confidentcannabis.com/v0/docs/request-signing.md
import { signRequest } from './sign_request.js';

const API_KEY = 'YOUR_API_KEY';
const API_SECRET = 'YOUR_API_SECRET';
const path = "/v0/compounds";

const headers = { 'X-ConfidentLims-Timestamp': String(Math.floor(Date.now() / 1000)) };
headers['X-ConfidentLims-Signature'] = signRequest(
  "GET", path, headers, {}, API_KEY, API_SECRET);
headers['X-ConfidentLims-APIKey'] = API_KEY;

const response = await fetch("https://api.confidentcannabis.com" + path, {
  headers,
});
console.log(await response.json());
```

---

HTML version: https://api.confidentcannabis.com/v0/docs/get-compound  
OpenAPI spec for this section: https://api.confidentcannabis.com/v0/docs/openapi.json  
Request Signing guide: https://api.confidentcannabis.com/v0/docs/request-signing.md
