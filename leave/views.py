from django.shortcuts import render,get_object_or_404
from .forms import RequestForm
from .models import Request
from django.utils import timezone
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings


# Create your views here.

def about(request):
    return render(request, 'leave/about.html',{})

def contact(request):
    return render(request, 'leave/contact.html',{})


def request_list(request):
    print(Request.objects.all)
    requests = Request.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'leave/request_list.html', {'requests': requests})

@login_required
def request_new(request):
    if request.method == "POST":
        # import pdb; pdb.set_trace()
        form = RequestForm(request.POST)
        if form.is_valid():
            requests = form.save(commit=False)
            requests.student = request.user
            requests.created_date = timezone.now()
            # send_mail(requests.subject, requests.description, settings.EMAIL_HOST_USER,
            # [requests.parent_email], fail_silently=False)
            requests.save()
            return redirect('request_detail', pk=requests.pk)
    else:
        form = RequestForm()
    return render(request, 'leave/request_edit.html', {'form': form})


def request_detail(request, pk):
    requests = get_object_or_404(Request, pk=pk)
    return render(request, 'leave/request_detail.html', {'requests': requests})

@login_required
def request_edit(request, pk):
    requests = get_object_or_404(Request, pk=pk)
    if request.method == "POST":
        form = RequestForm(request.POST, instance=requests)
        if form.is_valid():
            requests = form.save(commit=False)
            requests.student = request.user
            requests.created_date = timezone.now()
            requests.save()
            return redirect('request_detail', pk=requests.pk)
    else:
        form = RequestForm(instance=requests)
    return render(request, 'leave/request_edit.html', {'form': form})

def confirm(request, pk):
    requests = get_object_or_404(Request, pk=pk)
    if requests.perm:
        send_mail(requests.subject, requests.description, settings.EMAIL_HOST_USER,
        [requests.roll+'@iiita.ac.in'], fail_silently=False)

'''def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    to_email = request.POST.get('parent_email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, 'abc@abc.com', ['admin@example.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')'''
