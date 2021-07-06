import smtplib
import ssl


def send_verification_email(receiver_email, otp):
    # function to send the OTP to the account registered :)
    port = 465 # for ssl
    username = "attaskmanagermail@gmail.com"
    password = "abviktor4o"

    message = f"""Subject: TaskManager Account Verification\n\n
    This is an automatic verification email sent to you by the TaskManager app. Your OTP password is {otp} and you have
    5 minutes to enter it.
    """

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, f"<{receiver_email}>", message)
            return 1
    except Exception:
        return 0