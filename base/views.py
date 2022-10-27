from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .models import User, Event, Submission
from .forms import SubmissionForm, CustomUserCreateForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from PIL import Image
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime, timedelta



def login_page(request):
    page = 'login'

    if request.method == 'POST':
        user = authenticate(email=request.POST['email'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            messages.info(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Email or Password is incorrect')
            return redirect('login')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def logout_page(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def register_page(request):
    page = 'register'
    form = CustomUserCreateForm()

    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created!')

            login(request, user)
            messages.success(request, 'User account was created!')
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context)


def home_page(request):
    users = User.objects.filter(subscriber=True)
    count_users = users.count()

    page = request.GET.get('page')
    paginator = Paginator(users, per_page=2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        users = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        users = paginator.page(page)


    pages = list(range(1, (paginator.num_pages + 1)))


    events = Event.objects.all()
    context = {'users': users, 'events': events, 'count_users': count_users, 'paginator': paginator, 'pages': pages}
    return render(request, 'home.html', context)


def user_page(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def account_page(request):
    user = request.user

    # img = user.avatar
    # img = Image.open(user.avatar)
    # new_size = (10, 10)
    # img = img.resize(new_size)
    #
    # user.avatar = img
    # user.save()

    context = {'user': user}
    return render(request, 'account.html', context)


@login_required(login_url='login')
def edit_account(request):
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        # img = Image.open(request.FILES.get('avatar'))
        # new_size = (10, 10)
        # img = img.resize(new_size)
        # request.FILES['avatar'] = img
        # img = Image.open(user.avatar)
        # new_size = (10, 10)
        # img = img.resize(new_size)

        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'user_form.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            new_password = make_password(password1)
            request.user.password = new_password
            request.user.save()
            messages.success(request, "Password was changed")
            return redirect('account')
        else:
            messages.error(request, "Please, type same passwords for all fields!")
            return redirect('change-password')

    context = {}
    return render(request, 'change_password.html', context)


def event_page(request, pk):
    event = Event.objects.get(id=pk)

    present = datetime.now().timestamp()
    deadline = event.registration_deadline.timestamp()
    past_deadline = (present > deadline)

    registered = False
    submitted = False

    if request.user.is_authenticated:
        registered = request.user.events.filter(id=event.id).exists()
        submitted = Submission.objects.filter(participant=request.user, event=event).exists()
    context = {'event': event, 'past_deadline': past_deadline, 'registered': registered, 'submitted': submitted}
    return render(request, 'event.html', context)


@login_required(login_url='login')
def register_confirm(request, pk):
    event = Event.objects.get(id=pk)
    context = {'event': event}

    if request.method == 'POST':
        event.participants.add(request.user)
        return redirect('event', pk=event.id)

    return render(request, 'event_confirmation.html', context)


@login_required(login_url='login')
def project_submission(request, pk):
    event = Event.objects.get(id=pk)
    form = SubmissionForm()

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()

            return redirect('account')
    context = {'event': event, 'form': form}
    return render(request, 'submit_form.html', context)


# Add owner authentication
@login_required(login_url='login')
def update_submission(request, pk):
    submission = Submission.objects.get(id=pk)

    if request.user != submission.participant:
        return HttpResponse('You cant be here!!')

    event = submission.event
    form = SubmissionForm(instance=submission)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form, 'event': event}
    return render(request, 'submit_form.html', context)
