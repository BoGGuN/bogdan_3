# Create your models here.

from django.db import models

# class Author(models.Model):
#     first_name =  models.CharField("Имя", max_length=255)
#     surname = models.CharField("Фамилия", max_length=255)
#     patronymic = models.CharField("Отчество", max_length=255)
#     birth_date = models.DateField("Дата рождения")
#
#     class Meta:
#         verbose_name="Автор"
#         verbose_name_plural = "Авторы"
#         ordering = ["first_name"]
#
#     def __str__(self):
#         return f'{self.first_name} {self.surname} {self.patronymic}'
#
# class Book(models.Model):
#     title=models.CharField(verbose_name="Название", max_length=255)
#     public_date = models.DateField(verbose_name="Дата публикации")
#     description = models.TextField(verbose_name="Описание", blank=True)
#     author = models.ForeignKey(
#         Author,
#         verbose_name="Автор",
#         blank=True,
#         null=True,
#         related_name='books',
#         on_delete = models.SET_NULL,
#     )
#
#     class Meta:
#         verbose_name="Книга"
#         verbose_name_plural = "Книги"
#         ordering = ["-title"]
#
#     def __str__(self):
#         return self.title
#
# class Genre(models.Model):
#     name = models.CharField("Название", max_length=255)
#     description = models.TextField("Описание", blank=True)
#     books = models.ManyToManyField(
#         Book,
#         verbose_name="Книги",
#         related_name="genres",
#         blank=True,
#     )
#
#     class Meta:
#         verbose_name="Жанр"
#         verbose_name_plural = "Жанры"
#         ordering = ["name"]
#
#     def __str__(self):
#         return self.name
#
# class Storage(models.Model):
#     amount = models.PositiveIntegerField("Количество")
#     price = models.PositiveIntegerField("Стоимость")
#     book = models.OneToOneField(
#         Book,
#         verbose_name="Книга",
#         related_name="storage",
#         blank=True,
#         null = True,
#         on_delete=models.SET_NULL,
#     )
#
#     class Meta:
#         verbose_name = "Склад"
#         verbose_name_plural = "Склады"
#         ordering = ["amount","price"]
#
#     def __str__(self):
#         return f'{self.book} {self.price}'
#
#     def get_discount(self):
#         return self.price - (self.price*0.1)


class Profile(models.Model):
    name = models.CharField("Имя", max_length=255)
    description = models.TextField(verbose_name="Описание", blank = True)
    birth_date = models.DateField("Дата рождения")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural="Профили"
        ordering=["-name"]

    def __str__(self):
        return self.name

class User(models.Model):
    login = models.CharField('Логин', max_length=255, unique=True)
    password = models.CharField('Пароль', max_length=255)
    profile = models.OneToOneField(
        Profile,
        verbose_name="Профиль",
        related_name = "user",
        blank=False,
        null=False,
        on_delete = models.CASCADE,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-profile"]

    def __str__(self):
        return self.login

class Group(models.Model):
    name = models.CharField("Название", max_length=255, unique=True)
    admin = models.ForeignKey(
        User,
        verbose_name="Админ группы",
        related_name = "group_admin",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    users = models.ManyToManyField(
        User,
        verbose_name="Участники",
        related_name="group_users",
        blank = True,
    )

    class Meta:
        verbose_name="Группа"
        verbose_name_plural="Группы"
        ordering = ["-name"]

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField("Название", max_length=255)
    text = models.TextField("Текст", blank=False)
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    edited_at = models.DateTimeField(
        verbose_name="Дата редактирования",
        auto_now=True,
    )
    group = models.ForeignKey(
        Group,
        verbose_name="Группа",
        related_name="group_posts",
        blank=False,
        null = False,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name="user_posts",
        blank = False,
        null = True,
        on_delete=models.SET_NULL,
    )
    image_field=models.ImageField(
        verbose_name="Изображение",
        upload_to='posts/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name="Пост"
        verbose_name_plural="Посты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField('Комментарий', blank = False)
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    edited_at = models.DateTimeField(
        verbose_name="Дата редактирования",
        auto_now=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name = "user_comments",
        blank = False,
        null = True,
        on_delete=models.SET_NULL,
    )
    post = models.ForeignKey(
        Post,
        verbose_name="Пост",
        related_name="post_comments",
        blank = False,
        null = False,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        # if self.author:
        #     return f'{self.author} - {self.text}'
        # else:
        #     return f'Аноним - {self.text}'
        if self.author:
            return f'{self.author} - {self.created_at}'
        else:
            return f'{self.created_at}'