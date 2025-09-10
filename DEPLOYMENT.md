# 3D Printing Hub - Deployment Guide

## Local Development

### Prerequisites
- Python 3.10+
- pip

### Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Populate sample data:**
   ```bash
   python manage.py populate_sample_data
   ```

4. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - Main site: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Build and start services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Main site: http://localhost:8000/
   - Admin: http://localhost:8000/admin/ (admin/admin123)

### Manual Docker Build

1. **Build the image:**
   ```bash
   docker build -t 3d-printing-hub .
   ```

2. **Run with MySQL database:**
   ```bash
   docker run -d \
     --name 3d-printing-app \
     -p 8000:8000 \
     -e DATABASE_URL="mysql://root:admin123@your-mysql-host:3306/3d_printing?charset=utf8mb4" \
     -v $(pwd)/media:/app/media \
     3d-printing-hub
   ```

## Environment Variables

### For Container Deployment

Set the `DATABASE_URL` environment variable in your container:

```
DATABASE_URL=mysql://user:password@host:port/database?charset=utf8mb4
```

Example:
```
DATABASE_URL=mysql://root:admin123@mysql:3306/3d_printing?charset=utf8mb4
```

### For Portainer Deployment

1. **Create a new stack**
2. **Add environment variables:**
   - `DATABASE_URL`: `mysql://root:admin123@mysql:3306/3d_printing?charset=utf8mb4`
3. **Deploy the stack**

## Database Configuration

### Local Development
- Uses SQLite by default (`db.sqlite3`)
- No additional setup required

### Production/Container
- Uses MySQL when `DATABASE_URL` is set
- Database will be automatically created and migrated
- Sample data will be populated on first run

## File Structure

```
3d-printing-hub/
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Multi-container setup
├── entrypoint.sh          # Container startup script
├── requirements.txt       # Python dependencies
├── .dockerignore          # Docker build exclusions
├── printing_site/         # Django project
│   ├── settings.py        # Configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
├── prints/               # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── admin.py          # Admin interface
│   └── management/       # Custom commands
├── templates/            # HTML templates
├── static/              # Static files (CSS, JS)
└── media/               # User uploaded files
```

## Production Considerations

### Security
- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Use proper database credentials
- Configure `ALLOWED_HOSTS` properly

### Performance
- Use a reverse proxy (nginx)
- Configure static file serving
- Set up database connection pooling
- Enable caching

### Monitoring
- Set up logging
- Monitor database performance
- Track application metrics

## Troubleshooting

### Common Issues

1. **Database connection errors:**
   - Check MySQL server is running
   - Verify database credentials
   - Ensure database exists

2. **Static files not loading:**
   - Run `python manage.py collectstatic`
   - Check static file configuration

3. **Permission errors:**
   - Check file permissions
   - Ensure proper user/group ownership

### Logs
- Check container logs: `docker logs <container-name>`
- Check Django logs in the application
- Monitor database logs

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify environment variables
3. Test database connectivity
4. Review Django documentation
