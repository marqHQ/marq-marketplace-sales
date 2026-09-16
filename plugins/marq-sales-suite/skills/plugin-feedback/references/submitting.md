# Submitting to the contribution pipeline

The pipeline has two intake lanes. Agents use the JSON webhook. The hosted form is for a human with no terminal, and both lanes converge on identical downstream logic.

- Endpoint: `https://marqapp.app.n8n.cloud/webhook/sales-plugin-submit`
- Method: `POST`, `application/json`, no authentication
- Form fallback: `https://marqapp.app.n8n.cloud/form/sales-plugin-contribute`

## Payload

```json
{
  "submission_type": "New skill proposal",
  "submitter_name": "Rep Name",
  "submitter_email": "rep@marq.com",
  "skill": "skill-name",
  "summary": "One line, short enough for a Slack message",
  "privacy_confirmation": true,
  "submission": "the bundle or feedback record, unchanged"
}
```

- `submission_type` is `New skill proposal` or `Feedback about an existing skill`, spelled exactly.
- `submitter_email` must be the rep's real Marq address. It is the only channel the pipeline has back to them; a wrong address means they never learn the outcome.
- `skill` is the proposed skill name, or the existing skill's folder name for feedback.
- `privacy_confirmation` records that the rep attested the submission is clean. Set it only after they actually said so.

## Posting it

Write the payload to a UTF-8 file and post the file. Never build the JSON on a command line: bundles contain newlines, quotes, `$`, and backticks, and every shell mangles at least one of them. Serialize with a real JSON writer so the bundle is escaped correctly.

```
curl -sS -X POST "https://marqapp.app.n8n.cloud/webhook/sales-plugin-submit" -H "Content-Type: application/json" -d @payload.json -w '\nHTTP %{http_code}\n'
```

macOS and Linux use `curl`. Windows uses `curl.exe`. The arguments are identical; only the executable name differs, because in Windows PowerShell 5.1 the bare word `curl` is an alias for `Invoke-WebRequest` and rejects these arguments. Keep the command on one line so no shell-specific continuation character is needed.

A successful post returns `HTTP 200` and:

```json
{"status":"accepted","note":"Watch Slack for the tracking DM."}
```

## Confirming it landed

`HTTP 200` means the pipeline accepted the request, not that the submission passed. The real receipt is the Slack DM, which arrives within about a minute, echoes the parsed submission type, skill, and summary, and carries a `sub_...` reference plus the tracking thread. If those echoed values look wrong, say so rather than treating `HTTP 200` as success.

The pipeline validates the bundle itself and DMs the rep a rejection without filing anything public when the frontmatter is missing or malformed, `kind` is not `skill-proposal`, `skill_name` is absent, there is no `SKILL.md` file block, the bundle exceeds 60,000 characters, or a credential pattern matches. Feedback records under 40 characters are rejected the same way. Getting the bundle right before posting is what avoids that round trip.

## Stopping conditions

Stop and hand the rep the form link with the field values when any of these is true:

- No curl on the machine, or no network path to `marqapp.app.n8n.cloud`
- The POST returns a non-2xx status twice in a row
- The rep has not confirmed the exact bundle text

Do not retry a POST that returned `HTTP 200`. The pipeline is not idempotent; a second identical POST files a second submission.

## Do not post to the form endpoint

`/form/sales-plugin-contribute` is an n8n Form Trigger. Its wire contract is UI implementation detail: positional `field-0`…`field-6` keys, `multipart/form-data` only, a JSON-array-encoded checkbox, and a bot filter that answers `HTTP 401` with a `WWW-Authenticate: Basic` header. Worst of all, sending semantic field names there returns `HTTP 200` while every field arrives empty, so a broken submission looks like a successful one. The webhook exists so no agent has to care about any of that.
