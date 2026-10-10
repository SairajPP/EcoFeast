import os

def ai_service_url(request):
    ai_host = os.environ.get('AI_SERVICE_HOST', 'localhost:8001')
    ai_url = f"https://{ai_host}" if not ai_host.startswith('localhost') and not ai_host.startswith('127.0.0.1') else f"http://{ai_host}"
    return {'AI_SERVICE_URL': ai_url}
