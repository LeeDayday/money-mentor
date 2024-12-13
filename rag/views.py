import uuid
from .models import ChatbotResponse
from django.http import JsonResponse
from django.utils.timezone import now
import json
import os
from django.conf import settings

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def generate_id(request):
    """
    사용자에게 고유 ID를 생성하여 반환하는 함수.

    - 현재 시간(년월일시분)과 랜덤한 고유 값을 조합하여 custom_id 생성.
    - 생성된 custom_id는 사용자를 구분하는 데 사용.
    """
    timestamp = now().strftime("%Y%m%d%H%M")
    unique_id = str(uuid.uuid4())[:6]  # 고유한 ID 생성
    custom_id = f"{timestamp}{unique_id}"
    return JsonResponse({'customId': custom_id})


# 질문 로드
def get_questions(request):
    """
    JSON 파일에서 질문 데이터를 로드하여 반환하는 함수
    """
    try:
        file_path = os.path.join(settings.BASE_DIR, 'static', 'survey_questions.json')
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            questions = json.load(file)
        return JsonResponse(questions, safe=False)
    except FileNotFoundError:
        return JsonResponse({'error': 'Questions file not found.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format in the questions file.'}, status=500)


@csrf_exempt
def submit_response(request):
    """
    사용자 답변을 데이터베이스에 저장하는 함수
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # 요청 데이터를 JSON으로 파싱
            custom_id = data.get('customId')  # 사용자 ID
            responses = data.get('responses')  # 질문과 답변 데이터
            if not custom_id or not responses:
                return JsonResponse({'error': 'Invalid data'}, status=400)

            # 데이터 저장 또는 업데이트
            ChatbotResponse.objects.update_or_create(
                custom_id=custom_id,
                defaults={'responses': responses}
            )

            return JsonResponse({'message': 'Responses saved successfully!'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)


# HTML 렌더링
def chatbot_interface(request):
    return render(request, 'chatbot.html')
