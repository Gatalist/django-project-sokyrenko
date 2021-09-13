from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from datetime import date
from django.utils import timezone

from django.urls import reverse


class Category(models.Model):
    """Категория"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Author(models.Model):
    """Автор"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="author/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Автора"


class Sculpture(models.Model):
    """Скульптура"""
    draft = models.BooleanField("Деактивировать на сайте", default=False)
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    url = models.SlugField("Ссылка", max_length=160, unique=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    author = models.ManyToManyField(Author, verbose_name="Автор", related_name='sculpture_author')
    description = RichTextUploadingField("Описание")
    image_title = models.ImageField("Фото изделия", upload_to='image_title/')
    files = models.FileField(verbose_name='Архив с фото', default="", upload_to='files/', blank=True)
    presence = models.CharField("Наличие", max_length=30, blank=True)
    complectation = models.CharField("Комплектация", max_length=99, default='', blank=True)
    production_time = models.CharField("Срок изготовления", max_length=30, blank=True)
    price = models.IntegerField("Цена", default='12000', blank=True)
    old_price = models.IntegerField("Старая цена", blank=True, null=True)
    valute = models.CharField("Валюта", default='грн', max_length=10, blank=True, null=True)

    year = models.DateField("Изделие создано", default=date.today, blank=True)
    material = models.CharField("Материал", max_length=60, blank=True)
    gabarits = models.CharField("Габариты", max_length=30, blank=True)
    conditions = RichTextUploadingField("Условия заказа", blank=True)
    delivery = RichTextUploadingField("Доставка", blank=True)

    meta_keywords = models.TextField("meta name=\"keywords\" content ", default='', blank=True)
    meta_description = models.TextField("meta name=\"description\" content ", default='', blank=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("sculpture_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия | Каталог"


class ImageSculpture(models.Model):
    """Изображения скульптуры"""
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="image_sculpture/")
    sculpture = models.ForeignKey(Sculpture, verbose_name="Изделие", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sculpture} - {self.title}'

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения | Католог"


class ImageHome(models.Model):
    """слайдер на главной"""
    draft = models.BooleanField("Деактивировать на сайте", default=False)
    title = RichTextUploadingField("Заголовок", max_length=100)
    up_title = models.CharField("Подзаголовок", max_length=100)
    image = models.ImageField("Изображение", upload_to="image_home/")
    sculpture = models.ForeignKey(Sculpture, verbose_name="Изделие", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sculpture}'

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды на главной"


class News(models.Model):
    draft = models.BooleanField("Деактивировать на сайте", default=False)
    title = models.CharField("Имя", max_length=100)
    text = RichTextUploadingField("Сообщение", max_length=5000)
    image = models.ImageField("Изображение", upload_to="news/")
    year = models.DateField("Дата публикации", default=date.today)

    def __str__(self):
        return f'{self.title} - {self.year}'

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    sculpture = models.ForeignKey(Sculpture, verbose_name="Изделие", on_delete=models.CASCADE)
    year = models.DateField("Дата отзыва", default=date.today, blank=True)

    def __str__(self):
        return f"{self.sculpture} - {self.name}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Development(models.Model):
    """Скульптура разработка"""
    draft = models.BooleanField("Деактивировать на сайте", default=False)
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    url = models.SlugField("Ссылка", max_length=160, unique=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)

    description = RichTextUploadingField("Описание")
    image_title = models.ImageField("Фото изделия", upload_to='image_title/')

    meta_keywords = models.TextField("Meta name=\"keywords\" content ", default='', blank=True)
    meta_description = models.TextField("Meta name=\"description\" content ", default='', blank=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("development", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия | Мастерская"


class ImageDevelopment(models.Model):
    """Изображения скульптуры"""
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="image_sculpture/")
    sculpture = models.ForeignKey(Development, verbose_name="Изделие", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sculpture} - {self.title}'

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения | Мастерская"


class PlaceOder(models.Model):
    """Оформить заказ"""
    email = models.EmailField()
    first_name = models.CharField("Имя", max_length=30, default='')
    last_name = models.CharField("Фамилия", max_length=50, default='')
    phone = models.CharField("Телефон", max_length=13)
    text = models.TextField("Сообщение", max_length=5000, default='', blank=True)
    sculpture = models.ForeignKey(Sculpture, verbose_name="Изделие", on_delete=models.CASCADE)
    year = models.DateTimeField("Дата заказа", default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.sculpture}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
