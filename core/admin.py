from django.contrib import admin
from .models import Branch, District, Print, FiscalSessionAD, FiscalSessionBS

# Register your models here.
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class BranchAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code"]


class PrintAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name"]


class FiscalSessionADAdmin(admin.ModelAdmin):
    list_display = ["id", "session_short_name"]


class FiscalSessionBSAdmin(admin.ModelAdmin):
    list_display = ["id", "session_short_name"]


admin.site.register(Print, PrintAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(FiscalSessionAD, FiscalSessionADAdmin)
admin.site.register(FiscalSessionBS, FiscalSessionBSAdmin)
