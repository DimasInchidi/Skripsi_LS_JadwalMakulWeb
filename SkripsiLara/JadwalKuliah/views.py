from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from JadwalKuliah.models import Jadwal


# Create your views here.

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
