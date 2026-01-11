from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "John Doe"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "you@example.com"
            }),
            "subject": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Course Inquiry"
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write your message here...",
                "rows": 5
            }),
        }
