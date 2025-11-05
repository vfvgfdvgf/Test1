from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Category, GalleryItem

# ---------------- Articles ----------------
class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.filter(is_published=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at

# ---------------- Categories ----------------
class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.all().order_by('name')

    def location(self, obj):
        return reverse('category_detail', args=[obj.slug])

# ---------------- Static Views ----------------
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        # إضافة الصفحات الثابتة
        return ['home', 'articles', 'contact', 'about', 'terms', 'privacy', 'disclaimer', 'gallery']

    def location(self, item):
        return reverse(item)

# ---------------- Gallery ----------------
class GallerySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return GalleryItem.objects.all().order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at

    def location(self, obj):
        return reverse('gallery_detail', args=[obj.id])
