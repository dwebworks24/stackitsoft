# utils/email_utils.py

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

def send_market_update_email(market, prices, recipient_list,updated_by):
    if not recipient_list:
        return False, "Recipient list is empty"

    subject = f"Market price updated: {market.name}"
    message = (
        f"The market information for {market.name} has been updated by {updated_by.username}.\n\n"
        f"Unit: {market.unit}\n\n"
        f"Updated Prices:\n" +
        "\n".join(
            f"- {hour.replace('_', ' ').upper().replace('PRICE ', '')}: {getattr(market, hour) or '-'}"
            for hour in prices.keys()
        ) +
        f"\n\nBest regards,\n{updated_by.username}"
    )
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return True, "Email sent successfully"
    except BadHeaderError:
        return False, "Invalid header found"
    except Exception as e:
        return False, f"Email sending failed: {str(e)}"