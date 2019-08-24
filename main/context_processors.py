from smiap.settings import CONFIG


def app_processor(request):
    nav_items = [
        {"id": "home", "title": "Главная", "link": "/", "subitems": []},
        {"id": "about", "title": "О кафедре", "link": "/about/intro", "subitems": [
            {"id": "intro", "title": "Введение", "link": "/about/intro"},
            {"id": "history", "title": "История кафедры", "link": "/about/history"},
            {"id": "staff", "title": "Сотрудники кафедры", "link": "/about/staff"},
            {"id": "contacts", "title": "Контакты", "link": "/about/contacts"}
        ]},

        {"id": "materials", "title": "Материалы", "link": "/materials/news", "subitems": [
            {"id": "news", "title": "Новости", "link": "/materials/news"},
            {"id": "publications", "title": "Публикации", "link": "/materials/publications"},
            {"id": "tutorials", "title": "Учебные пособия", "link": "/materials/tutorials"},
            {"id": "timetable", "title": "Расписания занятий", "link": "/materials/timetable"},
            # {"id": "session", "title": "Расписание сессии заочной формы", "link": "/materials/session"}
        ]},

        {"id": "programs", "title": "Программы", "link": "/programs", "subitems": []},
        {"id": "conferences", "title": "Конференции", "link": "/conferences", "subitems": [
            # {"id": "gagarin", "title": "Гагаринские чтения", "link": "gagarin"}
        ]},

        {"id": "abiturients", "title": "Абитуриентам", "link": "/abiturients", "subitems": []},
    ]

    if request.user and request.user.is_authenticated:
        last_item = {"id": "username", "title": request.user.username, "link": None, "subitems": [
            {"id": "logout", "title": "Выйти", "link": "/auth/logout?next={}".format(request.path), "subitems": []}
        ]}
    else:
        last_item = {"id": "login", "title": "Войти",
                     "link": "/auth/login?next={}".format(request.path), "subitems": []}
    nav_items.append(last_item)

    if request.path == '/':
        active_items = 'home'
    else:
        active_items = request.path.split('/')

    return {
        'APP_TITLE': CONFIG.get('brand', 'name'),
        'NAV_ITEMS': nav_items,
        'ACTIVE_ITEMS': active_items
    }
