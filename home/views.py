from unicodedata import name
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from .models import Entry, Category, Topic, Comment
from .forms import EntryForm, NewTopicForm, NewUserForm, NewCommentForm, BookLessonForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import Group, User, Permission
from collections import namedtuple
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError


def index(request):
    context = {}
    return render(request, 'home/index.html', context)


def register(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Members')
            user.groups.add(group)
            auth_login(request, user)
            return redirect("home")
    return render(request=request, template_name="home/register.html", context={"register_form": form})


def login(request):
    form = AuthenticationForm()
    context = {}
    context['login_form'] = form
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("home")
    return render(request=request, template_name="home/login.html", context=context)


def logout(request):
    auth_logout(request)
    return redirect('login')


def topic_new(request, category_pk):
    context = {}
    form_name = NewTopicForm(prefix='new_topic_name')
    form_comment = NewCommentForm(prefix='new_topic_comment')
    context['category'] = get_object_or_404(Category, pk=category_pk)
    context['path'] = namedtuple('Page', 'page pageurl category topic')(
        'Forum', 'forum', context['category'], 'New Topic')
    if request.method == "POST":
        form_topic = NewTopicForm(request.POST, prefix='new_topic_name')
        form_comment = NewCommentForm(request.POST, prefix='new_topic_comment')
        if form_topic.is_valid() and form_comment.is_valid():
            topic = form_topic.save(commit=False)
            topic.category = context['category']
            topic.author = request.user
            topic.save()
            comment = form_comment.save(commit=False)
            comment.author = request.user
            comment.date = timezone.now()
            comment.topic = topic
            comment.save()
            return redirect('topic', category_pk=category_pk, topic_pk=topic.pk)
    context['form_name'] = form_name
    context['form_comment'] = form_comment
    return render(request, 'home/topic_new.html', context)


def entry_new(request):
    form = EntryForm()
    if request.method == "POST":
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('entry_detail', entry_pk=post.pk)
    return render(request, 'home/entry_edit.html', {'form': form})


def book_lesson(request):
    form = BookLessonForm()
    context = {}
    context['form'] = form
    context['path'] = namedtuple('Page', 'page pageurl')(
        'Book a lesson', 'book_lesson')
    if request.method == "POST":
        form = BookLessonForm(request.POST)
        if form.is_valid():
            booking = form.save()
            booking.date = timezone.now()
            messages.info(request, 'We will call you soon')
    return render(request, 'home/book_lesson.html', context)


def blog(request):
    context = {}
    context['path'] = namedtuple('Page', 'page pageurl')('Blog', 'blog')
    context['entries'] = Entry.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date').reverse()



    return render(request, 'home/blog.html', context)


def entry_detail(request, entry_pk):
    context = {}
    context['path'] = namedtuple('Page', 'page pageurl entry')(
        'Blog', 'blog', request.path.split('/')[-2])
    context['entry'] = get_object_or_404(Entry, pk=entry_pk)

    #context['entry'].text = context['entry'].text.replace('&', "&amp;")
    #context['entry'].text = context['entry'].text.replace('<', "&lt;")
    #context['entry'].text = context['entry'].text.replace('>', "&gt;")
    #context['entry'].text = context['entry'].text.replace('"', "&quot;")
    #context['entry'].text = context['entry'].text.replace("'", "&#039;");

    context['entry'].text = context['entry'].text.replace('\n','&Tab;')
    #context['entry'].text = context['entry'].text.replace(' ','&nbsp;')


    return render(request, 'home/entry_detail.html', context)


def forum(request):
    context = {}
    context['path'] = namedtuple('Page', 'page pageurl')('Forum', 'forum')
    context['categories'] = Category.objects.all()
    return render(request, 'home/forum.html', context)


def category(request, category_pk):
    context = {}
    context['category'] = get_object_or_404(Category, pk=category_pk)
    context['path'] = namedtuple('Page', 'page pageurl category')(
        'Forum', 'forum', context['category'].name)
    context['topics'] = Topic.objects.filter(category=category_pk)
    return render(request, 'home/category.html', context)


def topic(request, category_pk, topic_pk):
    context = {}
    context['category'] = get_object_or_404(Category, pk=category_pk)
    context['topic'] = get_object_or_404(Topic, pk=topic_pk)

    context['path'] = namedtuple('Page', 'page pageurl category topic')(
        'Forum', 'forum', context['topic'].category, context['topic'].name)
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.date = timezone.now()
            comment.topic = context['topic']

            comment.save()
    form = NewCommentForm()
    context['form'] = form
    context['comments'] = Comment.objects.filter(
        topic=context['topic']).order_by('date')
    for every in context['comments']:
        #every.text = every.text.replace('&', "&amp;")
        #every.text = every.text.replace('<', "&lt;")
        #every.text = every.text.replace('>', "&gt;")
        #every.text = every.text.replace('"', "&quot;")
        #every.text = every.text.replace("'", "&#039;");

        every.text = every.text.replace('\n','&Tab;')
        #every.text = every.text.replace(' ','&nbsp;')

    return render(request, 'home/topic.html', context)


def contact(request):
    context = {}
    context['path'] = namedtuple('Page', 'page pageurl')('Contact', 'contact')
    return render(request, 'home/contact.html', context)


def about(request):
    context = {}
    context['path'] = namedtuple('Page', 'page pageurl')('About', 'about')
    return render(request, 'home/about.html', context)
