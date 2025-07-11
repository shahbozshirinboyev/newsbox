from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class PublishedManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset().filter(status=News.Status.Published)

class Category(models.Model):
  name = models.CharField(max_length=150)
  description = models.TextField()

  def __str__(self):
    return self.name

class News(models.Model):
  class Status(models.TextChoices):
    Draft = "DF", "Draft"
    Published = "PB", "Published"

  # id = models.IntegerField(primary_key=True, unique=True)
  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=250)
  body = models.TextField()
  image = models.ImageField(upload_to='news/images') #Rasmlar bilan ishlaganda "pillow" kutubxonasini o'rnatish kerak bo'ladi.
  # pipenv install Pillow
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  publish_time = models.DateTimeField(default=timezone.now)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=2, choices=Status.choices, default=Status.Draft)

  objects = models.Manager() #default django manager
  published = PublishedManager()

  class Meta:
    ordering = ["-publish_time"]

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('news_detail_page', args=[self.slug])

  def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Contact(models.Model):
  name = models.CharField(max_length=150)
  email = models.EmailField(max_length=150)
  subject = models.CharField(max_length=300)
  message = models.TextField()

  def __str__(self):
    return self.email
