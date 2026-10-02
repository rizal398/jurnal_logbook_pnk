from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ProfilMahasiswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    nim = models.CharField(max_length=30, blank=True, null=True, verbose_name="NIM")
    nama_lengkap = models.CharField(max_length=150, blank=True, null=True)
    pembimbing_dosen = models.CharField(max_length=150, blank=True, null=True, verbose_name="Pembimbing Lapangan Dosen")
    pembimbing_mitra = models.CharField(max_length=150, blank=True, null=True, verbose_name="Pembimbing Lapangan Mitra")
    tempat_magang = models.CharField(max_length=200, blank=True, null=True, verbose_name="Magang (Tempat/Instansi)")
    waktu_pelaksanaan = models.CharField(max_length=100, blank=True, null=True, verbose_name="Waktu Pelaksanaan")
    jumlah_sks = models.CharField(max_length=20, default="20", blank=True, null=True, verbose_name="Jumlah Konversi SKS")
    program_studi = models.CharField(max_length=100, blank=True, null=True, verbose_name="Program Studi")
    jurusan = models.CharField(max_length=100, blank=True, null=True, verbose_name="Jurusan")
    tahun = models.CharField(max_length=10, default="2026", blank=True, null=True)

    def __str__(self):
        return f"Profil {self.nama_lengkap or self.user.username}"


class Jurnal(models.Model):
    KATEGORI_CHOICES = [
        ('Website', 'Website'),
        ('Meeting', 'Meeting'),
        ('Personal', 'Personal'),
        ('Lainnya', 'Lainnya'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jurnal_set', null=True, blank=True)
    tanggal = models.DateField(default=timezone.now)
    jam_masuk = models.TimeField(default="08:00", verbose_name="Jam Masuk")
    jam_pulang = models.TimeField(default="16:00", verbose_name="Jam Pulang")
    nama_kegiatan = models.CharField(max_length=200)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, default='Personal')
    catatan = models.TextField(verbose_name="Uraian Kerja")
    foto_dokumentasi = models.ImageField(upload_to='jurnal_fotos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['tanggal', 'created_at']

    def __str__(self):
        return f"{self.nama_kegiatan} - {self.tanggal}"