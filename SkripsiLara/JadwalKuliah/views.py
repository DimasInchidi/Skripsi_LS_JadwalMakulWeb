from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from SkripsiLara.JadwalKuliah.models import JadwalKuliah as Jadwal, Dosen, Kelas


def index(request):
    jadwal = Jadwal.objects.all()
    return render(request, 'index_table.html', {'jadwal': jadwal})


def mobile(request):
    dosen = request.GET.get('dosen', '')
    kelas = request.GET.get('kelas', '')
    if not (dosen == kelas == ''):
        jdl = Jadwal.objects.filter(
            Q(
                matakuliah__dosen1__dosen=dosen
            ) | Q(
                matakuliah__dosen2__dosen=dosen
            ) | Q(
                matakuliah__dosen3__dosen=dosen
            ) | Q(
                matakuliah__kelas1__kelas=kelas
            ) | Q(
                matakuliah__kelas2__kelas=kelas
            ) | Q(
                matakuliah__kelas3__kelas=kelas
            ) | Q(
                matakuliah__kelas4__kelas=kelas
            ) | Q(
                matakuliah__kelas5__kelas=kelas
            )
        )
    elif len(dosen) > 0:
        jdl = Jadwal.objects.filter(
            Q(
                matakuliah__dosen1__dosen=dosen
            ) | Q(
                matakuliah__dosen2__dosen=dosen
            ) | Q(
                matakuliah__dosen3__dosen=dosen
            )
        )
    elif len(kelas) > 0:
        jdl = Jadwal.objects.filter(
            Q(
                matakuliah__kelas1__kelas=kelas
            ) | Q(
                matakuliah__kelas2__kelas=kelas
            ) | Q(
                matakuliah__kelas3__kelas=kelas
            ) | Q(
                matakuliah__kelas4__kelas=kelas
            ) | Q(
                matakuliah__kelas5__kelas=kelas
            )
        )
    else:
        jdl = Jadwal.objects.filter()
    return JsonResponse(to_json(jdl))


def to_json(data):
    list_result = {}
    n = 0
    for i in data:
        row = {
            'Hari': i.get_hari(),
            'Jam': i.get_jam(),
            'Ruang': i.ruang.ruang,
            'Matakuliah': i.matakuliah.matakuliah.matakuliah,
            'SKS': i.matakuliah.matakuliah.sks,
            'Kelas': i.matakuliah.get_kelas(),
            'Dosen': i.matakuliah.get_dosen(),
        }
        list_result[n] = row
        n += 1
    return list_result


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
