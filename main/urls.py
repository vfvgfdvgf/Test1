from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # 🏠 الصفحة الرئيسية
    path('', views.home, name='home'),

    # 📰 المقالات
    path('articles/', views.articles, name='articles'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),

    # 🌍 الأقسام
    path('categories/', views.categories_view, name='categories'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    # 📑 الصفحات الثابتة
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),

    # 💬 صفحة الاتصال
    path('contact/', views.contact_view, name='contact'),

    # 🎞️ معرض الوسائط
   path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:pk>/', views.gallery_detail, name='gallery_detail'),
    
    # ✍️ محرر النصوص CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# 🖼️ إعدادات الوسائط في وضع التطوير فقط
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
