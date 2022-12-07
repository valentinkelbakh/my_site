from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.generic import RedirectView
urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('home/', views.index, name='home'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('book_lesson/', views.book_lesson, name='book_lesson'),
    path('forum/', views.forum, name='forum'),
    path('forum/category/<int:category_pk>/', views.category, name='category'),
    path('forum/category/<int:category_pk>/topic/<int:topic_pk>/',views.topic, name='topic'),
    path('forum/category/<int:category_pk>/topic/new/',views.topic_new, name='topic_new'),
    path('blog/entry/<int:entry_pk>/', views.entry_detail, name='entry_detail'),
    path('blog/entry/new/', views.entry_new, name='entry_new'),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path('logout/', views.logout, name='logout'),
] + static(settings.IMG_URL, document_root=settings.IMG_ROOT)
