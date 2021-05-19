from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Profile
from .models import Contact

# without this, it won't show date fields, as they are not editable. Lazy.
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('last_check_in', 'checked_in_until',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contact)
