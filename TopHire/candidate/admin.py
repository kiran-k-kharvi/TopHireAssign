from django.contrib import admin

from candidate.models import Resume


# Register your models here.
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')
