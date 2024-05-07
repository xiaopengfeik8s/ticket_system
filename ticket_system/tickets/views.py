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
from .forms import CommentForm
from .models import Ticket, Comment
from django.db.models import Count
from django.db.models import Count, F, Avg, DurationField, ExpressionWrapper
import json
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def ticket_list(request):
    status_query = request.GET.get('status')
    assigned_query = request.GET.get('assigned_to')
    archived_query = request.GET.get('archived')
    
    tickets = Ticket.objects.all()
    
    if status_query:
        tickets = tickets.filter(status=status_query)
    if assigned_query:
        tickets = tickets.filter(assigned_to__username=assigned_query)
    if archived_query is not None:
        tickets = tickets.filter(archived=archived_query == 'True')
    
    # Paginate after all filters are applied
    paginator = Paginator(tickets, 10)  # Show 10 tickets per page
    page = request.GET.get('page')
    tickets_page = paginator.get_page(page)

    labels = Ticket.objects.values_list('labels', flat=True).distinct()
    
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets_page, 'labels': labels})


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


    # 这里处理评论的提交
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # 创建并保存新的评论
            new_comment = comment_form.save(commit=False)
            new_comment.ticket = Ticket.objects.get(pk=pk)
            new_comment.author = request.user  # 确保 request.user 是当前登录用户
            new_comment.save()
            # 重定向回工单详情页面
            return redirect('ticket_detail', pk=pk)
    else:
        comment_form = CommentForm()

    # 将评论表单传递给模板
    return render(request, 'tickets/ticket_detail.html', {
        'ticket': Ticket.objects.get(pk=pk),
        'comment_form': comment_form,
        'comments': Comment.objects.filter(ticket__pk=pk),
        # ... 其他上下文 ...
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

@login_required
def ticket_archive(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.archived = True
    ticket.save()
    return redirect('ticket_list')  # 或者重定向到其他页面，如工单详情页

@login_required
def dashboard(request):
    total_tickets = Ticket.objects.count()
    status_new = Ticket.objects.filter(status='new').count()
    status_in_progress = Ticket.objects.filter(status='in_progress').count()
    status_resolved = Ticket.objects.filter(status='resolved').count()  # 假设 'resolved' 是解决状态
    avg_resolve_time = Ticket.objects.filter(status='resolved').annotate(
        resolve_time=ExpressionWrapper(F('updated_at') - F('created_at'), 
        output_field=DurationField())
    ).aggregate(average=Avg('resolve_time'))
    
    context = {
        'total_tickets': total_tickets,
        'status_new': status_new,
        'status_in_progress': status_in_progress,
        'status_resolved': status_resolved,
        'avg_resolve_time': avg_resolve_time['average'] if avg_resolve_time['average'] is not None else 'N/A',
        # 更多上下文信息
    }
    return render(request, 'tickets/dashboard.html', context)

@require_POST
def ticket_comment(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = get_object_or_404(Ticket, pk=pk)
            comment.author = request.user
            comment.save()
            return JsonResponse({
              'success': True,
              'author': comment.author.username,
              'text': comment.text,
            })
        else:
            return JsonResponse({
              'success': False,
              'error': 'Invalid form submission.',
            })
    return JsonResponse({'success': False, 'error': 'Invalid request'})