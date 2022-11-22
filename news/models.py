from django.db import models

from accounts.models import User


class News(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Заголовок")
    news_text = models.TextField(
        verbose_name="Текст")
    date_posted = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата опубликования")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="news",
        verbose_name="Владелец")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"