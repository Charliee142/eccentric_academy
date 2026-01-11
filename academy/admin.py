from django.contrib import admin
from django.utils.html import format_html
from .models import *


class PlanAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ("name", "price", "duration_weeks", "is_active")


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("title", "plan",)



class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject")


class CohortAlertAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "message")


class ProgramOutcomeAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "icon_preview", "order", "is_active")
    list_editable = ("level", "order", "is_active")

    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html(
                '<img src="{}" width="40" style="border-radius:8px;" />',
                obj.icon_image.url
            )
        return "-"


class CohortAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "registration_deadline",
        "max_slots",
        "slots_taken",
        "is_active",
    )
    list_editable = ("is_active",)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'order')
    list_editable = ('order',)


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)


class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active', 'order')
    list_editable = ('is_active', 'order')


admin.site.register(PlanEnrollment)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Payment)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(CohortAlert, CohortAlertAdmin)
admin.site.register(ProgramOutcome, ProgramOutcomeAdmin)
admin.site.register(Cohort, CohortAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)


