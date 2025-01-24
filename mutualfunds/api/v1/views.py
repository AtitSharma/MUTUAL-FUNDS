from drf_spectacular.utils import extend_schema

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from mutualfunds.api.v1.serializers import MutualFundsSerializer
from mutualfunds.models import MutualFunds


@extend_schema(
    operation_id="Mutual Funds API",
    summary="MFAS-MF-01",
    description="""
    This API endpoint allows users to manage mutual funds. 
    Users can fetch a list of all mutual funds (GET) or create new mutual fund records (POST).
    The mutual fund data includes important details like the fund's name, NAV (Net Asset Value), and other relevant financial data.
    """,
    request=MutualFundsSerializer,  # Serializer used to handle mutual fund data in the request body for POST requests.
    responses={
        200: MutualFundsSerializer,
        201: {
            "description": "Success: A new mutual fund was created successfully.",
        },
        400: {
            "description": "Bad Request: Invalid mutual fund data provided."
        },
        401: {
            "description": "Unauthorized: User not authenticated to create or view mutual funds."
        }
    }
)
class MutualFundsApiView(APIView):
    """
    API View to handle Mutual Funds operations.

    This view allows fetching all mutual funds (GET) and creating new mutual funds (POST).
    """
    serializer_class = MutualFundsSerializer  # Serializer to handle mutual fund data.

    def get_queryset(self):
        """
        Retrieve all mutual funds from the database.

        Returns:
            QuerySet: A QuerySet containing all mutual funds.
        """
        return MutualFunds.objects.all()

    def get_permissions(self):
        """
        Define permissions for different HTTP methods.

        For GET requests, no permissions are required.
        For other methods, default permissions are applied.

        Returns:
            List: A list of permission classes.
        """
        if self.request.method == "GET":
            self.permission_classes = []
        return super().get_permissions()

    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle POST requests to create a new mutual fund.

        Args:
            request: The HTTP request containing mutual fund data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A Response object containing a success message and the created mutual fund data.
        """

        serializer = self.serializer_class(data=request.data)
        

        serializer.is_valid(raise_exception=True)
        

        serializer.save()
        

        return Response({
            "message": "Mutual Funds Created Successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET requests to fetch all mutual funds.

        Args:
            request: The HTTP request to fetch mutual fund data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A Response object containing a success message and the list of mutual funds.
        """

        queries = self.get_queryset()
        

        serializer = self.serializer_class(queries, many=True)
        

        return Response({
            "message": "Mutual Funds fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
