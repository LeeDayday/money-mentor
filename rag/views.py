import uuid
from .models import ChatbotResponse
from django.http import JsonResponse
from django.utils.timezone import now


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


def submit_response(request):
    """
    사용자의 질문 및 답변 데이터를 데이터베이스에 저장하는 함수.

    - POST 요청으로 전달된 custom_id, question, answer 데이터를 받아 저장.
    - 입력 데이터가 없거나 유효하지 않은 경우 에러 응답 반환.
    """
    if request.method == 'POST':
        import json
        data = json.loads(request.body)

        custom_id = data.get('customId')
        question = data.get('question')
        answer = data.get('answer')

        if not all([custom_id, question, answer]):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        # 데이터 저장
        ChatbotResponse.objects.create(custom_id=custom_id, question=question, answer=answer)
        return JsonResponse({'message': 'Response saved successfully!'})

    return JsonResponse({'error': 'Invalid method'}, status=405)
