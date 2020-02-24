from django.urls import path

from api.v1.views import *
from main.models import Schedule

urlpatterns = [
    path('groups/', GroupList.as_view(), name='groups'),
    path('schedule/fulltime/study/<int:group_id>',
         FullTimeScheduleAPI.as_view(schedule_type=Schedule.STUDY), name='schedule-study'),
    path('schedule/fulltime/session/<int:group_id>',
         FullTimeScheduleAPI.as_view(schedule_type=Schedule.SESSION), name='schedule-session'),
    path('schedule/extramural/study/<int:group_id>',
         ExtramuralScheduleAPI.as_view(schedule_type=Schedule.STUDY), name='schedule-study'),
    path('schedule/extramural/session/<int:group_id>',
         ExtramuralScheduleAPI.as_view(schedule_type=Schedule.SESSION), name='schedule-session')
]
