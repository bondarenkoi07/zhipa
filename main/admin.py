from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.forms import Form
from django.urls import path

from main.models import *
from main.types import Degree
from main.views.admin.couple_publications import SeveralPublicationsView


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'regalia', 'leader', 'lecturer', 'hide')
    list_filter = ('leader', 'lecturer', 'hide')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'hidden', 'author')
    list_display_links = ('title',)
    list_filter = ('hidden',)
    exclude = ('author',)

    def save_model(self, request, obj, form: Form, change):
        if form.is_valid():
            user = request.user
            obj.author = user
        super().save_model(request, obj, form, change)


class GroupCourseFilter(admin.SimpleListFilter):
    title = 'Course'
    parameter_name = 'courses'

    def lookups(self, request, model_admin):
        courses = Group.objects.distinct('course').only('course')
        return ((c.course, f'{c.course} курс') for c in courses)

    def queryset(self, request, queryset: QuerySet):
        if self.value():
            value = int(self.value())
            return queryset.filter(semester__gte=value * 2 - 1,
                                   semester__lte=value * 2)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('degree', 'course', '-study_form', 'name')
    list_display = ('name', 'study_form', 'get_degree', 'semester', 'course', 'schedule_version')
    list_filter = ('study_form', GroupCourseFilter, 'schedule_version')

    def get_degree(self, obj: Group):
        return Degree(obj.degree).name.casefold().capitalize()

    get_degree.short_description = 'Degree'
    get_degree.admin_order_field = 'degree'


@admin.register(User)
class SmiapUserAdmin(UserAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


class TeacherIsStuffFilter(admin.SimpleListFilter):
    title = 'Teacher is staff'
    parameter_name = 'is_staff'

    def lookups(self, request, model_admin):
        return (
            ('Y', 'Yes'),
            ('N', 'No')
        )

    def queryset(self, request, queryset: QuerySet):
        if self.value():
            value = self.value() == 'Y'
            return queryset.filter(staff__isnull=not value)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'staff')
    list_filter = (TeacherIsStuffFilter,)


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'week')
    inlines = (ItemInline,)
    list_filter = ('week',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'day', 'starts_at', 'ends_at')
    list_filter = ('type', 'starts_at', 'ends_at')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    change_list_template = 'admin/publications/list.html'
    list_display = ('pk', 'name', 'place', 'authors')
    list_display_links = ('name',)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add-couple/', SeveralPublicationsView.as_view())
        ]
        return my_urls + urls
