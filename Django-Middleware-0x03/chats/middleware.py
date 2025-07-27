from datetime import datetime
import logging
import os
from pathlib import Path

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Configure logging
logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'requests.log'),
    level=logging.INFO,
    format='%(message)s',
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        # Get current timestamp
        timestamp = datetime.now()
        
        # Get user info (anonymous if not authenticated)
        user = request.user.username if request.user.is_authenticated else 'AnonymousUser'
        
        # Log the request
        log_message = f"{timestamp} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        # Process the request
        response = self.get_response(request)

        return response
