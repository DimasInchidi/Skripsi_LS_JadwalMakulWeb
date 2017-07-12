from JadwalKuliah.models import *
from django.contrib import admin
from django.utils.safestring import mark_safe


class FakultasAdmin(admin.ModelAdmin):
    list_display = ('universitas', 'fakultas')
    ordering = ('fakultas',)
    list_filter = ('fakultas',)


admin.site.register(Fakultas, FakultasAdmin)


class ProgramStudiAdmin(admin.ModelAdmin):
    list_display = ('fakultas', 'prodi')
    list_filter = ('prodi',)


admin.site.register(ProgramStudi, ProgramStudiAdmin)


class DosenAdmin(admin.ModelAdmin):
    list_display = ('dosen', 'fakultas')
    list_filter = ('fakultas',)


admin.site.register(Dosen, DosenAdmin)


class MataKuliahAdmin(admin.ModelAdmin):
    list_display = ('matakuliah', 'prodi')
    ordering = ('matakuliah',)
    list_filter = ('prodi',)


admin.site.register(MataKuliah, MataKuliahAdmin)


class RuangAdmin(admin.ModelAdmin):
    list_display = ('ruang', 'fakultas')
    ordering = ('ruang',)


admin.site.register(Ruang, RuangAdmin)


class KelasAdmin(admin.ModelAdmin):
    list_display = ('kelas', 'angkatan')
    ordering = ('angkatan',)
    list_filter = ('prodi',)


admin.site.register(Kelas, KelasAdmin)


class SKMengajarAdmin(admin.ModelAdmin):
    list_display = ('matakuliah', 'get_kelas', 'get_dosen')
    ordering = ('matakuliah',)
    exclude = ('terjadwal',)
    list_filter = (('dosen1', admin.RelatedOnlyFieldListFilter),)

    def get_kelas(self, obj):
        return obj.get_kelas()

    def get_dosen(self, obj):
        return obj.get_dosen()

    get_dosen.short_description = 'Dosen'
    get_kelas.short_description = 'Kelas'


admin.site.register(SKMengajar, SKMengajarAdmin)


class JadwalKuliahAdmin(admin.ModelAdmin):
    list_display = ('hari', 'jam_mulai', 'matakuliah', 'ruang', 'get_dosen', 'get_kelas')
    ordering = ('jam_mulai',)
    list_filter = ('hari',)
    readonly_fields = ('matakuliah_info',)

    def matakuliah_info(self, instance):
        return mark_safe("<span class='info'>Pastikan data SK Mengajar sudah benar sebelum membuat jadwal.</span>")

    def get_kelas(self, obj):
        return obj.matakuliah.get_kelas()

    def get_dosen(self, obj):
        return obj.matakuliah.get_dosen()

    get_dosen.short_description = 'Dosen'
    get_kelas.short_description = 'Kelas'


admin.site.register(JadwalKuliah, JadwalKuliahAdmin)
admin.site.site_header = 'Administrator Jadwal Kuliah'
