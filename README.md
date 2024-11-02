# Image Project

## Description

The **Image Project** is a Django-based web application. Its primary goal is to assist companies that send advertising or any other type of emails to users by enabling the technical team to understand which emails were opened by which users.

### How It Works

- **Email Tracking Mechanism**: The application generates unique tracking images (often 1x1 pixel) embedded in emails. When a user opens an email, their email client requests this image from the server.
- **User Activity Logging**: The server captures the request, logging the user's IP address, user agent, and the specific email associated with the tracking image.
- **Analytics**: This data allows companies to analyze user engagement, tailoring future communications based on insights gained from email open rates.

<details>
<summary><strong>Key Features</strong></summary>

- **Image Upload**: administrators can upload images that are stored with unique identifiers (UUIDs).
- **Dynamic Loading**: Images are served through a dedicated view that handles various URL formats.
- **User Logging**: Each image access logs user details (such as IP address and user agent) to track interactions with email content.
- **Throttling**: The application implements request throttling to prevent abuse and manage server load effectively.
- **Caching**: Cached image data enhances performance by reducing database queries and speeding up retrieval.
- **Django Admin Interface**: Administrators can manage images and logs easily through Django's built-in admin panel.

</details>

<details>
<summary><strong>Technologies Used</strong></summary>

- Django
- PostgreSQL (for database)
- Nginx (as a reverse proxy)
- Docker (for containerization)

</details>

## Installation and Setup (using Docker) <br />

### Prerequisites <br />
Docker and Docker Compose must be installed on your machine. <br />
Steps <br />
Clone the repository: <br />

```
git clone https://github.com/hiddenSm/image-project.git
cd image-project
```

### Environment Variables <br />
create an `.env` file next to the project Dockerfile, and add these to it:

```
## Django settings
DEBUG=False
SECRET_KEY=your_secret_key

## Database settings
DATABASE_NAME=your-db-name
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=your-db-host
DATABASE_PORT=your-db-port

## cache-redis
LOCATION=your-redis-location

## sentry
DSN=your-sentry-dsn (if you have)
```

Build and start the containers: <br />
```
docker-compose up --build
```

Access the application: <br />
===================================

Nginx will be available at `http://localhost:80`. <br />

Admin Panel: <br />
===================================
After running the containers, create a superuser for the Django admin panel: <br />
```
docker-compose exec django-app python manage.py createsuperuser
```
Access the admin panel at [http://localhost:80/admin](http://localhost:80/admin). <br /> 
