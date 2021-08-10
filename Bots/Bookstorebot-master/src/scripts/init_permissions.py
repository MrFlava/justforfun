from src.models import DBSession, Permission, User


# noinspection SpellCheckingInspection
def main():
    """"""

    """-----------------Default-----------------"""
    # menus
    Permission.create('start_menu_access', {'en': 'Access to "Start" menu', 'ru': 'Доступ к меню "Старт"', 'uk': 'Доступ до меню "Старт"'})
    Permission.create('profile_menu_access', {'en': 'Access to "Profile" menu', 'ru': 'Доступ к меню "Профиль"', 'uk': 'Доступ до меню "Профіль"'})
    Permission.create('change_language_menu_access', {'en': 'Access to "Change language" menu', 'ru': 'Доступ к меню "Сменить язык"', 'uk': 'Доступ до меню "Змінити мову"'})
    Permission.create('marketplace_menu_access', {'en': 'Access to "Marketplace" menu', 'ru': 'Доступ к меню "Маркет"', 'uk': 'Доступ до меню "Маркет"'})
    Permission.create('price_analysis_menu_access', {'en': 'Access to "Price analysis" menu', 'ru': 'Доступ к меню "Аназлиз цен"', 'uk': 'Доступ до меню "Аналіз цін"'})
    Permission.create('make_query_menu_access', {'en': 'Access to "Make query" menu', 'ru': 'Доступ к меню "Сделать запрос"', 'uk': 'Доступ до меню "Зробити запит"'})
    Permission.create('queries_history_menu_access', {'en': 'Access to "Queries history" menu', 'ru': 'Доступ к меню "История запросов"', 'uk': 'Доступ до меню "Історія запитів"'})
    Permission.create('buy_queries_menu_access', {'en': 'Access to "Buy queries" menu', 'ru': 'Доступ к меню "Купить запросы"', 'uk': 'Доступ до меню "Придбати запити"'})
    Permission.create('operators_menu_access', {'en': 'Access to "Operators" menu', 'ru': 'Доступ к меню "Операторы"', 'uk': 'Доступ до меню "Оператори"'})

    # actions
    # Permission.create('allow_download_ticket', {'en': 'Allow download ticket', 'ru': 'Разрешить скачивать билет', 'uk': 'Дозволити завантажувати квиток'})
    """-----------------Privileged-----------------"""
    # menus
    Permission.create('admin_menu_access', {'en': 'Access to "Admin" menu', 'ru': 'Доступ к меню "Админ"', 'uk': 'Доступ до меню "Адмін"'})
    Permission.create('permissions_menu_access', {'en': 'Access to "Permissions" menu', 'ru': 'Доступ к меню "Права"', 'uk': 'Доступ до меню "Права"'})
    Permission.create('distribution_menu_access', {'en': 'Access to "Distribution" menu', 'ru': 'Доступ к меню "Рассылка"', 'uk': 'Доступ до меню "Розсилка"'})
    Permission.create('operator_groups_menu_access', {'en': 'Access to "Operator group" menu', 'ru': 'Доступ к меню "Группы операторов"', 'uk': 'Доступ до меню "Групи операторів"'})

    # operator groups menu
    Permission.create('operator_groups_menu_access', {'en': 'Access to "Operator group" menu', 'ru': 'Доступ к меню "Группы операторов"', 'uk': 'Доступ до меню "Групи операторів"'})
    Permission.create('add_group_access', {'en': 'Access to "Add group" menu', 'ru': 'Доступ к меню "Добавить группу"', 'uk': 'Доступ до меню "Додати групу"'})
    Permission.create('edit_group_access', {'en': 'Access to "Edit group" menu', 'ru': 'Доступ к меню "Редактировать группу"', 'uk': 'Доступ до меню "Редагувати групу"'})
    Permission.create('group_translations_menu_access', {'en': 'Access to "Translations group" menu', 'ru': 'Доступ к меню "Группа переводов"', 'uk': 'Доступ до меню "Переклади групи"'})
    Permission.create('add_translations_group_menu_access', {'en': 'Access to "Add translations group" menu', 'ru': 'Доступ к меню "Добавить группу переводов"', 'uk': 'Доступ до меню "Додати групу перекладів"'})
    Permission.create('edit_translations_group_menu_access', {'en': 'Access to "Edit translations group" menu', 'ru': 'Доступ к меню "Редактировать группу переводов"', 'uk': 'Доступ до меню "Редагувати групу перекладів"'})
    Permission.create('allow_remove_groups', {'en': 'Allow delete gorups', 'ru': 'Разрешить удаление групп', 'uk': 'Дозволити видалення груп'})
    Permission.create('allow_remove_translations_group', {'en': 'Allow delete group translations', 'ru': 'Разрешить удалять переводы груп', 'uk': 'Дозволити видалення перекладу груп'})

    # group entries menu
    Permission.create('group_entries_menu_access', {'en': 'Access to "Entries group" menu', 'ru': 'Доступ к меню "Группа записей"', 'uk': 'Доступ до меню "Записи групи"'})
    Permission.create('add_entry_access', {'en': 'Access to "Add entry" menu', 'ru': 'Доступ к меню "Добавить запись"', 'uk': 'Доступ до меню "Додати запис"'})
    Permission.create('edit_entry_access', {'en': 'Access to "Edit entry" menu', 'ru': 'Доступ к меню "Редактировать запись"', 'uk': 'Доступ до меню "Редагувати запис"'})
    Permission.create('entry_translations_menu_access', {'en': 'Access to "Translations entry" menu', 'ru': 'Доступ к меню "Группа записей"', 'uk': 'Доступ до меню "Группа записів"'})
    Permission.create('add_translations_entry_menu_access', {'en': 'Access to "Add translations entry" menu', 'ru': 'Доступ к меню "Добавить переводы записей"', 'uk': 'Доступ до меню "Додати переклади записів"'})
    Permission.create('edit_translations_entry_menu_access', {'en': 'Access to "Edit translations entry" menu', 'ru': 'Доступ к меню "Редактировать переводы записей"', 'uk': 'Доступ до меню "Редагувати переклади записів"'})

    Permission.create('allow_remove_entries', {'en': 'Allow delete entries', 'ru': 'Разрешить удаление записей', 'uk': 'Дозволити видалення записів'})
    Permission.create('allow_remove_translations_entry', {'en': 'Allow delete entry translations', 'ru': 'Доступ к меню "Удалить запись переводов"', 'uk': 'Доступ до меню "Видалення запису перекладів"'})

    Permission.create('allow_remove_translations_entry', {'en': 'Allow delete group translations', 'ru': 'Доступ к меню "Удалить запись переводов"', 'uk': 'Доступ до меню "Видалення запису перекладів"'})
    Permission.create('import_from_csv_access', {'en': 'Access to "Import from csv" menu', 'ru': 'Доступ к меню "Импорт из CSV"', 'uk': 'Доступ до меню "Імпортувати з csv"'})

    Permission.create('allow_add_permission', {'en': 'Allow add permission', 'ru': 'Разрешить добавлять право', 'uk': 'Дозволити додавати право'})
    Permission.create('allow_remove_permission', {'en': 'Allow remove permission', 'ru': 'Разрешить удалять право', 'uk': 'Дозволити видаляти право'})
    Permission.create('superuser', {'en': 'Superuser', 'ru': 'Суперпользователь', 'uk': 'Суперкористувач'})

    DBSession.commit()

    superuser = DBSession.query(User).filter(User.username == 'm8_uwot').first()
    if superuser:
        for permission in DBSession.query(Permission).all():
            if not superuser.has_permission(permission.code):
                superuser.permissions.append(permission)
        DBSession.add(superuser)
    DBSession.commit()


if __name__ == '__main__':
    main()
