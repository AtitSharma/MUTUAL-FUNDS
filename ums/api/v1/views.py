from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from ums.api.v1.serializers import (CustomTokenRefreshSerializer, 
                                    InvestmentSerializer,
                                      ReportGenerationListSerializer,
                                        UserLoginSerializer, 
                                        UserRegisterSerializer)
from ums.models import UserInvestment
from drf_spectacular.utils import extend_schema


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer

class UserRegisterApiView(APIView):
    """
    API View to handle user registration.

    This view allows new users to register by sending their details in a POST request.
    """
    permission_classes: list = [] 
    serializer_class = UserRegisterSerializer  


    @extend_schema(
        operation_id="User Register API.",
        summary="MFAS-UMS-01",
        description="""
        This api Creates User .  Handle POST requests to register a new user.
        """,
        request=UserRegisterSerializer,
        responses=UserRegisterSerializer
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle POST requests to register a new user.

        Args:
            request: The HTTP request containing user registration data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A Response object containing a success message and the registered user data.
        """
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "User Registered Successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    

class UserLoginApiView(APIView):
    """
    API View to handle user login.

    This view allows users to log in by sending their credentials in a POST request.
    """
    permission_classes: list = []  
    serializer_class = UserLoginSerializer  


    @extend_schema(
        operation_id="User Login API.",
        summary="MFAS-UMS-02",
        description="""
        This API endpoint allows users to log in by providing their credentials (username and password).
        On successful authentication, the user will receive a JWT token or session token that can be used for subsequent requests.
        """,
        request=UserLoginSerializer,
        responses={
            200: UserLoginSerializer,  
            401: "Unauthorized: Incorrect credentials", 
            400: "Bad Request: Missing or invalid parameters" 
        }
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle POST requests to log in a user.

        Args:
            request: The HTTP request containing user login data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A Response object containing a success message and the validated login data.
        """

        serializer = self.serializer_class(data=request.data)
        

        serializer.is_valid(raise_exception=True)
        
        return Response({
            "message": "User Login Successfully",
            "data": serializer.validated_data
        }, status=status.HTTP_200_OK)

    

class GetNewAccessTokenSerializer(APIView):
    """
    API View to refresh and fetch a new access token.

    This view allows users to send their refresh token and obtain a new access token.
    """
    permission_classes: list = [] 
    serializer_class = CustomTokenRefreshSerializer 

    @extend_schema(
        operation_id="Refresh Access Token API",
        summary="MFAS-UMS-03",
        description="""
        This API endpoint allows users to refresh their access token by providing a valid refresh token. 
        Upon successful validation of the refresh token, a new access token will be generated and returned. 
        This is useful for keeping user sessions active without requiring them to log in again.
        """,
        request=CustomTokenRefreshSerializer,  # Serializer for handling the refresh token in the request body.
        responses={
            200: {
                "description": "Successfully refreshed access token.",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Access token fetched successfully",
                            "data": {
                                "access_token": "<new_access_token_here>"
                            }
                        }
                    }
                }
            },
            400: {
                "description": "Bad request: The refresh token is invalid or missing."
            },
            401: {
                "description": "Unauthorized: The refresh token has expired or is invalid."
            }
        }
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle POST requests to refresh and fetch a new access token.

        Args:
            request: The HTTP request containing the refresh token.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A Response object containing a success message and the new access token.
        """
        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        return Response({
            "message": "Access token fetched successfully",
            "data": serializer.validated_data
        }, status=status.HTTP_200_OK)





@extend_schema(
    operation_id="User Investment API",
    summary="MFAS-UMS-04",
    description="""
    This API endpoint allows users to manage their investments, including performing READ AND POST operations 
    The investments are associated with mutual funds and users.
    """,
    request=InvestmentSerializer,  # Serializer used for handling investment data in the request body.
    responses={
        200: {
            "description": "Success: Investment data uploaded or fetched successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Investment Uploaded Successfully",
                        "data": {
                            "investment_id": 123,
                            "user": "user_id",
                            "mutual_fund": "mutual_fund_id",
                            "amount_invested": 1000.0,
                            "date_invested": "2025-01-01"
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad Request: Invalid investment data provided."
        },
        401: {
            "description": "Unauthorized: User not authenticated to access or modify the investment data."
        }
    }
)
class InvestmentApiView(APIView):
    """
    API View to handle user investments.

    This view allows users to perform CRUD operations on their investments.
    """
    serializer_class = InvestmentSerializer  # Serializer to handle investment data.

    def get_queryset(self):
        """
        Get the queryset of the user's investments.

        Returns:
            QuerySet: A QuerySet containing the user's investments, including related user and mutual fund data.
        """
        return UserInvestment.objects.select_related("user", "mutual_fund").filter(user=self.request.user).values()
    

    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle POST requests to upload a new investment.

        Args:
            request: The HTTP request containing investment data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A Response object containing a success message and the uploaded investment data.
        """

        serializer = self.serializer_class(data=request.data, context={"request": request})
        

        serializer.is_valid(raise_exception=True)
        

        serializer.save()
        

        return Response({
            "message": "Investment Uploaded Successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET requests to fetch user investments.

        Args:
            request: The HTTP request to fetch investment data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A Response object containing a success message and the user's investment data.
        """

        user_investment = self.get_queryset()
        

        serializer = self.serializer_class(user_investment, many=True)
        

        return Response({
            "message": "User's Investment Fetched Successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    
class ReportGenerationListApiView(APIView):
    """
    API View to generate a detailed report of user investments.

    This view fetches the user's investments and includes computed fields like 
    mutual fund name, total units, NAV, and total value.
    """
    serializer_class = ReportGenerationListSerializer  # Serializer to handle the report generation data.

    def get_queryset(self):
        """
        Retrieve and annotate the user's investment data.

        This method fetches the user's investments and annotates each record with additional fields:
        - mutual_fund_name: The name of the associated mutual fund.
        - total_units: The total units invested.
        - nav: The net asset value (NAV) of the mutual fund.
        - total_value: The total value of the investment (NAV * units).

        Returns:
            QuerySet: Annotated QuerySet of user investments.
        """
        return UserInvestment.objects.select_related('user', 'mutual_fund').filter(
            user=self.request.user
        ).annotate(
            mutual_fund_name=F('mutual_fund__name'),
            total_units=F('units'),
            nav=F('mutual_fund__nav'),
            total_value=F('mutual_fund__nav') * F('units')
        ).values()


    @extend_schema(
        operation_id="User Investment Report Generation API",
        summary="MFAS-UMS-05",
        description="""
        This API endpoint generates a detailed report of the user's investments. 
        The report includes important fields such as mutual fund names, 
        total units invested, NAV (Net Asset Value) of the mutual fund, 
        and the total value of the user's investments (NAV * total units).
        This endpoint helps users to get a quick overview of their investment portfolio.
        """,
        request=None,  # No request body is needed for GET request, as it’s a report fetching operation.
        responses={
            200: {
                "description": "Success: Investment report generated successfully.",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Report Generated Successfully",
                            "data": [
                                {
                                    "mutual_fund_name": "Mutual Fund A",
                                    "total_units": 100,
                                    "nav": 10.5,
                                    "total_value": 1050.0
                                },
                                {
                                    "mutual_fund_name": "Mutual Fund B",
                                    "total_units": 200,
                                    "nav": 12.3,
                                    "total_value": 2460.0
                                }
                            ]
                        }
                    }
                }
            },
            401: {
                "description": "Unauthorized: User not authenticated to fetch the report."
            },
            404: {
                "description": "Not Found: No investments found for the user."
            }
        }
    )
    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET requests to generate a report of user investments.

        Args:
            request: The HTTP request to fetch the report data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A Response object containing a success message and the annotated investment data.
        """
        
        query = self.get_queryset()
        
       
        serializer = self.serializer_class(query, many=True)
        
        
        return Response({
            "message": "Report Generated Successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
