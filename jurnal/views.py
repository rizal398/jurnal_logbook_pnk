import io
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Jurnal, ProfilMahasiswa
from .forms import JurnalForm, ProfilMahasiswaForm, RegisterForm

# --- AUTENTIKASI ---
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Pendaftaran berhasil!")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# --- DASHBOARD & JURNAL ---
@login_required(login_url='login')
def dashboard(request):
    sekarang = timezone.now()

    if request.method == 'POST':
        form = JurnalForm(request.POST, request.FILES)
        if form.is_valid():
            jurnal = form.save(commit=False)
            jurnal.user = request.user  # Mengikat data ke akun yang sedang login
            jurnal.save()
            return redirect('dashboard')
    else:
        form = JurnalForm(initial={'tanggal': sekarang.date()})

    # Hanya hitung & ambil data milik user yang sedang aktif
    user_jurnal = Jurnal.objects.filter(user=request.user)
    
    total_jurnal = user_jurnal.count()
    bulan_ini = user_jurnal.filter(
        tanggal__year=sekarang.year,
        tanggal__month=sekarang.month
    ).count()
    hari_aktif = user_jurnal.values('tanggal').distinct().count()
    jurnal_terbaru = user_jurnal[:5]

    context = {
        'form': form,
        'total_jurnal': total_jurnal,
        'bulan_ini': bulan_ini,
        'hari_aktif': hari_aktif,
        'jurnal_list': jurnal_terbaru,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def profil(request):
    profil_mahasiswa, _ = ProfilMahasiswa.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfilMahasiswaForm(request.POST, instance=profil_mahasiswa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data profil berhasil disimpan.')
            return redirect('profil')
    else:
        form = ProfilMahasiswaForm(instance=profil_mahasiswa)

    user_jurnal = Jurnal.objects.filter(user=request.user)
    context = {
        'profil': profil_mahasiswa,
        'form': form,
        'total_jurnal': user_jurnal.count(),
        'hari_aktif': user_jurnal.values('tanggal').distinct().count(),
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def semua_jurnal(request):
    query = request.GET.get('q', '')
    kategori_terpilih = request.GET.get('kategori', '')

    daftar_jurnal = Jurnal.objects.filter(user=request.user)

    if query:
        daftar_jurnal = daftar_jurnal.filter(
            Q(nama_kegiatan__icontains=query) | Q(catatan__icontains=query)
        )

    if kategori_terpilih and kategori_terpilih != 'Semua':
        daftar_jurnal = daftar_jurnal.filter(kategori=kategori_terpilih)

    kategori_list = ['Semua', 'Website', 'Meeting', 'Personal', 'Lainnya']

    context = {
        'daftar_jurnal': daftar_jurnal,
        'query': query,
        'kategori_list': kategori_list,
        'kategori_terpilih': kategori_terpilih,
        'total_hasil': daftar_jurnal.count(),
    }
    return render(request, 'semua_jurnal.html', context)

@login_required(login_url='login')
def edit_jurnal(request, pk):
    jurnal = get_object_or_404(Jurnal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = JurnalForm(request.POST, request.FILES, instance=jurnal)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = JurnalForm(instance=jurnal)

    return render(request, 'edit_jurnal.html', {'form': form, 'jurnal': jurnal})

@login_required(login_url='login')
def hapus_jurnal(request, pk):
    jurnal = get_object_or_404(Jurnal, pk=pk, user=request.user)
    if request.method == 'POST':
        if jurnal.foto_dokumentasi:
            jurnal.foto_dokumentasi.delete(save=False)
        jurnal.delete()
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    return redirect('dashboard')
# ================= FUNGSI EXPORT PDF LOGBOOK =================
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Terjadi kesalahan saat membuat PDF", status=500)


@login_required(login_url='login')
def export_logbook_pdf(request):
    sekarang = timezone.now()
    bulan = int(request.GET.get('bulan', sekarang.month))
    tahun = int(request.GET.get('tahun', sekarang.year))

    profil, _ = ProfilMahasiswa.objects.get_or_create(user=request.user)

    logbook_list = Jurnal.objects.filter(
        user=request.user,
        tanggal__year=tahun,
        tanggal__month=bulan
    ).order_by('tanggal')

    daftar_nama_bulan = [
        '', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ]
    nama_bulan = daftar_nama_bulan[bulan]

    context = {
        'user': request.user,
        'profil': profil,
        'logbook_list': logbook_list,
        'nama_bulan': nama_bulan,
        'bulan': bulan,
        'tahun': tahun,
        'tgl_sekarang': sekarang,
    }

    response = render_to_pdf('logbook_pdf.html', context)
    if response and isinstance(response, HttpResponse) and response.status_code == 200:
        filename = f"Logbook_Magang_{profil.nim or request.user.username}_{nama_bulan}_{tahun}.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response

    return HttpResponse("Gagal membuat dokumen PDF.", status=500)