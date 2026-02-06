def send_password_reset_email(email: str, reset_link: str):
    # MVP: just log it
    print(f"Password reset link for {email}: {reset_link}")
