from datetime import datetime, time
import logging
import os
from pathlib import Path
from collections import defaultdict
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings
from django.urls import resolve
from django.utils.functional import SimpleLazyObject

logger = logging.getLogger(__name__)

class RolepermissionMiddleware:
    """Middleware to enforce role-based permissions for chat actions."""
    
    ADMIN_ONLY_ACTIONS = [
        'delete_chat',
        'ban_user',
        'edit_settings',
        'view_analytics',
    ]
    
    MODERATOR_ACTIONS = [
        'mute_user',
        'delete_message',
        'view_reports',
    ] + ADMIN_ONLY_ACTIONS  # Moderators can also do admin actions
    
    def __init__(self, get_response):
        self.get_response = get_response

    def _is_admin(self, user):
        """Check if user has admin privileges"""
        return user.is_authenticated and (user.is_staff or user.is_superuser)
    
    def _is_moderator(self, user):
        """Check if user has moderator privileges"""
        return user.is_authenticated and (
            hasattr(user, 'user_role') and 
            getattr(user, 'user_role', '') == 'moderator'
        )
    
    def _get_view_name(self, request):
        """Get the name of the view being accessed"""
        resolver_match = resolve(request.path)
        return resolver_match.url_name if resolver_match else None

    def __call__(self, request):
        """Process the request and check role permissions"""
        view_name = self._get_view_name(request)
        
        # Only check permissions for protected views
        if view_name in self.ADMIN_ONLY_ACTIONS or view_name in self.MODERATOR_ACTIONS:
            user = request.user
            
            if view_name in self.ADMIN_ONLY_ACTIONS and not self._is_admin(user):
                return HttpResponseForbidden("This action requires administrator privileges.")
                
            if view_name in self.MODERATOR_ACTIONS and not (self._is_admin(user) or self._is_moderator(user)):
                return HttpResponseForbidden("This action requires moderator privileges.")
        
        return self.get_response(request)
    
    def _get_view_name(self, request):
        resolver_match = resolve(request.path)
        return resolver_match.url_name if resolver_match else None

    def __call__(self, request):
        view_name = self._get_view_name(request)
        
        # Only check permissions for protected views
        if view_name in self.ADMIN_ONLY_ACTIONS or view_name in self.MODERATOR_ACTIONS:
            user = request.user
            
            if view_name in self.ADMIN_ONLY_ACTIONS and not self._is_admin(user):
                return HttpResponseForbidden("This action requires administrator privileges.")
                
            if view_name in self.MODERATOR_ACTIONS and not (self._is_admin(user) or self._is_moderator(user)):
                return HttpResponseForbidden("This action requires moderator privileges.")
            
        return self.get_response(request)

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
