import os

def ai_service_url(request):
    ai_host = os.environ.get('AI_SERVICE_HOST', 'localhost:8001')
    if ai_host.startswith('localhost') or ai_host.startswith('127.0.0.1'):
        ai_url = f"http://{ai_host}"
    else:
        # Render internal host looks like "ecofeast-ai-5ywe:10000"
        # We need the public URL for the user's browser!
        base_name = ai_host.split(':')[0] # gets "ecofeast-ai-5ywe"
        if ".onrender.com" not in base_name:
            base_name += ".onrender.com"
        ai_url = f"https://{base_name}"
    return {'AI_SERVICE_URL': ai_url}
