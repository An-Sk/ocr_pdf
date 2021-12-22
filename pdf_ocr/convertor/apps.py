from django.apps import AppConfig

"""Класс показывающий джанго, что папка convertor содержит приложение"""
class ConvertorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'convertor'
