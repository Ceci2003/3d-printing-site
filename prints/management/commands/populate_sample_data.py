from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from prints.models import Category, PrintItem, PrintComment, PrintLike
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate the database with sample 3D printing data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            PrintLike.objects.all().delete()
            PrintComment.objects.all().delete()
            PrintItem.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating sample data...')

        # Create categories
        categories_data = [
            {
                'name': 'Toys & Games',
                'description': 'Fun toys, puzzles, and games for all ages',
                'slug': 'toys-games'
            },
            {
                'name': 'Home & Garden',
                'description': 'Practical items for your home and garden',
                'slug': 'home-garden'
            },
            {
                'name': 'Art & Sculpture',
                'description': 'Decorative art pieces and sculptures',
                'slug': 'art-sculpture'
            },
            {
                'name': 'Tools & Gadgets',
                'description': 'Useful tools and gadgets for everyday use',
                'slug': 'tools-gadgets'
            },
            {
                'name': 'Jewelry & Accessories',
                'description': 'Beautiful jewelry and fashion accessories',
                'slug': 'jewelry-accessories'
            },
            {
                'name': 'Educational',
                'description': 'Educational models and learning tools',
                'slug': 'educational'
            },
            {
                'name': 'Automotive',
                'description': 'Car parts, accessories, and automotive tools',
                'slug': 'automotive'
            },
            {
                'name': 'Electronics',
                'description': 'Cases, mounts, and accessories for electronics',
                'slug': 'electronics'
            }
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create users
        users_data = [
            {'username': 'maker_pro', 'email': 'pro@example.com', 'first_name': 'Alex', 'last_name': 'Johnson'},
            {'username': 'designer_anna', 'email': 'anna@example.com', 'first_name': 'Anna', 'last_name': 'Smith'},
            {'username': 'tech_geek', 'email': 'tech@example.com', 'first_name': 'Mike', 'last_name': 'Chen'},
            {'username': 'creative_carol', 'email': 'carol@example.com', 'first_name': 'Carol', 'last_name': 'Davis'},
            {'username': 'hobbyist_bob', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Wilson'},
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            users.append(user)
            if created:
                self.stdout.write(f'Created user: {user.username}')

        # Create print items
        prints_data = [
            {
                'title': 'Flexible Phone Stand',
                'description': 'A versatile phone stand that can hold your phone in both portrait and landscape modes. Features a flexible design that adapts to different viewing angles.',
                'category': 'electronics',
                'author': 'maker_pro',
                'difficulty': 'beginner',
                'print_time_hours': 2,
                'filament_type': 'PLA',
                'filament_amount_grams': 25,
                'layer_height': Decimal('0.20'),
                'infill_percentage': 20,
                'status': 'featured'
            },
            {
                'title': 'Dragon Bookmark',
                'description': 'An intricate dragon-shaped bookmark that will make reading more magical. Perfect for fantasy book lovers!',
                'category': 'art-sculpture',
                'author': 'designer_anna',
                'difficulty': 'intermediate',
                'print_time_hours': 4,
                'filament_type': 'PLA',
                'filament_amount_grams': 15,
                'layer_height': Decimal('0.15'),
                'infill_percentage': 15,
                'status': 'featured'
            },
            {
                'title': 'Cable Management Tray',
                'description': 'Keep your desk organized with this sleek cable management tray. Hides cables while maintaining easy access.',
                'category': 'tools-gadgets',
                'author': 'tech_geek',
                'difficulty': 'beginner',
                'print_time_hours': 3,
                'filament_type': 'PETG',
                'filament_amount_grams': 45,
                'layer_height': Decimal('0.25'),
                'infill_percentage': 25,
                'status': 'published'
            },
            {
                'title': 'Geometric Vase',
                'description': 'A stunning geometric vase that combines form and function. Perfect for displaying flowers or as a standalone art piece.',
                'category': 'art-sculpture',
                'author': 'creative_carol',
                'difficulty': 'advanced',
                'print_time_hours': 8,
                'filament_type': 'PLA',
                'filament_amount_grams': 120,
                'layer_height': Decimal('0.20'),
                'infill_percentage': 10,
                'status': 'featured'
            },
            {
                'title': 'Raspberry Pi Case',
                'description': 'A protective case for Raspberry Pi 4 with ventilation holes and easy access to ports. Includes mounting holes for various setups.',
                'category': 'electronics',
                'author': 'tech_geek',
                'difficulty': 'intermediate',
                'print_time_hours': 5,
                'filament_type': 'ABS',
                'filament_amount_grams': 60,
                'layer_height': Decimal('0.20'),
                'infill_percentage': 30,
                'status': 'published'
            },
            {
                'title': 'Toy Car',
                'description': 'A fun toy car for kids with smooth wheels and detailed design. Safe for children and durable for play.',
                'category': 'toys-games',
                'author': 'hobbyist_bob',
                'difficulty': 'beginner',
                'print_time_hours': 2,
                'filament_type': 'PLA',
                'filament_amount_grams': 35,
                'layer_height': Decimal('0.25'),
                'infill_percentage': 20,
                'status': 'published'
            },
            {
                'title': 'Garden Planter',
                'description': 'A decorative planter for your garden or indoor plants. Features drainage holes and a modern design.',
                'category': 'home-garden',
                'author': 'creative_carol',
                'difficulty': 'intermediate',
                'print_time_hours': 6,
                'filament_type': 'PETG',
                'filament_amount_grams': 150,
                'layer_height': Decimal('0.30'),
                'infill_percentage': 15,
                'status': 'published'
            },
            {
                'title': 'Mechanical Puzzle Cube',
                'description': 'A challenging mechanical puzzle that will test your problem-solving skills. Great for stress relief and mental exercise.',
                'category': 'toys-games',
                'author': 'designer_anna',
                'difficulty': 'expert',
                'print_time_hours': 12,
                'filament_type': 'PLA',
                'filament_amount_grams': 80,
                'layer_height': Decimal('0.15'),
                'infill_percentage': 40,
                'status': 'published'
            },
            {
                'title': 'Earring Holder',
                'description': 'An elegant earring holder that keeps your jewelry organized and easily accessible. Beautiful design for your dressing table.',
                'category': 'jewelry-accessories',
                'author': 'designer_anna',
                'difficulty': 'beginner',
                'print_time_hours': 1,
                'filament_type': 'PLA',
                'filament_amount_grams': 20,
                'layer_height': Decimal('0.20'),
                'infill_percentage': 25,
                'status': 'published'
            },
            {
                'title': 'DNA Model',
                'description': 'An educational DNA double helix model perfect for students and teachers. Shows the structure of DNA in 3D.',
                'category': 'educational',
                'author': 'maker_pro',
                'difficulty': 'intermediate',
                'print_time_hours': 7,
                'filament_type': 'PLA',
                'filament_amount_grams': 90,
                'layer_height': Decimal('0.20'),
                'infill_percentage': 20,
                'status': 'published'
            },
            {
                'title': 'Car Phone Mount',
                'description': 'A sturdy phone mount for your car dashboard. Adjustable angle and secure grip for safe driving.',
                'category': 'automotive',
                'author': 'tech_geek',
                'difficulty': 'intermediate',
                'print_time_hours': 4,
                'filament_type': 'ABS',
                'filament_amount_grams': 50,
                'layer_height': Decimal('0.25'),
                'infill_percentage': 35,
                'status': 'published'
            },
            {
                'title': 'Miniature Chess Set',
                'description': 'A complete chess set with detailed pieces. Perfect for travel or as a decorative piece.',
                'category': 'toys-games',
                'author': 'creative_carol',
                'difficulty': 'advanced',
                'print_time_hours': 15,
                'filament_type': 'PLA',
                'filament_amount_grams': 200,
                'layer_height': Decimal('0.15'),
                'infill_percentage': 15,
                'status': 'featured'
            }
        ]

        created_prints = []
        for print_data in prints_data:
            category = next(cat for cat in categories if cat.slug == print_data['category'])
            author = next(user for user in users if user.username == print_data['author'])
            
            print_item, created = PrintItem.objects.get_or_create(
                title=print_data['title'],
                defaults={
                    'description': print_data['description'],
                    'category': category,
                    'author': author,
                    'difficulty': print_data['difficulty'],
                    'print_time_hours': print_data['print_time_hours'],
                    'filament_type': print_data['filament_type'],
                    'filament_amount_grams': print_data['filament_amount_grams'],
                    'layer_height': print_data['layer_height'],
                    'infill_percentage': print_data['infill_percentage'],
                    'status': print_data['status'],
                    'views_count': random.randint(10, 500),
                    'likes_count': random.randint(0, 50),
                    'downloads_count': random.randint(0, 100),
                }
            )
            created_prints.append(print_item)
            if created:
                self.stdout.write(f'Created print: {print_item.title}')

        # Create some comments
        comments_data = [
            "Great design! Printed perfectly on my Ender 3.",
            "Love this! The quality is amazing.",
            "Had some issues with supports, but overall great model.",
            "Perfect for my project. Thanks for sharing!",
            "Excellent detail and easy to print.",
            "This saved me so much time. Highly recommended!",
            "Beautiful design and very functional.",
            "Printed without any issues. Great work!",
        ]

        for print_item in created_prints[:8]:  # Add comments to first 8 prints
            num_comments = random.randint(1, 4)
            for _ in range(num_comments):
                author = random.choice(users)
                content = random.choice(comments_data)
                
                PrintComment.objects.get_or_create(
                    print_item=print_item,
                    author=author,
                    content=content
                )

        # Create some likes
        for print_item in created_prints:
            num_likes = random.randint(0, 8)
            liked_users = random.sample(users, min(num_likes, len(users)))
            
            for user in liked_users:
                PrintLike.objects.get_or_create(
                    print_item=print_item,
                    user=user
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created:\n'
                f'- {len(categories)} categories\n'
                f'- {len(users)} users\n'
                f'- {len(created_prints)} print items\n'
                f'- {PrintComment.objects.count()} comments\n'
                f'- {PrintLike.objects.count()} likes'
            )
        )
