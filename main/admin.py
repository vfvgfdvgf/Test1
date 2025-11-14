from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.utils.html import format_html
from .models import (
    Category, Article, SiteSettings, ContactMessage, 
    MediaItem, GalleryItem, Subscriber, Notification
)

# 📚 إدارة الأقسام
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'description', 'image', 'image_url')}),
        ('SEO', {'fields': ('seo_title', 'seo_description', 'seo_keywords')}),
    )

# 📰 إدارة المقالات
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'is_published')
    list_filter = ('category', 'created_at', 'is_published')
    search_fields = ('title', 'content', 'seo_keywords')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('category', 'title', 'slug', 'author', 'content', 'image', 'image_url')}),
        ('SEO', {'fields': ('seo_title', 'seo_description', 'seo_keywords')}),
        ('النشر', {'fields': ('is_published', 'created_at', 'updated_at')}),
    )

from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name",)
    fields = ("site_name", "favicon", "favicon_url")


# 📬 رسائل التواصل
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")

# 🎞️ إدارة الوسائط
@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "created_at")
    list_filter = ("media_type", "created_at")
    search_fields = ("title", "description")

# 🖼️ معرض الوسائط
@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'created_at', 'cover_preview')
    list_filter = ('type', 'created_at')
    search_fields = ('title', 'description', 'seo_keywords')
    readonly_fields = ('created_at', 'cover_preview')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('title', 'description', 'type')}),
        ('الوسائط', {'fields': ('media_file', 'media_url')}),
        ('صورة الغلاف', {'fields': ('cover_image', 'cover_image_url', 'cover_preview')}),
        ('SEO', {'fields': ('seo_title', 'seo_description', 'seo_keywords')}),
        ('معلومات إضافية', {'fields': ('created_at',)}),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="100" style="border-radius:8px;">', obj.cover_image.url)
        return "لا توجد صورة غلاف"
    cover_preview.short_description = "معاينة الغلاف"

# 📨 المشتركين
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'send_button')
    readonly_fields = ('created_at',)

    change_list_template = "admin/subscriber_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('send-newsletter/', self.admin_site.admin_view(self.send_newsletter_view), name='send_newsletter')
        ]
        return custom + urls

    def send_newsletter_view(self, request):
        subscribers = Subscriber.objects.all()
        latest = Article.objects.filter(is_published=True).order_by('-created_at')[:5]

        subject = "النشرة اليومية للثقافة العربية"
        message = "\n".join([f"{a.title}: {a.get_absolute_url()}" for a in latest])

        for sub in subscribers:
            send_mail(subject, message, None, [sub.email])

        self.message_user(request, "🚀 تم إرسال النشرة لجميع المشتركين!")
        return redirect("../")

    def send_button(self, obj):
        return format_html('<a class="button" href="send-newsletter/">إرسال</a>')
    send_button.short_description = "إرسال النشرة"

# 🔔 الإشعارات
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active',)
    search_fields = ('title', 'message')
