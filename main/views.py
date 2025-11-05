from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Article, Category, SiteSettings, MediaItem

# 🏠 الصفحة الرئيسية
from .models import SiteSettings, Article, Category, GalleryItem

def home(request):
    site_settings = SiteSettings.objects.first()
    latest_articles = Article.objects.filter(is_published=True).order_by('-created_at')[:6]
    categories = Category.objects.all()
    
    # عناصر المعرض: صور، فيديوهات، وأخبار
    gallery_items = GalleryItem.objects.all().order_by('-created_at')[:10]

    return render(request, 'index.html', {
        'site_settings': site_settings,
        'latest_articles': latest_articles,
        'categories': categories,
        'gallery_items': gallery_items,  # ⬅ تم الإضافة
    })


# 📰 صفحة جميع المقالات
def articles(request):
    all_articles = Article.objects.filter(is_published=True).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'articles.html', {
        'articles': all_articles,
        'categories': categories
    })

# 🌍 صفحة الأقسام
def categories_view(request):
    cats = Category.objects.all()
    return render(request, 'categories.html', {'categories': cats})

# 📄 صفحة عرض مقالات قسم معين
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category, is_published=True)
    return render(request, 'category_detail.html', {
        'category': category,
        'articles': articles
    })

# 📖 صفحة عرض مقال معين
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    related_articles = Article.objects.filter(
        category=article.category,
        is_published=True
    ).exclude(id=article.id)[:3]
    return render(request, 'article_detail.html', {
        'article': article,
        'related_articles': related_articles
    })

# 📑 الصفحات الثابتة
def about(request):
    return render(request, 'about.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def disclaimer(request):
    return render(request, 'disclaimer.html')

# 💬 صفحة الاتصال
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        full_message = f"📩 رسالة جديدة من {name} <{email}>\n\nالموضوع: {subject}\n\nالرسالة:\n{message}"

        # إرسال إلى البريد الرئيسي
        send_mail(
            subject=f"رسالة جديدة من موقع الثَّقَف العربي: {subject}",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["halax.7y7@gmail.com"],
            fail_silently=False,
        )

        # إرسال تأكيد للمستخدم
        confirmation = (
            f"مرحباً {name},\n\n"
            "نشكر تواصلك مع موقع الثَّقَف العربي 🌿\n"
            "تم استلام رسالتك وسنقوم بالرد عليك قريباً بإذن الله.\n\n"
            "تحياتنا،\nفريق الثَّقَف العربي"
        )

        send_mail(
            subject="تم استلام رسالتك - الثَّقَف العربي",
            message=confirmation,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        messages.success(request, "✅ تم إرسال رسالتك بنجاح! شكرًا لتواصلك معنا.")
        return redirect("contact")

    return render(request, "contact.html")

# 🎞️ صفحة معرض الوسائط (صور، فيديو، أخبار)
def gallery(request):
    images = MediaItem.objects.filter(media_type='image').order_by('-created_at')
    videos = MediaItem.objects.filter(media_type='video').order_by('-created_at')
    news = MediaItem.objects.filter(media_type='news').order_by('-created_at')
    site_settings = SiteSettings.objects.first()
    return render(request, 'gallery.html', {
        'images': images,
        'videos': videos,
        'news': news,
        'site_settings': site_settings
    })


from django.shortcuts import render, get_object_or_404
from .models import GalleryItem
from main.models import SiteSettings  # إذا أردنا اسم الموقع

def gallery(request):
    site_settings = SiteSettings.objects.first()
    items = GalleryItem.objects.all()
    return render(request, 'gallery.html', {'items': items, 'site_settings': site_settings})

def gallery_detail(request, pk):
    site_settings = SiteSettings.objects.first()
    item = get_object_or_404(GalleryItem, pk=pk)
    return render(request, 'gallery_detail.html', {'item': item, 'site_settings': site_settings})
