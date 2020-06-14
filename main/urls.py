from django.urls import path, register_converter
from django.views.generic import RedirectView
from django.contrib.flatpages import views

from news import converters
from .views import *

register_converter(converters.FourDigitYearConverter, 'yyyy')
register_converter(converters.TwoDigitConverter, 'mm')
register_converter(converters.TwoDigitConverter, 'dd')
register_converter(converters.ActivateCodeConverter, 'key')

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('important-message', views.flatpage, {'url': '/important-message'}, name='important-message'),

    path('abiturients/info', views.flatpage, {'url': '/abiturients/info'}, name='abiturients'),
    path('abiturients/programs', views.flatpage, {'url': '/abiturients/programs'}, name='programs'),

    path('about', RedirectView.as_view(pattern_name='intro')),
    path('about/intro', views.flatpage, {'url': '/about/intro'}, name='intro'),

    path('about/conferences', views.flatpage, {'url': '/about/conferences'}, name='conferences'),
    path('about/history', HistoryView.as_view(), name='history'),
    path('about/history/page<int:number>', HistoryView.as_view(), name='history'),
    path('about/staff', StaffView.as_view(), name='staff'),
    path('about/contacts', views.flatpage, {'url': '/about/contacts'}, name='contacts'),

    path('materials/tutorials', views.flatpage, {'url': '/materials/tutorials'}, name='tutorials'),
    path('materials/publications', PublicationView.as_view(), name='publications'),

    path('f/<str:link>', LinkView.as_view(), name='short-file'),

    # Redirects from old url.
    path('programs', RedirectView.as_view(pattern_name='programs')),
    path('conferences', RedirectView.as_view(pattern_name='conferences')),
    path('abiturients', RedirectView.as_view(pattern_name='abiturients')),
    path('materials', RedirectView.as_view(pattern_name='news:news-list')),
    path('materials/timetable', RedirectView.as_view(pattern_name='schedule:timetable')),
    path('materials/timetable/extramural', RedirectView.as_view(pattern_name='schedule:timetable-extramural')),

    # TODO
    # Making registration backend by django-registration
    # path('auth/login', SmiapLoginView.as_view(), name='login'),
    # path('auth/logout', SmiapLogoutView.as_view(), name='logout'),
    # path('auth/register/', SmiapRegistrationView.as_view(), name='registration'),
    # path('auth/register/complete',
    #      TemplateView.as_view(template_name='auth/registration_complete.html'), name='registration_complete'),
    # path('auth/activate/<key:activation_key>/', SmiapActivationView.as_view(), name='activation'),
    # path('auth/complete',
    #      TemplateView.as_view(template_name='auth/activation_complete.html'), name='activation_complete'),
]
