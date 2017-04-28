from django.contrib import admin

from SkripsiLara.JadwalKuliah.models import Jadwal


# Register your models here.
class JadwalAdmin(admin.ModelAdmin):
    list_display = ('Hari',)
    search_fields = ['MataKuliah']


admin.site.register(Jadwal, JadwalAdmin)
admin.site.site_header = 'Administrator Jadwal Kuliah'
