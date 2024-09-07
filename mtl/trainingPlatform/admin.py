from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.http import HttpResponseForbidden

class MyAdminSite(admin.AdminSite):
    def has_permission(self, request):
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().has_permission(request)

admin_site = MyAdminSite(name='myadmin')