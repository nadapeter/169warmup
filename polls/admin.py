from polls.models import User
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['username']}),
        (None,               {'fields': ['password']}),
        (None,               {'fields': ['count']}),
    ]
    list_display = ('username', 'password', 'count')


admin.site.register(User, UserAdmin)