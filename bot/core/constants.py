from django.utils.translation import gettext_lazy as _, activate


class BaseChoices:
    BACK = str(_('Назад'))

    def get_back(self):
        return str(_('Назад'))

    @staticmethod
    def get_back_multi():
        return 'Orqaga', 'Назад'
