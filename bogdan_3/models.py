from django.db import models


class Book(models.Model):
    title=models.CharField(verbose_name="Название", max_length=255)
    public_date = models.DateField(verbose_name="Дата публикации")
    description = models.TextField(verbose_name="Описание", blank=True)
    author = models.ForeignKey(
        "Author",
        verbose_name="Автор",
        blank=True,
        null=True,
        related_name='books'
    )

    class Meta:
        verbose_name="Книга",
        verbose_name_plural = "Книги",
        ordering = ["-title"]

    def __str__(self):
        return self.title

class Author(models.Model):
    first_name =  models.CharField("Имя", max_length=255)
    surname = models.CharField("Фамилия", max_length=255)
    patronymic = models.CharField("Отчество", max_length=255)
    birth_date = models.DateField("Дата рождения")

    class Meta:
        verbose_name="Автор",
        verbose_name_plural = "Авторы",
        ordering = ["first_name"]

    def __str__(self):
        return f'{self.first_name} {self.surname} {self.patronymic}'

class Genre(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    books = models.ManyToManyField(
        "Book",
        verbose_name="Книги",
        related_name="genres",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name="Жанр",
        verbose_name_plural = "Жанры",
        ordering = ["name"]

    def __str__(self):
        return self.name

class Storage(models.Model):
    amount = models.PositiveIntegerField("Количество")
    price = models.PositiveIntegerField("Стоимость")
    book = models.OneToOneField(
        "Book",
        verbose_name="Книга",
        related_name="book",
        blank=True,
        null = True,
    )

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"
        ordering = ["amount","price"]

        def __str__(self):
            return f'{self.book} {self.price}'

        def get_discount(self):
            return self.price - (self.price*0.1)