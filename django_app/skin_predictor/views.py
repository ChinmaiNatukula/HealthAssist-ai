import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .ml import predict_skin_disease


@login_required
def skin_predictor_view(request):
    return render(request, 'skin_predictor/index.html')


@login_required
@csrf_exempt
def predict_view(request):
    if request.method == 'POST':
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image uploaded'}, status=400)
        image = request.FILES['image']
        try:
            result = predict_skin_disease(image)
            return JsonResponse({'success': True, **result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
