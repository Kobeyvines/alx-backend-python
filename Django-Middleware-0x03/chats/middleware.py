from datetime import datetime, time
import logging
import os
from pathlib import Path
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current time
        current_time = datetime.now().time()
        
        # Define allowed time range (9 AM to 6 PM)
        start_time = time(9, 0)  # 9:00 AM
        end_time = time(18, 0)   # 6:00 PM

        # Check if current time is within allowed range
        if not (start_time <= current_time <= end_time):
            return HttpResponseForbidden("Access to chat is only allowed between 9 AM and 6 PM")
        
        return self.get_response(request)

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
