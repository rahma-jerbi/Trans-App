from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

def frontpage(request):
    return render(request, 'core/frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})

@login_required
def redirect_to_transcriptions(request):
  # Removed unnecessary redirection logic
  return render(request, 'transcription/transcriptions.html')

@login_required
def redirect_to_extract_informations(request):
  # Removed unnecessary redirection logic
  return render(request, 'transcription/extract_informations.html')
