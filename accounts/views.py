from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .models import User
from .serializer import UserSerializer
from drf_spectacular.utils import extend_schema


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    """API view for user registration.
    
    Handles user registration requests both HTML form display and JSON API calls.
    No authentication required. Automatically assigns 'student' role to new users.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get(self, request):
        """Display HTML registration form.
        
        Args:
            request: HTTP request object.
        
        Returns:
            HttpResponse: HTML form for user registration.
        """
        html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: #fff;
                color: #333;
            }
            .page-header {
                background: #f5f5f5;
                border-bottom: 1px solid #ddd;
                padding: 10px 20px;
                font-size: 13px;
                color: #666;
            }
            .main {
                padding: 20px 30px;
            }
            h1 {
                font-size: 32px;
                font-weight: bold;
                margin: 0 0 20px 0;
            }
            .url-bar {
                background: #f5f5f5;
                border: 1px solid #ddd;
                padding: 8px 12px;
                font-family: monospace;
                font-size: 13px;
                margin-bottom: 20px;
                color: #333;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                font-size: 13px;
                font-weight: bold;
                margin-bottom: 4px;
                color: #333;
            }
            input {
                width: 30%;
                padding: 6px 10px;
                border: 1px solid #ccc;
                font-size: 13px;
                border-radius: 3px;
                box-sizing: border-box;
            }
            button {
                background-color: #337ab7;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #286090;
            }
        </style>
    </head>
    <body>
        <div class="page-header">Register</div>
        <div class="main">
            <h1>Register</h1>
            <div class="url-bar">POST /api/register/</div>
            <form method="post" action="/api/register/">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username">
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" name="email">
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="text" name="password">
                </div>
                <button type="submit">POST</button>
            </form>
        </div>
    </body>
    </html>
    """
        return HttpResponse(html)

    @extend_schema(request=UserSerializer)
    def post(self, request):
        """Handle user registration submission.
        
        Creates a new user account with the provided credentials.
        Automatically assigns 'student' role to new users.
        
        Args:
            request: HTTP request with username, email, and password.
        
        Returns:
            Response: Success message with status 201 if valid, errors otherwise.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(role='student')
            return Response({'message': 'User Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)