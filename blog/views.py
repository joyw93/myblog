from django.shortcuts import render
from .models import Post, Category



def post_list(request):
    posts = Post.objects.all().order_by('-pk')
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : posts,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
        }
    )    


def category_page(request, slug):
    if slug == "no_category":
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
            'category' : category
        }
    )    


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/post_detail.html',
        {
            'post' : post,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
        }
    )
