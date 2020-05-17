from django.contrib import admin
from benchmark.models import CipherResult, SystemInfo

# Register your models here.
admin.site.register(CipherResult)
admin.site.register(SystemInfo)
