import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .ml import predict_disease, ALL_SYMPTOMS


@login_required
def symptom_checker_view(request):
    return render(request, 'symptom_checker/index.html', {
        'all_symptoms': json.dumps(ALL_SYMPTOMS),
    })


@login_required
@csrf_exempt
def predict_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            symptoms = data.get('symptoms', [])
            result, confidence = predict_disease(symptoms)
            return JsonResponse({
                'success': True,
                'disease': result['disease'],
                'description': result['description'],
                'next_steps': result['next_steps'],
                'severity': result['severity'],
                'icon': result['icon'],
                'confidence': confidence,
                'symptoms_analyzed': symptoms,
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
