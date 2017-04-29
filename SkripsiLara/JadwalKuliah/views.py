from itertools import chain

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from SkripsiLara.JadwalKuliah.models import Jadwal


# Create your views here.

def index(request):
    jadwal = Jadwal.objects.all()
    return render(request, 'index_table.html', {'jadwal': jadwal})


def mobile(request):
    dosen = request.GET.get('dosen', '')
    kelas = request.GET.get('kelas', '')
    jdl = Jadwal.objects.none().values()
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
    dosen1 = Jadwal.objects.values_list('Dosen_1', flat=True).values()
    dosen2 = Jadwal.objects.values_list('Dosen_2', flat=True).values()
    dosen3 = Jadwal.objects.values_list('Dosen_3', flat=True).values()
    jdl = list(chain(dosen1, dosen2, dosen3))
    return JsonResponse(android_json(jdl))


def kelas(request):
    jdl = Jadwal.objects.values_list('Kelas', flat=True).values()
    return JsonResponse(android_json(jdl))
