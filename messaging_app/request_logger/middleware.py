import logging
import os
from datetime import datetime
from django.conf import settings

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler(settings.REQUEST_LOGGER_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get timestamp at the start of request
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get user information
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        
        # Get request path
        path = request.path
        
        # Log the request
        log_message = f"[{timestamp}] User: {user} - Path: {path}"
        logger.info(log_message)
        
        # Pass the request to the next middleware/view
        response = self.get_response(request)
        
        return response
