import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .engine import get_response


@login_required
def chatbot_view(request):
    return render(request, 'chatbot/index.html')


@login_required
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            if not message:
                return JsonResponse({'error': 'Empty message'}, status=400)
            response = get_response(message)
            return JsonResponse({'success': True, 'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
