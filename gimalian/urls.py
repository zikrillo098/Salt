from django.urls import path
from .views import index, post_detail, email_share, category_share
from django.urls import re_path

app_name = 'gimalian'

urlpatterns = [
    path('', index, name='index'),
    re_path(r'^tag/(?P<tag_slug>[-\w]+)/$', index, name='index_tags'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', post_detail, name='post_detail'),
    path('<int:post_id>/share/', email_share, name='email_share'),
    path('<int:category_id>/category', category_share, name='category')
]
