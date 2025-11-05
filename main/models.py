from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# 🌍 إعدادات الموقع العامة
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default="الثَّقَف العربي", verbose_name="اسم الموقع")
    logo = models.ImageField(upload_to="site_logo/", blank=True, null=True, verbose_name="شعار الموقع")

    hero_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="عنوان الهيرو (Hero)")
    hero_subtitle = models.TextField(blank=True, null=True, verbose_name="وصف الهيرو")

    hero_background = models.ImageField(upload_to="hero_backgrounds/", blank=True, null=True, verbose_name="خلفية الهيرو")
    hero_background_url = models.URLField(blank=True, null=True, verbose_name="رابط خلفية الهيرو (URL)")

    footer_text = models.TextField(blank=True, null=True, verbose_name="نص الفوتر")

    class Meta:
        verbose_name = "إعدادات الموقع"
        verbose_name_plural = "إعدادات الموقع"

    def __str__(self):
        return self.site_name or "إعدادات الموقع"

    def get_hero_background(self):
        """ترجع الخلفية سواء كانت مرفوعة أو من رابط أو افتراضية"""
        if self.hero_background:
            return self.hero_background.url
        elif self.hero_background_url:
            return self.hero_background_url
        return '/static/images/default_hero.jpg'


# 📚 الأقسام
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="اسم القسم")
    slug = models.SlugField(unique=True, verbose_name="رابط القسم (slug)")
    description = models.TextField(blank=True, null=True, verbose_name="وصف القسم")
    image = models.ImageField(upload_to="category_images/", blank=True, null=True, verbose_name="صورة القسم")
    image_url = models.URLField(blank=True, null=True, verbose_name="رابط الصورة (URL)")

    class Meta:
        verbose_name = "قسم"
        verbose_name_plural = "الأقسام"

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return '/static/images/default_category.png'


# 📰 المقالات
class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="articles", verbose_name="القسم")
    title = models.CharField(max_length=200, verbose_name="عنوان المقال")
    slug = models.SlugField(unique=True, verbose_name="الرابط (slug)")
    author = models.CharField(max_length=100, default="فريق الثَّقَف العربي", verbose_name="الكاتب")
    content = RichTextUploadingField(verbose_name="محتوى المقال")
    image = models.ImageField(upload_to="articles/", blank=True, null=True, verbose_name="صورة المقال")
    image_url = models.URLField(blank=True, null=True, verbose_name="رابط الصورة (URL)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name="منشور؟")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "مقال"
        verbose_name_plural = "المقالات"

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return '/static/images/default_article.jpg'

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})


# 🎞️ معرض الوسائط
MEDIA_TYPES = [
    ('image', 'صورة'),
    ('video', 'فيديو'),
    ('news', 'خبر'),
]

class MediaItem(models.Model):
    title = models.CharField(max_length=200, verbose_name="العنوان")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, verbose_name="النوع")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    image = models.ImageField(upload_to="gallery/", blank=True, null=True, verbose_name="صورة")
    image_url = models.URLField(blank=True, null=True, verbose_name="رابط الصورة (URL)")
    video_url = models.URLField(blank=True, null=True, verbose_name="رابط الفيديو (YouTube أو خارجي)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "عنصر وسائط"
        verbose_name_plural = "📷 معرض الصور والفيديوهات"

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return '/static/images/default_gallery.jpg'


# 📬 نموذج اتصل بنا
class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="الاسم")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    message = models.TextField(verbose_name="الرسالة")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "رسالة تواصل"
        verbose_name_plural = "رسائل التواصل"

    def __str__(self):
        return f"رسالة من {self.name}"
from django.db import models

class GalleryItem(models.Model):
    TYPE_CHOICES = (
        ('image', 'صورة'),
        ('video', 'فيديو'),
        ('news', 'خبر'),
    )

    title = models.CharField(max_length=200, verbose_name="عنوان العنصر")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='image', verbose_name="نوع العنصر")
    media_file = models.FileField(upload_to="gallery_media/", blank=True, null=True, verbose_name="ملف الوسائط")
    media_url = models.URLField(blank=True, null=True, verbose_name="رابط خارجي للوسائط")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "عنصر معرض"
        verbose_name_plural = "معرض الصور والفيديوهات والأخبار"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_media(self):
        """إرجاع الرابط الصحيح للوسائط"""
        if self.media_file:
            return self.media_file.url
        elif self.media_url:
            return self.media_url
        return '/static/images/default_media.jpg'
