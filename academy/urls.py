from django.urls import path
from .views import pages, plans, payments

urlpatterns = [
    path('', pages.home, name='home'),
    path('about/', pages.about, name='about'),
    path('pricing/', pages.pricing, name='pricing'),
    path('programs/', pages.programs, name='programs'),
    path('contact/', pages.contact, name='contact'),
    path('faq/', pages.faq, name='faq'),
    path('testimonials/', pages.testimonials, name='testimonials'),

    path('plan/<slug:slug>/', plans.plan_detail, name='plan_detail'),
    path('plan/<slug:slug>/enroll/', plans.enroll_plan, name='enroll_plan'),

    path('dashboard/', pages.dashboard, name='dashboard'),

    path('plan/<slug:slug>/pay/', payments.paystack_init, name='paystack_init'),
    path('payment/verify/', payments.paystack_verify, name='paystack_verify'),

    path('register-now/', pages.register_now, name='register_now'),

]

