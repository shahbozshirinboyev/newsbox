from django.shortcuts import render, get_object_or_404
from .models import Category, News
from .forms import ContactForm
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

# Create your views here.
def news_list(request):
  news_list_published = News.published.all()
  news_list_draft = News.objects.filter(status=News.Status.Draft)
  context = {
    'news_list_published': news_list_published,
    'news_list_draft': news_list_draft
  }
  return render(request, 'news/news_list.html', context)

def news_detail(request, news):
  news = get_object_or_404(News, slug=news, status=News.Status.Published)
  context = {
    'news': news,
  }
  return render(request, 'news/news_detail_page.html', context)

# def homePageView(request):
#   news_list = News.published.all().order_by('-publish_time')
#   categories = Category.objects.all()
#   sport_news_one = News.published.all().filter(category__name='Sport').order_by('-publish_time')[0]
#   sport_news_two = News.published.filter(category__name='Sport').order_by('-publish_time')[1:3]
#   context = {
#     'news_list': news_list,
#     'categories': categories,
#     'sport_news_one': sport_news_one,
#     'sport_news_two': sport_news_two,
#   }
#   return render(request, 'news/index.html', context)

class HomePageView(ListView):
   model = News
   template_name = 'news/index.html'
   context_object_name = 'news'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['categories'] = Category.objects.all()
      context['news_list'] = News.published.all().order_by('-publish_time')
      context['sport'] = News.published.all().filter(category__name='Sport').order_by('-publish_time')
      context['jamiyat'] = News.published.all().filter(category__name='Jamiyat').order_by('-publish_time')
      context['texnologiya'] = News.published.all().filter(category__name='Texnologiya').order_by('-publish_time')
      context['iqtisodiyot'] = News.published.all().filter(category__name='Iqtisodiyot').order_by('-publish_time')
      context['siyosat'] = News.published.all().filter(category__name='Siyosat').order_by('-publish_time')
      return context

def categoryPageView(request):
   news_list = News.published.all().order_by('-publish_time')
   categories = Category.objects.all()
   context = {
    'news_list': news_list,
    'categories': categories,
  }
   return render(request, 'news/categories.html', context)

def AboutPageView(request):
    return render(request, 'news/about.html')

# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#        form.save()
#        return HttpResponse("<h2>Biz bilan bog'langaningiz uchun rahmat!</h2>")
#     context = {
#        'form': form
#     }
#     return render(request, 'news/contact.html', context)

# contactPageView'ni class orqali ham qilib ko'ramiz:

class ContactPageView(TemplateView):
   template_name = 'news/contact.html'

   def get(self, request, *args, **kwargs):
      form = ContactForm
      context = {
         'form': form,
      }
      return render(request, 'news/contact.html', context)

   def post(self, request, *args, **kwargs):
      form = ContactForm(request.POST)
      if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponse("<h2>Biz bilan bog'langaningiz uchun rahmat!</h2>")
      context = {
         'form': form,
      }
      return render(request, 'news/contact.html', context)

# Sport
class SportNewsView(ListView):
   model = News
   template_name = 'news/sport.html'
   context_object_name = 'sport_yangiliklari'

   def get_queryset(self):
    news = self.model.published.all().filter(category__name = 'Sport')
    return news

# Jamiyat
class JamiyatNewsView(ListView):
   model = News
   template_name = 'news/jamiyat.html'
   context_object_name = 'jamiyat_yangiliklari'

   def get_queryset(self):
    news = self.model.published.all().filter(category__name = 'Jamiyat')
    return news

# Texnologiya
class TexnologiyaNewsView(ListView):
   model = News
   template_name = 'news/texnologiya.html'
   context_object_name = 'texnologiya_yangiliklari'

   def get_queryset(self):
    news = self.model.published.all().filter(category__name = 'Texnologiya')
    return news

# Iqtisodiyot
class IqtisodiyotNewsView(ListView):
   model = News
   template_name = 'news/iqtisodiyot.html'
   context_object_name = 'iqtisodiyot_yangiliklari'

   def get_queryset(self):
    news = self.model.published.all().filter(category__name = 'Iqtisodiyot')
    return news

# Siyosat
class SiyosatNewsView(ListView):
   model = News
   template_name = 'news/siyosat.html'
   context_object_name = 'siyosat_yangiliklari'

   def get_queryset(self):
    news = self.model.published.all().filter(category__name = 'Siyosat')
    return news

class NewsUpdateView(UpdateView):
  model = News
  fields = ('title', 'body', 'image', 'category', 'status')
  template_name = 'crud/news_edit.html'

class NewsDeleteView(DeleteView):
  model = News
  template_name = 'crud/news_delete.html'
  success_url = reverse_lazy('home_page')

class NewsCreateView(CreateView):
  model = News
  template_name = 'crud/news_create.html'
  fields = ('title', 'body', 'image', 'category', 'status')