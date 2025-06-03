from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'access_level', 'created_at', 'is_featured')
    list_filter = ('access_level', 'category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    raw_id_fields = ('author',)
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'tags', 'access_level')
        }),
        ('Flags', {
            'fields': ('is_featured', 'is_published')
        }),
    )
