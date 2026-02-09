from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .predictor import FreshnessPredictor

class PredictFreshnessView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Get data from POST request
            data = request.data 
            # Expected keys: storage_time, food_type, storage_condition, etc.
            
            result = FreshnessPredictor.predict(data)
            
            return Response({
                "success": True,
                "prediction": result
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)