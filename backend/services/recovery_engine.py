"""Turns "what happened" into a prioritized recovery plan.

Exposure -> actions. Steps are grouped by when they matter:
  do_now (first hour) -> within_24h -> this_week
Reporting directory is per country. VERIFY these contacts before shipping and review them regularly.
"""
from typing import Any

REPORTING = {
    "IN": [
        {"name": "National Cybercrime Helpline", "how": "Call 1930 right away if money was lost. Early reports give the best chance of freezing funds.", "phone": "1930"},
        {"name": "National Cyber Crime Reporting Portal", "how": "File a complaint online.", "url": "https://cybercrime.gov.in"},
        {"name": "Sanchar Saathi (Chakshu)", "how": "Report suspicious calls, SMS and WhatsApp numbers.", "url": "https://sancharsaathi.gov.in"},
    ],
    "US": [
        {"name": "FTC", "how": "Report the scam.", "url": "https://reportfraud.ftc.gov"},
        {"name": "FBI IC3", "how": "Report internet crime, especially if money was sent.", "url": "https://www.ic3.gov"},
        {"name": "IdentityTheft.gov", "how": "Get a personal recovery plan if your identity was exposed.", "url": "https://www.identitytheft.gov"},
    ],
    "UK": [
        {"name": "Action Fraud", "how": "Report fraud and cybercrime. Check the current name and site, as the service is being reorganised.", "phone": "0300 123 2040", "url": "https://www.actionfraud.police.uk"},
        {"name": "Forward scam texts", "how": "Forward the SMS to 7726 (free).", "phone": "7726"},
    ],
    "AU": [
        {"name": "Scamwatch", "how": "Report the scam.", "url": "https://www.scamwatch.gov.au"},
        {"name": "ReportCyber", "how": "Report cybercrime to police.", "url": "https://www.cyber.gov.au/report-and-recover/report"},
    ],
    "CA": [
        {"name": "Canadian Anti-Fraud Centre", "how": "Report fraud.", "phone": "1-888-495-8501", "url": "https://www.antifraudcentre-centreantifraude.ca"},
    ],
}
GENERIC_REPORT = [{"name": "Local police / national cybercrime unit", "how": "File a report and keep the reference number. Search for your country's official scam-reporting site."}]


def _s(title: str, detail: str) -> dict:
    return {"title": title, "detail": detail}


def build_plan(i: dict[str, Any]) -> dict:
    exp, now, day, week = [], [], [], []
    country = (i.get("country") or "").upper()
    method = (i.get("payment_method") or "").lower()
    sent = bool(i.get("sent_money"))
    hours = i.get("hours_since")

    def add(item, severity, why):
        exp.append({"item": item, "severity": severity, "why": why})

    if sent:
        add("Money sent", "critical", "Money moves fast. The first hours are the best window to stop or reverse it.")
        now.append(_s("Call your bank or payment app now", "Say you were scammed and ask them to freeze or recall the transaction. Note the reference number they give you."))
        if country == "IN":
            now.append(_s("Call 1930", "India's cybercrime helpline. Give the transaction ID, amount, time and the receiving account or UPI ID."))
        if method == "upi":
            now.append(_s("Raise a UPI dispute", "Use the 'Report / Raise dispute' option in your UPI app, and also complain to your bank."))
        elif method == "card":
            now.append(_s("Block your card and dispute the charge", "Ask for a chargeback. Request a replacement card with a new number."))
        elif method == "crypto":
            now.append(_s("Contact the exchange you used", "Give them the wallet address and transaction hash. Recovery is rarely possible, but exchanges can flag the receiving wallet."))
        elif method == "gift_card":
            now.append(_s("Contact the gift card issuer", "Give them the card numbers and receipts. Ask them to freeze any remaining balance."))
        elif method == "bank_transfer":
            now.append(_s("Ask your bank for a transfer recall", "Provide the beneficiary account details and transaction time."))
        day.append(_s("Expect follow-up 'recovery' scams", "Scammers sell fake help getting your money back for a fee. Only deal with your bank and the police."))

    if i.get("gave_remote_access"):
        add("Remote access to your device", "critical", "The scammer could see your screen, read OTPs and open apps.")
        now.append(_s("Disconnect and remove remote-access apps", "Turn on airplane mode, then uninstall AnyDesk, TeamViewer, QuickSupport or any unknown app."))
        now.append(_s("Use a different device to secure your accounts", "Change banking and email passwords from a clean phone or computer."))
        week.append(_s("Consider a factory reset", "This is the surest way to remove hidden malware. Back up photos and contacts first, but not apps."))

    if i.get("installed_app") or i.get("downloaded_file"):
        add("Malicious app or file", "high", "Fake apps and files can read SMS, capture keystrokes or overlay bank screens.")
        now.append(_s("Uninstall it and go offline", "Remove the app or delete the file. Turn off mobile data and Wi-Fi until you've done so."))
        day.append(_s("Run a security scan", "Use Google Play Protect, or Microsoft Defender or another trusted antivirus on a computer."))
        day.append(_s("Check app permissions", "Open Settings > Apps > Special access and remove Accessibility, Device admin and SMS access for anything unfamiliar."))
        week.append(_s("Factory reset if problems continue", "Unexplained pop-ups, battery drain or unknown apps mean the device may still be compromised."))

    if i.get("entered_password"):
        add("Password", "high", "Anyone with it can log in, and may try it on your other accounts.")
        now.append(_s("Change that password from a safe device", "Then change it anywhere else you used the same or a similar password."))
        day.append(_s("Sign out of all devices", "Most services have a 'log out everywhere' option in security settings."))
        day.append(_s("Turn on two-factor authentication", "Prefer an authenticator app over SMS."))
        week.append(_s("Check the account for changes", "Look at recovery email, phone number, forwarding rules and recent logins."))

    if i.get("entered_otp"):
        add("One-time code (OTP)", "critical", "An OTP usually authorises a login or payment, so the scammer may already be inside.")
        now.append(_s("Check for transactions and logins right now", "Open your bank, UPI and email accounts and look for anything you didn't do."))
        now.append(_s("Contact your bank if anything looks wrong", "Ask them to block transactions and reset online access."))

    if i.get("entered_card_details"):
        add("Card details", "critical", "Card number, expiry and CVV are enough to make many online payments.")
        now.append(_s("Block or freeze the card", "Use your banking app or call the number on the back of the card."))
        day.append(_s("Review recent transactions and dispute unknown ones", "Ask for a replacement card."))

    if i.get("shared_id_documents"):
        add("ID documents", "high", "IDs can be used for fake loans, SIM cards and account openings.")
        day.append(_s("Lock your ID where possible", "In India, lock Aadhaar biometrics in the mAadhaar app or at uidai.gov.in. Elsewhere, ask about fraud alerts."))
        week.append(_s("Check your credit report", "Look for accounts or loans you didn't open. Place a fraud alert or credit freeze if available."))
        week.append(_s("Monitor your SIM and accounts", "Sudden loss of mobile signal can mean a SIM swap. Contact your carrier immediately."))

    if i.get("clicked_link") and not exp:
        add("Link opened, no details entered", "low", "Just opening a link is usually low risk, but some pages try to trigger downloads or prompts.")
        now.append(_s("Don't enter anything else, and close the page", "If it asked for permissions or downloaded something, deny it and check your downloads."))
        day.append(_s("Update your browser and phone", "Security updates close the holes that malicious pages use."))
    elif i.get("clicked_link"):
        add("Link opened", "low", "The page may have tried to collect more than what you told us.")

    if not exp:
        add("No confirmed exposure", "low", "Nothing you told us suggests you shared sensitive information.")
        day.append(_s("Delete the message and block the sender", "Report it as spam or phishing in your app."))

    # Always-useful steps
    now.append(_s("Save evidence before you delete anything", "Screenshot messages, links, phone numbers and payment receipts. Use 'Evidence pack' in this app."))
    day.append(_s("Warn people close to you", "Scammers often try the same trick on your contacts, sometimes using your name."))
    week.append(_s("Watch for follow-up attempts", "Ignore calls or messages claiming to 'help' you recover money, or verify with an official number."))

    sev_rank = {"critical": 3, "high": 2, "low": 1}
    top = max(sev_rank[e["severity"]] for e in exp)
    if top == 3 and hours is not None and hours > 72:
        urgency = "high"
    else:
        urgency = {3: "critical", 2: "high", 1: "low"}[top]

    return {
        "urgency": urgency,
        "headline": {"critical": "Act now. The next hour matters most.",
                     "high": "Act today to limit the damage.",
                     "low": "Low exposure. A few precautions are enough."}[urgency],
        "exposures": sorted(exp, key=lambda e: -sev_rank[e["severity"]]),
        "do_now": now, "within_24h": day, "this_week": week,
        "report": REPORTING.get(country, GENERIC_REPORT),
        "prevent": [
            "Never share OTPs, PINs or passwords. No bank or agency will ask.",
            "Install apps only from official stores and never from links in messages.",
            "Verify by calling the number on the official website or your card.",
            "Turn on two-factor authentication with an authenticator app.",
            "Slow down. Urgency is the scammer's main tool.",
        ],
    }