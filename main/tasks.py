from .models import Article, GalleryItem, Category
from django.template.loader import render_to_string

def get_latest_news_html():
    latest_articles = Article.objects.filter(is_published=True).order_by('-created_at')[:5]
    gallery_items = GalleryItem.objects.all().order_by('-created_at')[:5]
    categories = Category.objects.all()
    
    return render_to_string('daily_newsletter.html', {
        'latest_articles': latest_articles,
        'gallery_items': gallery_items,
        'categories': categories
    })
