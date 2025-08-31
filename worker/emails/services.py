import os, aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from .config import *
from .exception import ErrorCode

class EmailService:
    def __init__(self):
        template_dir = os.path.join("app", "assets", "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))

    async def send_otp_email(self, email: str, fullname: str, otp: str):
        try:
            # Load & render template
            template = self.env.get_template("temp_otp.html")
            html_content = template.render(fullname=fullname, otp=otp)

            # Create message
            message = MIMEMultipart("alternative")
            message["From"] = USERNAME_SMTP
            message["To"] = email
            message["Subject"] = "[App-Api-Aio] Verification Code"
            message.attach(MIMEText(html_content, "html", "utf-8"))

            # Send mail
            await aiosmtplib.send(
                message,
                hostname=HOST_SMTP,
                port=PORT_SMTP,
                username=USERNAME_SMTP,
                password=PASSWORD_SMTP
            )

            print(f"[EmailService] Email sent successfully to {email}")

        except Exception as e:
            # print(f"[EmailService] Error sending email to {email}: {e}")
            raise ErrorCode.SendMailFailed()

