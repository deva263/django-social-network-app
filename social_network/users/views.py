from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response  # Import Response here
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User, FriendRequest
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, SignupSerializer, PasswordResetSerializer, FriendRequestSerializer, UserSearchSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    User signup view.

    This view handles user registration by taking email, first name, and last name from the request data,
    creating a new user with a random password, and returning the serialized user data.

    :param request: The request object containing user data.
    :return: Response with serialized user data if successful, otherwise errors.
    """
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        
        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(User.objects.make_random_password())
        user.save()
        
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    """
    Password reset view.

    This view handles password reset requests by taking email and new password from the request data,
    updating the user's password if the user exists, and returning a success message.

    :param request: The request object containing email and new password.
    :return: Response with success message if successful, otherwise errors.
    """
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    User login view.

    This view handles user authentication by taking email and password from the request data,
    and returning a token and serialized user data if credentials are valid.

    :param request: The request object containing email and password.
    :return: Response with token and serialized user data if successful, otherwise errors.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    print(f"Email: {email}, Password: {password}, User: {user}")
    if user is not None:
        # Generate or retrieve the token for the authenticated user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_users(request, search_keyword):
    """
    User search view.

    This view handles searching for users by email or name using a search keyword.

    :param request: The request object containing search keyword.
    :param search_keyword: The search keyword for finding users.
    :return: Response with serialized list of users matching the search keyword.
    """
    serializer = UserSearchSerializer(data={'search_keyword': search_keyword})
    if serializer.is_valid():
        search_keyword = serializer.validated_data.get('search_keyword')
        # Perform search by email or name
        users = User.objects.filter(email__icontains=search_keyword) | \
                User.objects.filter(first_name__icontains=search_keyword) | \
                User.objects.filter(last_name__icontains=search_keyword)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny]) 
def send_friend_request(request):
    """
    Send friend request view.

    This view handles sending a friend request from one user to another.

    :param request: The request object containing from_user_id and to_user_id.
    :return: Response with success message if friend request is sent successfully, otherwise errors.
    """
    try:
        # Extract from_user_id and to_user_id from request data
        from_user_id = request.data.get('from_user_id')
        to_user_id = request.data.get('to_user_id')

        friend_request = FriendRequest.objects.create(
            from_user_id=from_user_id,
            to_user_id=to_user_id
        )

        return Response({"detail": "Friend request sent successfully."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def accept_friend_request(request):
    """
    Accept friend request view.

    This view handles accepting a friend request.

    :param request: The request object containing friend_request_id.
    :return: Response with success message if friend request is accepted successfully, otherwise errors.
    """
    friend_request_id = request.data.get('from_user_id')
    if not friend_request_id:
        return Response({"error": "friend_request_id must be provided in the request body."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id)
    except FriendRequest.DoesNotExist:
        return Response({"error": "Friend request does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    friend_request.is_accepted = True
    friend_request.save()
    return Response({"detail": "Friend request accepted successfully."}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def reject_friend_request(request):
    """
    Reject friend request view.

    This view handles rejecting a friend request.

    :param request: The request object containing friend_request_id.
    :return: Response with success message if friend request is rejected successfully, otherwise errors.
    """
    friend_request_id = request.data.get('from_user_id')
    if not friend_request_id:
        return Response({"error": "friend_request_id must be provided in the request body."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id)
    except FriendRequest.DoesNotExist:
        return Response({"error": "Friend request does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    friend_request.delete()
    return Response({"detail": "Friend request rejected successfully."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_friends(request):
    """
    List friends view.

    This view handles listing friends of a user who have accepted the friend request.

    :param request: The request object containing email as a query parameter.
    :return: Response with serialized list of friends if successful, otherwise errors.
    """
    email = request.GET.get('email', '')
    if email:
        try:
            user = User.objects.get(email__iexact=email)
            # Get the list of friends who have accepted the friend request
            friends = User.objects.filter(
                sent_requests__is_accepted=True,
                sent_requests__to_user=user
            )
            friend_list = []
            for friend in friends:
                friend_data = {
                    'id': friend.id,
                    'username': friend.username,
                    'email': friend.email,
                    'first_name': friend.first_name,
                    'last_name': friend.last_name
                }
                friend_list.append(friend_data)
            
            return Response(friend_list, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Please provide an email in the query parameter 'email'."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_pending_friend_requests(request):
    """
    List pending friend requests view.

    This view handles listing pending friend requests for a user.

    :param request: The request object containing email as a query parameter.
    :return: Response with serialized list of pending friend requests if successful, otherwise errors.
    """
    email = request.GET.get('email', '')
    if email:
        try:
            user = User.objects.get(email__iexact=email)
            pending_requests = FriendRequest.objects.filter(to_user=user, is_accepted=False)
            pending_list = []
            for request in pending_requests:
                request_data = {
                    'id': request.id,
                    'from_user': {
                        'id': request.from_user.id,
                        'username': request.from_user.username,
                        'email': request.from_user.email,
                        'first_name': request.from_user.first_name,
                        'last_name': request.from_user.last_name
                    },
                    'created_at': request.created_at
                }
                pending_list.append(request_data)
            
            return Response(pending_list, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Please provide an email in the query parameter 'email'."}, status=status.HTTP_400_BAD_REQUEST)
    
