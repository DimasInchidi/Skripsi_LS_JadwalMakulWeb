from django.db import models

from SkripsiLara.JadwalKuliah import TanggalFields


class Jadwal(models.Model):
    Hari = TanggalFields.DayOfTheWeekField()
    Jam = models.TimeField()
    Jam_hingga = models.TimeField(default='00:00:00', blank=True)
    Ruang = models.CharField(max_length=40)
    SKS = models.IntegerField(default='', blank=True)
    Kelas = models.CharField(max_length=40, default='', blank=True)
    MataKuliah = models.CharField(max_length=100)
    Dosen_1 = models.CharField(max_length=100)
    Dosen_2 = models.CharField(max_length=100, default='', blank=True)
    Dosen_3 = models.CharField(max_length=100, default='', blank=True)


class Meta:
    unique_together = ('Hari', 'Jam',)
