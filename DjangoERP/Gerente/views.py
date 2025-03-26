from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def gerente_view(request):
    if request.user.rol != 'Gerente':
        return redirect('usuarios:logistics')
    return render(request, 'Gerente/gerente.html', {})