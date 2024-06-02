from django.shortcuts import render
from .forms import AddressForm,PenggunaForm,ContentForm,SearchPengguna
from .models import Pengguna
from django.http import JsonResponse


# Create your views here.
def set_data_entry(request):
    form = AddressForm()
    context  ={
        'form':form,
    }
    return render(request, 'data_entry\data_entry_1.html',context)

    
def set_pengguna(request):
    list_pengguna = Pengguna.objects.all().order_by('-id')
    context = None
    form = PenggunaForm(None)
    if request.method == "POST":
        form = PenggunaForm(request.POST)
        if form.is_valid():
            form.save()
            list_pengguna = Pengguna.objects.all().order_by('-id')
            context = {
              "form": form, 
              "list_pengguna": list_pengguna
              }
            return render(request, 'data_entry/data_entry_1.html', context)
    else:
        list_pengguna = Pengguna.objects.all().order_by('-id')
        context = {
            "form": form, 
            "list_pengguna": list_pengguna
            }
        return render(request, "data_entry/data_entry_1.html", context)
        

def view_pengguna(request):
    pass

def view_pengguna(request, id):
  try:
    pengguna = Pengguna.objects.get(pk=id)
    return render(request, 'data_entry/pengguna_detail.html', {'user_id': pengguna.id})
  except Pengguna.DoesNotExist:
    return JsonResponse({'error' : 'user not found '}, status = 404)


def get_pengguna_detail_api(request, user_id):
  try :
    pengguna = Pengguna.objects.get(pk=user_id)
    data = {
      'email' : pengguna.email,
      'address_1' : pengguna.address_1,
      'address_2' : pengguna.address_2,
      'city' : pengguna.city,
      'state' : pengguna.state,
      'zip_code' : pengguna.zip_code,
      'tanggal_join' : pengguna.tanggal_join.strftime('%Y-%m-%d'),
    }
    return JsonResponse(data)
  except Pengguna.DoesNotExist:
    return JsonResponse({'error' : 'user not found'}, status=404)

def set_content(request):
  form = ContentForm(None)
  if request.method =='POST':
    form = ContentForm(request.POST)
    if form.is_valid():
      form.save()
      list_pengguna = Pengguna.objects.all().order_by('-id')
      context = {
        "form": form, 
        "list_pengguna": list_pengguna
      }
      return render(request, 'data_entry/content.html', context)
  else :
    context = {
      "form" : form,
    }
    return render(request, 'data_entry/content.html', context)


def search_pengguna(request):
    pesan = None
    tampil = None
    form = None
    listpengguna = None
    status = None  # Define status variable
    if request.method == "POST":
        form = SearchPengguna(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            listpengguna = Pengguna.objects.filter(state=state)
            if not listpengguna:
                pesan = "Data Pengguna tidak ditemukan"
                status = True  # Assign a value to status
            else:
                tampil = True
    else:
        form = SearchPengguna()
    
    context = {
        'form': form,
        'tampil': tampil,
        'pesan': pesan,
        'listpengguna': listpengguna,
        'status': status,  # Include status in the context
    }
    return render(request, 'data_entry/list_pengguna.html', context=context)