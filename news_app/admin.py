from django.contrib import admin
from .models import News, Category, Contact, Comment

# admin.site.register(News)
# admin.site.register(Category)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'publish_time', 'status']
    list_filter = ['status', 'created_time', 'publish_time']
    prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ['title', 'body']
    ordering = ['status', 'publish_time']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject']

# 2-usul
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['deactivate_commets', 'activate_comments']

    def deactivate_commets(self, request, queryset):
        queryset.update(active=False)

    def activate_commets(self, request, queryset):
        queryset.update(active=True)

# 1-usul
# admin.site.register(Comment, CommentAdmin)

# Register your models here.
