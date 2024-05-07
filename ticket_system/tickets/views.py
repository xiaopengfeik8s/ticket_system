from django.shortcuts import render
from .models import Ticket
from django.shortcuts import redirect, render
from .forms import TicketForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import Ticket
from .forms import TicketForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import TicketForm
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
import sys


def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})

class TicketEditView(PermissionRequiredMixin, View):
    model = Ticket
    form_class = TicketForm
    permission_required = 'tickets.change_ticket'
    # ...更多视图方法，如get, post等...

def ticket_edit(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'tickets/ticket_form.html', {'form': form})

def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.delete()
    return redirect('ticket_list')



   

@login_required
def ticket_status_update(request, pk, status):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.status = status
    ticket.save()
    # 在这里可以加上发送通知的代码
    print(f'Notice: Ticket {ticket.pk} status has been updated to {ticket.status}.', file=sys.stderr)
    return redirect('ticket_list')