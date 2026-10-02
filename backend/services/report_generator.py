"""Builds a plain-text/Markdown evidence pack the user can give to a bank or police."""
from datetime import datetime, timezone
from ml.preprocessing import redact


def generate_report(incident: dict, plan: dict, scan: dict | None) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = [f"# Scam incident summary", f"Generated: {now}", ""]

    L.append("## What happened")
    if incident.get("notes"):
        L.append(redact(incident["notes"]))
    yes = [k.replace("_", " ") for k in ("clicked_link", "entered_password", "entered_otp", "entered_card_details",
           "shared_id_documents", "downloaded_file", "installed_app", "gave_remote_access", "sent_money") if incident.get(k)]
    L.append("Actions taken by victim: " + (", ".join(yes) if yes else "none reported"))
    if incident.get("incident_time"):
        L.append(f"Approximate time of incident: {incident['incident_time']}")
    L.append("")

    if incident.get("sent_money"):
        L += ["## Financial loss",
              f"- Amount: {incident.get('amount', 'unknown')} {incident.get('currency', '')}".rstrip(),
              f"- Payment method: {incident.get('payment_method', 'unknown')}",
              f"- Transaction ID / reference: {incident.get('transaction_id', '(add from your receipt)')}",
              f"- Recipient account / UPI ID / wallet: {incident.get('recipient', '(add)')}", ""]

    L.append("## Scammer details")
    L.append(f"- Contact (phone / handle / link): {incident.get('scammer_contact', '(add)')}")
    if scan:
        L += [f"- Automated analysis: {scan.get('verdict')} (risk {scan.get('score')}/100, confidence {scan.get('confidence')})"]
        L += [f"  - {r}" for r in scan.get("reasons", [])[:6]]
    L.append("")

    L.append("## Exposure assessed")
    L += [f"- [{e['severity'].upper()}] {e['item']}: {e['why']}" for e in plan["exposures"]]
    L.append("")

    L.append("## Steps to complete")
    for title, key in (("Now", "do_now"), ("Within 24 hours", "within_24h"), ("This week", "this_week")):
        L.append(f"### {title}")
        L += [f"- [ ] {s['title']}: {s['detail']}" for s in plan[key]]
    L.append("")

    L.append("## Where to report")
    for r in plan["report"]:
        L.append(f"- {r['name']}: {r.get('phone', '')} {r.get('url', '')} {r['how']}".replace("  ", " "))
    L += ["", "## Attach", "- Screenshots of messages, links and payment confirmations", "- Bank statement showing the transaction",
          "", "_Automated summary. Review and correct details before submitting._"]
    return "\n".join(L)