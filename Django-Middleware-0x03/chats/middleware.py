from datetime import datetime, time
import logging
import os
from pathlib import Path
from collections import defaultdict
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 5  # messages per minute
        self.time_window = 60  # 1 minute in seconds

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    def __call__(self, request):
        # Only check rate limit for POST requests to message endpoints
        if request.method == 'POST' and '/chats/' in request.path:
            client_ip = self._get_client_ip(request)
            cache_key = f'message_count_{client_ip}'
            
            # Get current message count and timestamp from cache
            message_data = cache.get(cache_key)
            current_time = datetime.now().timestamp()
            
            if message_data is None:
                # First message from this IP
                cache.set(cache_key, {
                    'count': 1,
                    'window_start': current_time
                }, self.time_window)
            else:
                # Check if we're in a new time window
                if current_time - message_data['window_start'] > self.time_window:
                    # Reset for new time window
                    cache.set(cache_key, {
                        'count': 1,
                        'window_start': current_time
                    }, self.time_window)
                else:
                    # Still in current window, check rate limit
                    if message_data['count'] >= self.rate_limit:
                        return HttpResponseForbidden(
                            f"Rate limit exceeded. Maximum {self.rate_limit} messages per {self.time_window} seconds."
                        )
                    # Increment message count
                    cache.set(cache_key, {
                        'count': message_data['count'] + 1,
                        'window_start': message_data['window_start']
                    }, self.time_window)

        return self.get_response(request)

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
