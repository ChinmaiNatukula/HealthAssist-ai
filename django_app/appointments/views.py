from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.user = request.user
            appt.save()
            messages.success(request, '✅ Appointment booked successfully! We will confirm shortly.')
            return redirect('my_appointments')
        else:
            messages.error(request, 'Please fill all required fields correctly.')
    else:
        form = AppointmentForm(initial={'name': request.user.get_full_name() or request.user.username})
    return render(request, 'appointments/book.html', {'form': form})


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments/list.html', {'appointments': appointments})
