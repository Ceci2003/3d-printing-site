from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import PrintItem, Category, PrintComment, PrintLike


def home(request):
    """Home page with featured prints and categories"""
    featured_prints = PrintItem.objects.filter(status='featured')[:6]
    recent_prints = PrintItem.objects.filter(status='published')[:6]
    categories = Category.objects.annotate(print_count=Count('prints')).order_by('-print_count')[:8]
    
    context = {
        'featured_prints': featured_prints,
        'recent_prints': recent_prints,
        'categories': categories,
    }
    return render(request, 'prints/home.html', context)


def print_list(request):
    """List all published prints with filtering and search"""
    prints = PrintItem.objects.filter(status='published').select_related('category', 'author')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        prints = prints.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        prints = prints.filter(category__slug=category_slug)
    
    # Difficulty filter
    difficulty = request.GET.get('difficulty')
    if difficulty:
        prints = prints.filter(difficulty=difficulty)
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'popular':
        prints = prints.order_by('-views_count')
    elif sort_by == 'likes':
        prints = prints.order_by('-likes_count')
    elif sort_by == 'oldest':
        prints = prints.order_by('created_at')
    else:  # newest
        prints = prints.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(prints, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'current_difficulty': difficulty,
        'current_sort': sort_by,
        'search_query': search_query,
    }
    return render(request, 'prints/print_list.html', context)


def print_detail(request, pk):
    """Detail view for a specific print item"""
    print_item = get_object_or_404(PrintItem, pk=pk, status='published')
    
    # Increment view count
    print_item.views_count += 1
    print_item.save(update_fields=['views_count'])
    
    # Get related prints
    related_prints = PrintItem.objects.filter(
        category=print_item.category,
        status='published'
    ).exclude(pk=pk)[:4]
    
    # Get comments
    comments = print_item.comments.all()
    
    # Check if user has liked this print
    user_liked = False
    if request.user.is_authenticated:
        user_liked = PrintLike.objects.filter(
            print_item=print_item,
            user=request.user
        ).exists()
    
    context = {
        'print_item': print_item,
        'related_prints': related_prints,
        'comments': comments,
        'user_liked': user_liked,
    }
    return render(request, 'prints/print_detail.html', context)


def category_detail(request, slug):
    """Detail view for a category"""
    category = get_object_or_404(Category, slug=slug)
    prints = PrintItem.objects.filter(
        category=category,
        status='published'
    ).select_related('author').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(prints, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'prints/category_detail.html', context)


@login_required
def like_print(request, pk):
    """Like/unlike a print item"""
    if request.method == 'POST':
        print_item = get_object_or_404(PrintItem, pk=pk)
        like, created = PrintLike.objects.get_or_create(
            print_item=print_item,
            user=request.user
        )
        
        if not created:
            like.delete()
            print_item.likes_count -= 1
            liked = False
        else:
            print_item.likes_count += 1
            liked = True
        
        print_item.save(update_fields=['likes_count'])
        
        return JsonResponse({
            'liked': liked,
            'likes_count': print_item.likes_count
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def add_comment(request, pk):
    """Add a comment to a print item"""
    if request.method == 'POST':
        print_item = get_object_or_404(PrintItem, pk=pk)
        content = request.POST.get('content', '').strip()
        
        if content:
            PrintComment.objects.create(
                print_item=print_item,
                author=request.user,
                content=content
            )
            messages.success(request, 'Your comment has been added!')
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    return redirect('prints:print_detail', pk=pk)
