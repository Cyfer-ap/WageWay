from django.http import HttpResponse
from .utils import send_dynamic_email
from django.contrib.auth.decorators import login_required

@login_required
def test_email(request):
    send_dynamic_email(
        subject='Test Email',
        to_email=request.user.email,
        template_name='emails/welcome_customer.html',
        context={'user': request.user}
    )
    return HttpResponse("Test email sent.")
