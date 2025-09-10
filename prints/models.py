from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """Model for 3D print categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('prints:category_detail', kwargs={'slug': self.slug})


class PrintItem(models.Model):
    """Model for individual 3D print items"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('featured', 'Featured'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='prints')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prints')
    
    # Print specifications
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    print_time_hours = models.PositiveIntegerField(help_text="Estimated print time in hours")
    filament_type = models.CharField(max_length=50, default='PLA')
    filament_amount_grams = models.PositiveIntegerField(help_text="Amount of filament needed in grams")
    layer_height = models.DecimalField(max_digits=3, decimal_places=2, default=0.20, help_text="Layer height in mm")
    infill_percentage = models.PositiveIntegerField(default=20, help_text="Infill percentage")
    
    # Media
    main_image = models.ImageField(upload_to='prints/images/', blank=True, null=True)
    stl_file = models.FileField(upload_to='prints/stl_files/', blank=True, null=True)
    
    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('prints:print_detail', kwargs={'pk': self.pk})
    
    def get_difficulty_color(self):
        """Return color class for difficulty level"""
        colors = {
            'beginner': 'success',
            'intermediate': 'warning', 
            'advanced': 'danger',
            'expert': 'dark'
        }
        return colors.get(self.difficulty, 'secondary')


class PrintImage(models.Model):
    """Model for additional images of print items"""
    print_item = models.ForeignKey(PrintItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='prints/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.print_item.title} - Image {self.order}"


class PrintComment(models.Model):
    """Model for comments on print items"""
    print_item = models.ForeignKey(PrintItem, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.print_item.title}"


class PrintLike(models.Model):
    """Model for likes on print items"""
    print_item = models.ForeignKey(PrintItem, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['print_item', 'user']
    
    def __str__(self):
        return f"{self.user.username} likes {self.print_item.title}"
