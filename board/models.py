from django.db import models

from accounts.models import User


class Thread(models.Model):
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания темы")
    title = models.CharField(
        max_length=100, blank=True, default='',
        verbose_name="Заголовок темы")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='threads',
        verbose_name="Создатель темы")

    def __str__(self):
        return self.title

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
        User, on_delete=models.CASCADE,
        related_name='messages', verbose_name="Создатель сообщения")
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE,
        verbose_name="Сообщение по теме", related_name='messages')
    likes = models.ManyToManyField(
        User, related_name='liked', verbose_name="Лайки")

    def __str__(self):
        return self.title

    def count_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ('created',)
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
