from django import forms
from django.contrib.auth.models import User
from .models import Jurnal, ProfilMahasiswa

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Minimal 8 karakter'
    }))
    konfirmasi_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ulangi password'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username / NIM'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap Mahasiswa'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@kampus.ac.id'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        konfirmasi = cleaned_data.get("konfirmasi_password")
        if password and konfirmasi and password != konfirmasi:
            self.add_error('konfirmasi_password', "Password tidak cocok!")
        return cleaned_data

class JurnalForm(forms.ModelForm):
    class Meta:
        model = Jurnal
        fields = ['tanggal', 'jam_masuk', 'jam_pulang', 'nama_kegiatan', 'kategori', 'catatan', 'foto_dokumentasi']
        widgets = {
            'tanggal': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'jam_masuk': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'jam_pulang': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'nama_kegiatan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Mengerjakan modul logbook'
            }),
            'kategori': forms.Select(attrs={
                'class': 'form-select',
            }),
            'catatan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tulis uraian kegiatan secara detail...'
            }),
            'foto_dokumentasi': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

class ProfilMahasiswaForm(forms.ModelForm):
    class Meta:
        model = ProfilMahasiswa
        fields = [
            'nim', 'nama_lengkap', 'tempat_magang', 'pembimbing_dosen',
            'pembimbing_mitra', 'waktu_pelaksanaan', 'jumlah_sks',
            'program_studi', 'jurusan',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'