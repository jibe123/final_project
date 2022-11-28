from django.db import models

from accounts.models import User


class Thread(models.Model):
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания темы")
    title = models.CharField(
        max_length=100, blank=True, default='',
        verbose_name="Заголовок темы")
    owner = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='threads',
        verbose_name="Создатель темы")

    class Meta:
        ordering = ('created',)

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class Message(models.Model):
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания сообщения")
    title = models.CharField(
        max_length=100, blank=True, default='',
        verbose_name="Заголовок")
    body_text = models.TextField(verbose_name="Текст сообщения")
    owner = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='messages', verbose_name="Создатель сообщения")
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE,
        verbose_name="Сообщение по теме", related_name='messages')

    class Meta:
        ordering = ('created',)
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
