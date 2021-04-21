from modeltranslation.translator import register, TranslationOptions
from app.territory.models import Territory


@register(Territory)
class TerritoryTranslationOptions(TranslationOptions):
    fields = ('name',)
