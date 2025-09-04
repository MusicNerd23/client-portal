import os
import smtplib
from email.mime.text import MIMEText


def _env_bool(name: str, default: bool = False) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "on")


def send_email(subject: str, body: str, recipients: list[str]) -> None:
    """Best-effort email sender.

    Falls back to printing to stdout if mail is not configured.
    Configure via env: MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD,
    MAIL_USE_TLS, MAIL_USE_SSL, MAIL_DEFAULT_SENDER.
    """
    recipients = [r for r in recipients if r]
    if not recipients:
        return

    server = os.environ.get("MAIL_SERVER")
    sender = os.environ.get("MAIL_DEFAULT_SENDER", os.environ.get("MAIL_USERNAME"))
    if not server or not sender:
        print(f"[notify] {subject} -> {', '.join(recipients)}\n{body}")
        return

    port = int(os.environ.get("MAIL_PORT", "587"))
    username = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")
    use_tls = _env_bool("MAIL_USE_TLS", True)
    use_ssl = _env_bool("MAIL_USE_SSL", False)

    msg = MIMEText(body, _subtype="plain", _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    if use_ssl:
        smtp = smtplib.SMTP_SSL(server, port)
    else:
        smtp = smtplib.SMTP(server, port)
    try:
        smtp.ehlo()
        if use_tls and not use_ssl:
            smtp.starttls()
        if username and password:
            smtp.login(username, password)
        smtp.sendmail(sender, recipients, msg.as_string())
    finally:
        try:
            smtp.quit()
        except Exception:
            pass

