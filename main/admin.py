from django.contrib import admin
from .models import Category, Article, SiteSettings, ContactMessage, MediaItem

# 📚 إدارة الأقسام
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

# 📰 إدارة المقالات
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "is_published", "created_at")
    list_filter = ("is_published", "category")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}

# 🌍 إعدادات الموقع
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name",)
    search_fields = ("site_name",)

# 📬 رسائل التواصل
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")

# 🎞️ معرض الوسائط
@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "created_at")
    list_filter = ("media_type", "created_at")
    search_fields = ("title", "description")
from django.contrib import admin
from .models import GalleryItem

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
