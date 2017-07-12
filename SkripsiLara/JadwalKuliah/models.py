from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext as _


class Fakultas(models.Model):
    fakultas = models.CharField(max_length=75, unique=True)
    universitas = models.CharField(max_length=75)
    alamat = models.TextField()
    kontak = models.TextField()

    class Meta:
        verbose_name = 'Fakultas'
        verbose_name_plural = 'Fakultas-fakultas'
        ordering = ['fakultas']

    def __str__(self):
        return self.fakultas


class ProgramStudi(models.Model):
    fakultas = models.ForeignKey(Fakultas, on_delete=models.CASCADE)
    prodi = models.CharField(max_length=75)

    class Meta:
        unique_together = ('fakultas', 'prodi')
        verbose_name = 'Program studi'
        verbose_name_plural = 'Program studi'
        ordering = ['prodi']

    def __str__(self):
        return self.prodi


class Dosen(models.Model):
    dosen = models.CharField(max_length=75, unique=True)
    email = models.EmailField(default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    fakultas = models.ForeignKey(Fakultas, blank=True, null=True)

    class Meta:
        verbose_name = 'Dosen'
        verbose_name_plural = 'Dosen-dosen'
        ordering = ['dosen']

    def __str__(self):
        return self.dosen


class MataKuliah(models.Model):
    matakuliah = models.CharField(max_length=75)
    prodi = models.ForeignKey(ProgramStudi, on_delete=models.CASCADE)
    sks = models.PositiveIntegerField()
    semester = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('matakuliah', 'prodi',)
        verbose_name = 'Mata kuliah'
        verbose_name_plural = 'Mata kuliah'
        ordering = ['prodi']

    def __str__(self):
        return self.matakuliah


class Ruang(models.Model):
    ruang = models.CharField(max_length=75, unique=True)
    fakultas = models.ForeignKey(Fakultas, blank=True, null=True)

    class Meta:
        verbose_name = 'Ruang'
        verbose_name_plural = 'Ruang Kelas'
        ordering = ['ruang']

    def __str__(self):
        return self.ruang


class Kelas(models.Model):
    kelas = models.CharField(max_length=75)
    angkatan = models.PositiveIntegerField()
    prodi = models.ForeignKey(ProgramStudi, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('kelas', 'angkatan',)
        verbose_name = 'Kelas'
        verbose_name_plural = 'Kelas-kelas'
        ordering = ['kelas']

    def __str__(self):
        return self.kelas


class SKMengajar(models.Model):
    matakuliah = models.ForeignKey(MataKuliah, on_delete=models.CASCADE)
    dosen1 = models.ForeignKey(Dosen, related_name='+', on_delete=models.CASCADE)
    dosen2 = models.ForeignKey(Dosen, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    dosen3 = models.ForeignKey(Dosen, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    kelas1 = models.ForeignKey(Kelas, related_name='+', on_delete=models.CASCADE)
    kelas2 = models.ForeignKey(Kelas, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    kelas3 = models.ForeignKey(Kelas, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    kelas4 = models.ForeignKey(Kelas, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    kelas5 = models.ForeignKey(Kelas, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    terjadwal = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'SK Mengajar'
        verbose_name_plural = 'SK Mengajar'
        ordering = ['matakuliah']

    def __str__(self):
        return self.matakuliah.matakuliah

    def get_kelas(self):
        result = self.kelas1.kelas
        if self.kelas2:
            result += " / " + self.kelas2.kelas
        if self.kelas3:
            result += " / " + self.kelas3.kelas
        if self.kelas4:
            result += " / " + self.kelas4.kelas
        if self.kelas5:
            result += " / " + self.kelas5.kelas
        return result

    def get_dosen(self):
        result = self.dosen1.dosen
        if self.dosen2:
            result += " / " + self.dosen2.dosen
        if self.dosen3:
            result += " / " + self.dosen3.dosen
        return result

    def dosen_count(self):
        fieldname = 'dosen'
        self.objects.values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))


class JadwalKuliah(models.Model):
    DAY_OF_THE_WEEK = {
        '1': _(u'Senin'),
        '2': _(u'Selasa'),
        '3': _(u'Rabu'),
        '4': _(u'Kamis'),
        '5': _(u'Jumat'),
        '6': _(u'Sabtu'),
        '7': _(u'Minggu'),
    }
    hari = models.CharField(max_length=1, choices=tuple(sorted(DAY_OF_THE_WEEK.items())))
    jam_mulai = models.TimeField()
    matakuliah = models.ForeignKey('SKMengajar', on_delete=models.CASCADE)
    jam_selesai = models.TimeField(default='00:00:00', blank=True)
    ruang = models.ForeignKey(Ruang, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('hari', 'jam_mulai', 'ruang',)
        verbose_name = 'Jadwal kuliah'
        verbose_name_plural = 'Jadwal-jadwal kuliah'
        ordering = ['hari']

    def __str__(self):
        return '{} jam {} ruang {}'.format(self.hari, self.jam_mulai, self.ruang)

    def save(self, *args, **kwargs):
        self.matakuliah.terjadwal = True
        self.matakuliah.save()
        super(JadwalKuliah, self).save(*args, **kwargs)

    def get_hari(self):
        return self.DAY_OF_THE_WEEK[self.hari]
