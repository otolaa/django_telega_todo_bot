from django.db import models


class Uid(models.Model):
    username = models.CharField(verbose_name="Логин", max_length=150)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.id} - @{self.username}'

class Todo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создание")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновление")

    is_active = models.BooleanField(default=True, verbose_name="Активность")
    title = models.CharField(max_length=369, verbose_name="Дело")

    uid = models.ForeignKey(Uid, verbose_name="Пользователь", related_name='uid', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Дело'
        verbose_name_plural = 'Дела'

    def __str__(self):
        return f'№{self.id} - {self.title}'