from django.contrib import admin
from django.utils.html import format_html
from .models import Category, PrintItem, PrintImage, PrintComment, PrintLike


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


class PrintImageInline(admin.TabularInline):
    model = PrintImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(PrintItem)
class PrintItemAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'author', 'difficulty', 'status', 
        'views_count', 'likes_count', 'created_at'
    ]
    list_filter = ['category', 'difficulty', 'status', 'filament_type', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    prepopulated_fields = {}
    readonly_fields = ['views_count', 'likes_count', 'downloads_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'author', 'status')
        }),
        ('Print Specifications', {
            'fields': (
                'difficulty', 'print_time_hours', 'filament_type', 
                'filament_amount_grams', 'layer_height', 'infill_percentage'
            )
        }),
        ('Media', {
            'fields': ('main_image', 'stl_file')
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count', 'downloads_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [PrintImageInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'author')


@admin.register(PrintComment)
class PrintCommentAdmin(admin.ModelAdmin):
    list_display = ['print_item', 'author', 'content_preview', 'created_at']
    list_filter = ['created_at', 'print_item__category']
    search_fields = ['content', 'author__username', 'print_item__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(PrintLike)
class PrintLikeAdmin(admin.ModelAdmin):
    list_display = ['print_item', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['print_item__title', 'user__username']


# Customize admin site
admin.site.site_header = "3D Printing Site Administration"
admin.site.site_title = "3D Printing Admin"
admin.site.index_title = "Welcome to 3D Printing Site Administration"
