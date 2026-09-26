"""Public, server-rendered pages for Google OAuth brand verification.

Google's verification crawler needs, WITHOUT logging in and WITHOUT running
JavaScript:
  * a home page that explains the app, uses the same app name as the OAuth
    consent screen and links to the privacy policy,
  * a privacy policy that fully describes how Google user data is handled,
  * (optionally) a Search Console ownership meta tag.

These routes are plain HTML so they respond instantly and are fully readable
by bots. The React app still owns every other route (/login, /dashboard ...).

Env:
  APP_PUBLIC_NAME             name shown on the pages — must match the OAuth
                              consent screen "App name" exactly (default MailShield)
  GOOGLE_SITE_VERIFICATION    content value of the Search Console HTML-tag method
  CONTACT_EMAIL               public contact / privacy e-mail
"""
from __future__ import annotations

import html
import os
from datetime import date

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(include_in_schema=False)

APP = os.getenv("APP_PUBLIC_NAME", "MailShield")
CONTACT = os.getenv("CONTACT_EMAIL", "baranidharanboopathy66@gmail.com")
UPDATED = os.getenv("POLICY_LAST_UPDATED", "27 September 2026")

CSS = """
*{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;color:#1d2433;background:#fbfaf8;line-height:1.6}
a{color:#b9301f}header,footer{background:#fff;border-bottom:1px solid #e7e3dd}footer{border-top:1px solid #e7e3dd;border-bottom:0;margin-top:48px}
.wrap{max-width:980px;margin:0 auto;padding:18px 20px}.nav{display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.brand{font-weight:700;font-size:20px;color:#1d2433;text-decoration:none;margin-right:auto}.brand span{color:#b9301f}
.btn{display:inline-block;background:#b9301f;color:#fff;text-decoration:none;padding:10px 18px;border-radius:8px;font-weight:700}
.btn.o{background:#fff;color:#1d2433;border:1px solid #cfc9c0}
h1{font-size:34px;line-height:1.2;margin:34px 0 12px}h2{font-size:21px;margin:30px 0 8px}h3{font-size:16px;margin:0 0 4px}
.lead{font-size:18px;color:#4a4f5c}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-top:16px}
.card{background:#fff;border:1px solid #e7e3dd;border-radius:10px;padding:16px}.card p{margin:0;color:#4a4f5c;font-size:14px}
table{border-collapse:collapse;width:100%;background:#fff;font-size:14px}td,th{border:1px solid #e7e3dd;padding:8px 10px;text-align:left;vertical-align:top}
th{background:#f3f0ec}.note{background:#fff7e6;border:1px solid #f0d9a8;border-radius:8px;padding:12px 14px;font-size:14px}
small,.muted{color:#6b7080}
"""


def _page(title: str, body: str, extra_head: str = "") -> HTMLResponse:
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{APP} — AI-powered email threat detection, geolocation and forensic intelligence platform.">
<meta name="application-name" content="{APP}">{extra_head}
<link rel="icon" type="image/svg+xml" href="/shield.svg"><style>{CSS}</style></head><body>
<header><div class="wrap nav"><a class="brand" href="/">{APP}<span>.</span></a>
<a href="/#features">Features</a><a href="/privacy-policy">Privacy Policy</a><a href="/terms">Terms of Service</a>
<a class="btn" href="/login">Sign in</a></div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap nav"><span class="muted">© {date.today().year} {APP} · Smart India Hackathon 2026 · PS 26106</span>
<a href="/privacy-policy">Privacy Policy</a><a href="/terms">Terms of Service</a><a href="mailto:{CONTACT}">Contact</a></div></footer>
</body></html>"""
    return HTMLResponse(doc, headers={"Cache-Control": "public, max-age=300"})


@router.api_route("/", methods=["GET", "HEAD"])
def home():
    token = os.getenv("GOOGLE_SITE_VERIFICATION", "").strip()
    meta = f'\n<meta name="google-site-verification" content="{html.escape(token)}">' if token else ""
    body = f"""
<h1>{APP} — AI-powered email threat detection &amp; forensic intelligence</h1>
<p class="lead">{APP} protects people and organisations from phishing, spoofed senders, business-email-compromise (BEC)
fraud and malicious attachments. It analyses an email, explains why it is dangerous, traces where it really came from and
produces an evidence-grade forensic report.</p>
<p><a class="btn" href="/login">Sign in / Create free account</a> &nbsp; <a class="btn o" href="/privacy-policy">Read our Privacy Policy</a></p>

<h2 id="features">What {APP} does</h2>
<div class="grid">
<div class="card"><h3>Detect threats</h3><p>AI/ML and NLP models plus forensic rules classify each email as safe, suspicious or malicious — phishing, impersonation, BEC and credential-harvesting.</p></div>
<div class="card"><h3>Trace the origin</h3><p>Checks SPF, DKIM and DMARC, rebuilds the mail-server relay path and maps the sending IP's approximate location.</p></div>
<div class="card"><h3>Analyse attachments safely</h3><p>Suspicious attachments and links are inspected in an isolated sandbox — they are never opened on the main server.</p></div>
<div class="card"><h3>Explain &amp; report</h3><p>Every verdict lists exactly what went wrong and is saved as a tamper-evident forensic report for investigators.</p></div>
</div>

<h2>How {APP} uses your Gmail account (optional)</h2>
<p>Connecting Gmail is optional — you can also upload an <code>.eml</code> file or paste an email instead. If you choose to connect,
{APP} uses Google Sign-In (OAuth) and asks for these permissions:</p>
<table><tr><th>Permission</th><th>Why {APP} needs it</th></tr>
<tr><td>Read your email messages (gmail.readonly)</td><td>To scan new messages in your inbox for phishing and fraud and show you the analysis.</td></tr>
<tr><td>Modify labels (gmail.modify)</td><td>Only when <b>you</b> press “Quarantine”: moves that one message to a “Quarantine” (or Spam) label, and back to the inbox if you release it. {APP} never deletes or sends email.</td></tr>
<tr><td>Email address &amp; basic profile</td><td>To identify your account and keep your data separate from other users.</td></tr></table>
<p class="note">{APP}'s use and transfer of information received from Google APIs adheres to the
<a href="https://developers.google.com/terms/api-services-user-data-policy">Google API Services User Data Policy</a>,
including the Limited Use requirements. Google user data is never sold, never used for advertising and never used to train AI models.
Full details are in our <a href="/privacy-policy">Privacy Policy</a>.</p>

<h2>Who it is for</h2>
<p>Individuals, colleges, companies, government departments and cyber-crime investigators who need to detect email fraud early
and investigate where it came from. {APP} was built for Smart India Hackathon 2026 (Problem Statement 26106, AICTE Cyber Security Cell).</p>
"""
    return _page(f"{APP} — AI-powered email threat detection", body, meta)


@router.api_route("/privacy-policy", methods=["GET", "HEAD"])
def privacy():
    body = f"""
<h1>{APP} Privacy Policy</h1><p class="muted">Last updated: {UPDATED}</p>
<p>This policy explains what information {APP} (“we”, “the app”) collects, how it is used, stored, shared and deleted, and the
choices you have. It applies to the website at https://mailshield-sih.onrender.com and all {APP} features.</p>

<h2>1. Information we collect</h2>
<ul>
<li><b>Account information:</b> your name, email address and a securely hashed password (Argon2) when you register.</li>
<li><b>Emails you submit:</b> <code>.eml</code> files you upload or text you paste for analysis.</li>
<li><b>Google user data (only if you connect Gmail):</b> email messages in your Gmail inbox (headers, body, attachments and labels)
read through the Gmail API, and your Google account email address and basic profile.</li>
<li><b>Analysis results:</b> threat scores, indicators, forensic findings and reports generated from those emails.</li>
<li><b>Technical logs:</b> audit logs of actions (for example “email quarantined”) and standard server logs. We do not use advertising or tracking cookies.</li>
</ul>

<h2>2. How we use Google user data</h2>
<p>We request the following Google OAuth scopes and use them only for the purposes below:</p>
<table><tr><th>Scope</th><th>Data accessed</th><th>Purpose</th></tr>
<tr><td>https://www.googleapis.com/auth/gmail.readonly</td><td>Your email messages and metadata</td><td>Scan incoming messages for phishing, spoofing, fraud and malware and display the results to you.</td></tr>
<tr><td>https://www.googleapis.com/auth/gmail.modify</td><td>Labels of a specific message</td><td>Move a message to a “Quarantine” (or Spam) label and back <b>only when you choose to</b>. We never delete, send or forward email.</td></tr>
<tr><td>userinfo.email, userinfo.profile</td><td>Email address, name</td><td>Sign you in and link the connected mailbox to your {APP} account.</td></tr></table>
<p>We use Google user data <b>only</b> to provide and improve the user-facing email-security features of {APP} that you see in the app.
We do <b>not</b>:</p>
<ul><li>sell Google user data or transfer it to data brokers or advertisers;</li>
<li>use it for advertising, retargeting or personalised ads;</li>
<li>use it to develop, improve or train generalised or non-personalised AI/ML models;</li>
<li>allow humans to read your email, except (a) with your explicit consent, (b) where necessary for security purposes such as investigating abuse,
(c) to comply with applicable law, or (d) when data is aggregated and anonymised for internal operations.</li></ul>
<p class="note"><b>Limited Use disclosure:</b> {APP}'s use and transfer to any other app of information received from Google APIs will adhere to the
<a href="https://developers.google.com/terms/api-services-user-data-policy">Google API Services User Data Policy</a>, including the Limited Use requirements.</p>

<h2>3. How emails are analysed</h2>
<ul>
<li>Emails are analysed by our own detection engine (rules, machine-learning and NLP models) on our server.</li>
<li>Suspicious attachments and links are sent to {APP}'s own isolated sandbox service for static analysis. The sandbox receives only the
attachment files, links and message body — never your password, Google tokens or account details — and keeps nothing after analysis.</li>
<li>If the AI-explanation or assistant features are enabled, short excerpts of the analysed email may be sent to Google's Gemini API
solely to generate the explanation you requested. These excerpts are not used by us for any other purpose.</li>
<li>To trace where an email came from, sender IP addresses and domain names (not email content) may be looked up with public IP-geolocation,
DNS and threat-reputation services.</li></ul>

<h2>4. Sharing</h2>
<p>We do not share your personal data or Google user data with third parties, except the processors listed in section 3 needed to provide the
feature you used, our hosting provider (Render) which stores the data on our behalf, or when required by law. Reports you choose to download or
share are under your control.</p>

<h2>5. Storage, security and retention</h2>
<ul>
<li>Data is stored in a PostgreSQL database hosted on Render. Connections use HTTPS/TLS.</li>
<li>Google OAuth tokens are encrypted at rest (Fernet/AES) and are used only by the server; they are never shown in the browser.</li>
<li>Each user can see only their own data (per-user isolation). Forensic reports are protected by a SHA-256 hash chain that stores only hashes, not email content.</li>
<li>Analysed emails and reports are automatically deleted after <b>90 days</b> (configurable), or earlier when you delete them.</li></ul>

<h2>6. Your choices and rights</h2>
<ul>
<li><b>Delete your data:</b> in the app open <i>Privacy &amp; Compliance</i> and use the delete-my-data option to erase all your analyses, reports and stored Gmail tokens, or delete individual cases.</li>
<li><b>Disconnect Gmail:</b> disconnect in the app, or revoke access at any time at <a href="https://myaccount.google.com/permissions">myaccount.google.com/permissions</a>.</li>
<li><b>Access or correction:</b> email us at <a href="mailto:{CONTACT}">{CONTACT}</a>. We respond within 30 days.</li>
<li>We process personal data in line with India's Digital Personal Data Protection Act, 2023.</li></ul>

<h2>7. Children</h2><p>{APP} is not directed at children under 18 and we do not knowingly collect their data.</p>
<h2>8. Changes</h2><p>We will post any change to this policy on this page and update the “Last updated” date.</p>
<h2>9. Contact</h2><p>{APP} — Team Raven Forge · Email: <a href="mailto:{CONTACT}">{CONTACT}</a></p>
"""
    return _page(f"Privacy Policy — {APP}", body)


@router.api_route("/terms", methods=["GET", "HEAD"])
def terms():
    body = f"""
<h1>{APP} Terms of Service</h1><p class="muted">Last updated: {UPDATED}</p>
<p>By creating an account or using {APP} you agree to these terms.</p>
<h2>1. The service</h2><p>{APP} is an email-security and forensic-analysis tool built for Smart India Hackathon 2026. It is provided free of charge,
“as is”, as a prototype, without warranties of any kind. Threat verdicts are decision support, not a guarantee; always use your own judgement.</p>
<h2>2. Your account</h2><p>Keep your password confidential. You are responsible for activity under your account. Only connect mailboxes you own or are authorised to analyse.</p>
<h2>3. Acceptable use</h2><p>Do not use {APP} to break the law, to access other people's email without permission, to attack or overload the service, or to upload material you have no right to share.
Reports produced by {APP} may be used for your security, incident-response and legal purposes.</p>
<h2>4. Google data</h2><p>Use of Gmail data is governed by our <a href="/privacy-policy">Privacy Policy</a> and the Google API Services User Data Policy, including the Limited Use requirements.</p>
<h2>5. Liability</h2><p>To the extent permitted by law, the {APP} team is not liable for losses arising from use of the prototype, including missed or incorrect detections.</p>
<h2>6. Termination</h2><p>You may stop using {APP} and delete your data at any time. We may suspend accounts that misuse the service.</p>
<h2>7. Governing law</h2><p>These terms are governed by the laws of India.</p>
<h2>8. Contact</h2><p><a href="mailto:{CONTACT}">{CONTACT}</a></p>
"""
    return _page(f"Terms of Service — {APP}", body)
