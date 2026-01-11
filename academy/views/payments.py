import uuid
import requests
import logging
from datetime import timedelta

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from ..models import Plan, Payment, PlanEnrollment

# Configure logger
logger = logging.getLogger(__name__)


@login_required
def paystack_init(request, slug):
    """
    Initialize a Paystack transaction for a plan.
    """
    plan = get_object_or_404(Plan, slug=slug)

    # Prevent double enrollment
    if PlanEnrollment.objects.filter(user=request.user, plan=plan).exists():
        messages.info(request, f"You are already enrolled in {plan.name}.")
        return redirect('plan_detail', slug=slug)

    # Generate unique reference
    reference = str(uuid.uuid4())
    amount = int(plan.price * 100)  # Convert to kobo

    # Create a Payment record
    payment = Payment.objects.create(
        user=request.user,
        plan=plan,
        amount=amount,
        reference=reference
    )

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "email": request.user.email,
        "amount": amount,
        "reference": reference,
        "callback_url": request.build_absolute_uri('/payment/verify/')
    }

    try:
        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            headers=headers,
            json=payload,
            timeout=10
        )
        response_data = response.json()
        logger.info(f"Paystack Init Response: {response_data}")

    except requests.RequestException as e:
        logger.error(f"Paystack request failed: {e}")
        messages.error(request, "Payment initialization failed. Please try again.")
        return redirect('pricing')

    # Check if Paystack returned a valid authorization URL
    if response_data.get('status') and response_data.get('data') and response_data['data'].get('authorization_url'):
        return redirect(response_data['data']['authorization_url'])
    else:
        logger.error(f"Invalid Paystack response: {response_data}")
        messages.error(request, f"Payment failed: {response_data.get('message', 'Unknown error')}")
        return redirect('pricing')


@login_required
def paystack_verify(request):
    """
    Verify a Paystack transaction after the user returns from Paystack.
    """
    reference = request.GET.get('reference') or request.GET.get('trxref')

    if not reference:
        messages.error(request, "No payment reference provided.")
        return redirect('pricing')

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    try:
        response = requests.get(
            f"https://api.paystack.co/transaction/verify/{reference}",
            headers=headers,
            timeout=10
        )
        response_data = response.json()
        logger.info(f"Paystack Verify Response: {response_data}")

    except requests.RequestException as e:
        logger.error(f"Paystack verification failed: {e}")
        messages.error(request, "Payment verification failed. Please try again.")
        return redirect('pricing')

    # Check if transaction was successful
    if response_data.get('status') and response_data.get('data') and response_data['data'].get('status') == 'success':
        try:
            # Mark payment as verified
            payment = Payment.objects.get(reference=reference)
            payment.verified = True
            payment.save()

            # Calculate plan expiration
            expires_at = timezone.now() + timedelta(weeks=payment.plan.duration_weeks)

            # Enroll user in plan
            PlanEnrollment.objects.get_or_create(
                user=payment.user,
                plan=payment.plan,
                defaults={'expires_at': expires_at}
            )

            messages.success(request, f"Payment successful! You are now enrolled in {payment.plan.name}.")
            return redirect('dashboard')

        except Payment.DoesNotExist:
            logger.error(f"Payment record not found for reference: {reference}")
            messages.error(request, "Payment record not found. Contact support.")
            return redirect('pricing')

    else:
        logger.warning(f"Payment not successful: {response_data}")
        messages.error(request, f"Payment failed: {response_data.get('message', 'Unknown error')}")
        return redirect('pricing')
