from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from SkripsiLara.JadwalKuliah.models import JadwalKuliah as Jadwal, Dosen, Kelas


def index(request):
    jadwal = Jadwal.objects.all()
    return render(request, 'index_table.html', {'jadwal': jadwal})


def mobile(request):
    dosen = request.GET.get('dosen', '')
    kelas = request.GET.get('kelas', '')
    if len(dosen) > 0 & len(kelas) > 0:
        jdl = Jadwal.objects.filter(Q(Dosen_1=dosen) | Q(Dosen_2=dosen) | Q(Dosen_3=dosen) | Q(Kelas=kelas)).values()
    elif len(dosen) > 0:
        jdl = Jadwal.objects.filter(Q(Dosen_1=dosen) | Q(Dosen_2=dosen) | Q(Dosen_3=dosen)).values()
    elif len(kelas) > 0:
        jdl = Jadwal.objects.filter(Kelas=kelas).values()
    elif dosen == kelas == '':
        jdl = Jadwal.objects.filter().values()
    return JsonResponse(android_json(jdl))


def android_json(data):
    list_result = {}
    for i in range(data.__len__()):
        list_result[i] = data[i]
    return list_result


def dosen(request):
    data_dosen = list(Dosen.objects.values_list('dosen', flat=True).distinct())
    return JsonResponse(android_json(data_dosen))


def kelas(request):
    data_kelas = list(Kelas.objects.values_list('kelas', flat=True).distinct())
    return JsonResponse(android_json(data_kelas))
