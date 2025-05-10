from django.contrib.messages import constants as messages
from django.contrib import messages
# Helper function to show notifications to users
def notify_user(request, message, level=messages.INFO):
    messages.add_message(request, level, message)
