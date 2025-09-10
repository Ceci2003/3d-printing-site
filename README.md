# 3D Printing Hub - Django Demo App

A comprehensive Django web application for sharing and discovering 3D printing designs. This demo showcases a modern, responsive interface for browsing prints, managing categories, and interacting with the community.

## Features

### 🎯 Core Functionality
- **Print Discovery**: Browse and search through 3D printing designs
- **Category Management**: Organize prints by categories (Toys, Home & Garden, Art, etc.)
- **User Interaction**: Like prints, leave comments, and track statistics
- **Advanced Filtering**: Filter by category, difficulty, and sort by popularity/date
- **Responsive Design**: Modern UI that works on all devices

### 🛠️ Technical Features
- **Django Admin**: Full admin interface for content management
- **User Authentication**: Built-in user system with Django's auth
- **File Management**: Support for STL files and images
- **Database Models**: Comprehensive models for prints, categories, comments, and likes
- **RESTful URLs**: Clean, SEO-friendly URL structure

### 🎨 UI/UX Features
- **Modern Bootstrap Design**: Clean, professional interface
- **Interactive Elements**: Smooth animations and hover effects
- **Mobile Responsive**: Optimized for all screen sizes
- **Accessibility**: Proper ARIA labels and keyboard navigation
- **Performance**: Optimized queries and lazy loading

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd "D:\3D printing\Website"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser account**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate with sample data**
   ```bash
   python manage.py populate_sample_data
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
printing_site/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── printing_site/           # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── prints/                  # Main application
│   ├── __init__.py
│   ├── admin.py            # Admin interface configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # App URL patterns
│   └── management/         # Custom management commands
│       └── commands/
│           └── populate_sample_data.py
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   └── prints/             # App-specific templates
│       ├── home.html
│       ├── print_list.html
│       ├── print_detail.html
│       └── category_detail.html
└── static/                 # Static files (CSS, JS, images)
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Database Models

### PrintItem
- **Title & Description**: Basic print information
- **Category**: Classification system
- **Author**: User who uploaded the print
- **Print Specifications**: Time, filament, layer height, infill
- **Media**: Main image and STL file
- **Statistics**: Views, likes, downloads
- **Status**: Draft, Published, Featured

### Category
- **Name & Description**: Category information
- **Slug**: URL-friendly identifier
- **Print Count**: Number of prints in category

### PrintComment
- **Content**: Comment text
- **Author**: User who commented
- **Timestamps**: Created and updated dates

### PrintLike
- **User & Print**: Many-to-many relationship
- **Timestamp**: When the like was created

## Admin Interface

The Django admin provides comprehensive management tools:

- **Print Management**: Create, edit, and organize prints
- **Category Management**: Manage print categories
- **User Management**: Handle user accounts
- **Comment Moderation**: Review and manage comments
- **Statistics**: View engagement metrics

Access the admin at `/admin/` after creating a superuser account.

## Customization

### Adding New Categories
1. Go to Admin → Categories → Add Category
2. Fill in name, description, and slug
3. Save to make it available immediately

### Modifying Print Specifications
Edit the `PrintItem` model in `prints/models.py` to add new fields like:
- Print bed temperature
- Nozzle temperature
- Support requirements
- Post-processing notes

### Styling Changes
- **CSS**: Modify `static/css/style.css`
- **JavaScript**: Update `static/js/main.js`
- **Templates**: Edit files in `templates/prints/`

## Sample Data

The `populate_sample_data` command creates:
- 8 categories (Toys, Home & Garden, Art, etc.)
- 5 sample users
- 12 diverse print items
- Comments and likes for engagement

To clear and repopulate:
```bash
python manage.py populate_sample_data --clear
```

## Development Tips

### Adding New Features
1. **Models**: Define in `prints/models.py`
2. **Admin**: Register in `prints/admin.py`
3. **Views**: Create in `prints/views.py`
4. **URLs**: Add patterns in `prints/urls.py`
5. **Templates**: Create HTML files in `templates/prints/`

### Database Changes
After modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files
For production, collect static files:
```bash
python manage.py collectstatic
```

## Next Steps for Main Application

This demo provides a solid foundation for a full 3D printing platform. Consider adding:

### Enhanced Features
- **User Profiles**: Detailed user pages with print collections
- **Print Upload**: File upload interface for users
- **Print Collections**: User-created collections and favorites
- **Advanced Search**: Full-text search with filters
- **Print History**: Track user's printing history
- **Rating System**: Star ratings for prints
- **Print Variations**: Different sizes and modifications

### Technical Improvements
- **API Endpoints**: REST API for mobile apps
- **Real-time Features**: WebSocket for live updates
- **File Processing**: Automatic STL analysis and preview generation
- **CDN Integration**: Optimized file delivery
- **Caching**: Redis for improved performance
- **Search Engine**: Elasticsearch for advanced search

### Community Features
- **Forums**: Discussion boards for each print
- **Print Challenges**: Community contests and events
- **Collaboration**: Multi-user print projects
- **Reviews**: Detailed print reviews with photos
- **Tutorials**: Step-by-step printing guides

## Support

For questions or issues with this demo:
1. Check the Django documentation: https://docs.djangoproject.com/
2. Review the code comments for implementation details
3. Test with the sample data to understand functionality

## License

This is a demo application for educational purposes. Feel free to use and modify as needed for your 3D printing platform.
