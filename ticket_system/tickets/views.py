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

from django.core.paginator import Paginator
from .forms import CommentForm
from django.contrib.auth.models import User

@login_required
def ticket_list(request):
    status_query = request.GET.get('status')
    assigned_query = request.GET.get('assigned_to')
    
    tickets = Ticket.objects.all()
    if status_query:
        tickets = tickets.filter(status=status_query)
    if assigned_query:
        try:
            user = User.objects.get(username=assigned_query)
            tickets = tickets.filter(assigned_to=user)
        except User.DoesNotExist:
            # 如果没有找到用户，则传回空的查询集
            tickets = Ticket.objects.none()

    paginator = Paginator(tickets, 10)  # 每页显示10个工单
    page = request.GET.get('page')
    tickets = paginator.get_page(page)

    archived_query = request.GET.get('archived')
    if archived_query is not None:
        tickets = tickets.filter(archived=archived_query == 'True')
       
# 获取所有标签的独特列表
    labels = Ticket.objects.values_list('labels', flat=True).distinct()
    
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            return redirect(request.path)
    else:
        comment_form = CommentForm()

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comment_form': comment_form,
        'comments': ticket.comments.all()
    })

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

@login_required
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
    print("Entering ticket_status_update view function.", file=sys.stderr)
    ticket = get_object_or_404(Ticket, pk=pk)
    print(f"Ticket with pk={pk} fetched successfully.", file=sys.stderr)
    ticket.status = status
    ticket.save()
    # 在这里可以加上发送通知的代码
    print(f'Notice: Ticket {ticket.pk} status has been updated to {ticket.status}.', file=sys.stderr)
    print("Redirecting to ticket_list.", file=sys.stderr)
    return redirect('ticket_list')