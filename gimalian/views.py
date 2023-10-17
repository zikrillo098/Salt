from django.shortcuts import render, get_object_or_404
from .models import Category, Post
from .forms import EmailShareForms
from django.core.mail import send_mail
from taggit.models import Tag


def index(request, tag_slug=None):
    post = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post = post.filter(tags__in=[tag])
    category = Category.objects.all()
    return render(request, 'gimalian/index.html', {'post': post,
                                                   'category': category,
                                                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'gimalian/detail.html', {'post': post})


def email_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailShareForms(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} посововетовал вам прочитать {post.title}"
            message = f"""Прочитайте {post.title} ссылка на пост: {post_url}
{cd['name']} прокоментировал {cd['comments']}"""
            send_mail(subject, message, 'abdukhakimovzikrillo886@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailShareForms()

    return render(request, '_heloer/share.html', {'post': post,
                                                  'form': form,
                                                  'sent': sent})


def category_share(request, category_id):
    category = Category.objects.filter(id=category_id)
    post = Post.published.filter(category__id=category_id)
    return render(request, 'gimalian/category.html', {'category': category,
                                                      'post': post})
