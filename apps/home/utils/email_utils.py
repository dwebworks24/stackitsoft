# utils/email_utils.py

from django.core.mail import send_mail, EmailMultiAlternatives, BadHeaderError
from django.conf import settings

def send_market_update_email(market, prices, recipient_list, updated_by):
    if not recipient_list:
        return False, "Recipient list is empty"

    subject = f"Market price updated: {market.name}"
    from_email = f"Stackitsoft <{getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')}>"
    logo_url = "https://stackitsoft.com/assets/images/logo/logo-final.png"  

    html_content = f"""
    <div style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
      <div style="max-width: 600px; margin: auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <div style="text-align: center; padding: 20px;">
          <img src="{logo_url}" alt="Logo" style="max-height: 45px;">
        </div>
        <div style="padding: 20px;">
          <h2 style="color: #333;">Market Price Updated: {market.name}</h2>
          <p><strong>Updated by:</strong> {updated_by.username}</p>
          <p><strong>Unit:</strong> {market.unit}</p>
          <h4 style="color: #555;">Updated Prices:</h4>
          <ul style="padding-left: 20px;">
            {''.join(f'<li><strong>{hour.replace("_", " ").upper().replace("PRICE ", "")}:</strong> {getattr(market, hour) or "-"}</li>' for hour in prices.keys())}
          </ul>
          <p style="margin-top: 30px;">Best regards,<br><strong>{updated_by.username}</strong></p>
        </div>
      </div>
    </div>
    """

    try:
        msg = EmailMultiAlternatives(subject, '', from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Email sending failed: {str(e)}"



def send_market_update_email_by_admin(market, prices, recipient_list, updated_by):
    x = "din"
    if not recipient_list:
        return False, "Recipient list is empty"

    subject = f"Market price updated: {market.name}"
    from_email = f"Stackitsoft <{getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')}>"
    logo_url = "https://stackitsoft.com/assets/images/logo/logo-final.png"

    # Format the prices list into HTML
    price_html = ''.join(
        f'<li><strong>{key.replace("price_", "").upper()}:</strong> {value or "-"}</li>'
        for key, value in prices.items()
    )

    html_content = f"""
    <div style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
      <div style="max-width: 600px; margin: auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <div style="text-align: center; padding: 20px;">
          <img src="{logo_url}" alt="Logo" style="max-height: 45px;">
        </div>
        <div style="padding: 20px;">
          <h2 style="color: #333;">Market Price Updated: {market.name}</h2>
          <p><strong>Updated by:</strong> {updated_by.username}</p>
          <p><strong>Unit:</strong> {market.unit}</p>
          <h4 style="color: #555;">Updated Prices:</h4>
          <ul style="padding-left: 20px;">
            {price_html}
          </ul>
          <p style="margin-top: 30px;">Best regards,<br><strong>{updated_by.username}</strong></p>
        </div>
      </div>
    </div>
    """

    try:
        msg = EmailMultiAlternatives(subject, '', from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Email sending failed: {str(e)}"