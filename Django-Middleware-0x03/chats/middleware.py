from datetime import datetime
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get user info (anonymous if not authenticated)
        user = request.user.username if request.user.is_authenticated else 'AnonymousUser'
        
        # Log the request
        log_message = f"[{timestamp}] User: {user} - Path: {request.path}"
        logger.info(log_message)

        # Process the request
        response = self.get_response(request)

        return response
