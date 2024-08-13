from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# API 엔드포인트와 API 키
url = "https://twomiles.openai.azure.com/openai/deployments/gpt4o/chat/completions?api-version=2024-02-15-preview"
api_key = os.getenv('RECOMMEND_API_KEY')

# 요청 헤더
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# 플로깅 장소와 좌표 
plogging_places = {
    "김량쟝역 - 용인중앙시장역": [[37.237293, 127.198671], [37.23789, 27.209046]],
    "용인시청 - 명지대역": [[37.240608, 127.1772935], [37.238043, 127.190298]],
    "고진역 - 보평역": [[37.244643, 127.214168], [37.262406, 127.223526]],
    "수지우체국 - 죽전역": [[37.3211906, 127.0968207], [37.324583, 127.107398]],
    "동천자연식물원 - 동천동우체국": [[37.3372303, 127.0792004], [35.93203889999999, 128.5580582]],
    "홍천말근린공원 - 수지생태공원": [[37.3219386107881, 127.078148702136], [37.324076, 127.0862177]],
    "기흥역 - 강남대역": [[37.275657, 127.115944], [37.270197, 127.126007]],
    "기흥역 - 신갈역": [[37.2782, 127.1265], [37.286127, 127.111311]],
    "구성역 - 보정역": [[37.299013, 127.105664], [37.312747, 127.108232]],
    "남사 시민 야구장 - 이진봉" : [[37.1116777, 127.1635253], [37.1666241, 127.2152553]], 
    "신라초등학교 - 신정공원" : [[37.1116777, 127.1635253], [37.3198793, 127.0943951]],
    "마북 근린공원 - 구성역" : [[37.2979795, 127.1144222], [37.299013, 127.105664]]
}

@app.route('/recommend', methods=['POST'])
def recommend_plogging_place():
    # 요청 데이터 파싱
    data = request.json
    user_query = data.get('user_query')

    # 요청 본문
    api_request_data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": f"""
                너는 아래의 데이터를 기반으로 플로깅 장소를 추천해주는 챗봇이야. 아래의 데이터는 플로깅 출발점, 도착지점이 나와있는 리스트야. 
                해당 플로깅 장소를 사용자가 원하는 조건에 맞게 9개 중 하나 지정해서 추천해주면 돼. 추천해주고 그 장소의 거리 등 설명을 1-2줄 이내로 말해줘.
                
                플로깅 장소 : 
                {json.dumps(plogging_places, ensure_ascii=False)}   
                """
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    }

    # POST 요청 보내기
    response = requests.post(url, headers=headers, data=json.dumps(api_request_data))

    # 메세지 부분만 출력 
    response_data = response.json()
    if 'choices' in response_data and len(response_data['choices']) > 0:
        messages = response_data['choices'][0].get('message', {}).get('content', '')
        return jsonify({"response": messages})
    else:
        return jsonify({"error": "No messages found in the response"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
