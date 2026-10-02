from django.contrib import admin
from .models import Jurnal

@admin.register(Jurnal)
class JurnalAdmin(admin.ModelAdmin):
    list_display = ('nama_kegiatan', 'kategori', 'tanggal', 'created_at')
    list_filter = ('kategori', 'tanggal')
    search_fields = ('nama_kegiatan', 'catatan')