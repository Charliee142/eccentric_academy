from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import *
from django.core.mail import send_mail
from django.conf import settings
from ..forms import ContactForm
from django.contrib import messages

def home(request):
    plans = Plan.objects.all()
    outcomes = ProgramOutcome.objects.filter(is_active=True)
    return render(request, 'academy/home.html', {'plans': plans, 'outcomes': outcomes})

def about(request):
    return render(request, 'academy/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if not all([name, email, subject, message]):
            messages.error(request, "All fields are required.")
            return redirect("contact")

        # Save to database
        contact = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

        # 1️⃣ Send notification to admin
        send_mail(
            subject=f"New Contact Message: {subject}",
            message=f"""
Name: {name}
Email: {email}

Message:
{message}
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )

        # 2️⃣ Auto-reply to user
        send_mail(
            subject="Thank you for contacting Eccentric Academy!",
            message=f"""
Hi {name},

Thank you for reaching out to us. We have received your message:

Subject: {subject}
Message: {message}

Our team will get back to you shortly.

Best regards,
Eccentric Academy
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        messages.success(request, "Your message has been sent successfully.")
        return redirect("contact")

    return render(request, "academy/contact.html")


def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'academy/faq.html', {'faqs': faqs})

def testimonials(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'academy/testimonial.html', {'testimonials': testimonials})

def pricing(request):
    plans = Plan.objects.all()
    return render(request, 'academy/pricing.html', {'plans': plans})

def programs(request):
    outcomes = ProgramOutcome.objects.filter(is_active=True)
    return render(request, 'academy/programs.html', {'outcomes': outcomes})

@login_required
def dashboard(request):
    enrollments = PlanEnrollment.objects.filter(user=request.user)
    return render(
        request,
        'academy/dashboard.html',
        {'enrollments': enrollments}
    )

def register_now(request):
    """
    CTA logic:
    - If user is logged in → go to pricing
    - Else → signup
    """
    if request.user.is_authenticated:
        return redirect('pricing')
    return redirect('account_signup')


