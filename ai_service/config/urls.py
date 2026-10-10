from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok", "service": "ecofeast-ai-service"})

urlpatterns = [
    path('', health_check),
    path('admin/', admin.site.urls),
    path('api/ml/', include('ml_service.urls')),
    path('api/genai/', include('genai_service.urls')),
    path('api/rag/', include('rag_service.urls')),
]