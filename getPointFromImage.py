from flask import Flask, request, jsonify
import google.generativeai as genai
import PIL.Image
import io

app = Flask(__name__)

def getPointFromImage(api_key: str, image_file: io.BytesIO, model_name: str) -> int:
    # API key
    genai.configure(api_key=api_key)
    
    # Open the image
    sample_file = PIL.Image.open(image_file)
    
    # model
    model = genai.GenerativeModel(model_name=model_name)
    
    prompt = """
        주어진 사진은 쓰레기봉투에 담긴 쓰레기들이 나와있어. 쓰레기가 봉투에 얼만큼 차있는 지 0 ~ 300 범위 내에 정수로만 반환해줘. 불필요한 설명 빼고 숫자만 출력해줘
        """
    
    # Create a prompt and generate content
    response = model.generate_content([prompt, sample_file])
    
    # Return the generated text
    return int(response.text)

@app.route('/process_image', methods=['POST'])
def process_image():
    api_key = request.form.get('api_key')
    model_name = request.form.get("gemini-1.5-pro")
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image_file = request.files['image'] # 여기에 이미지 경로 삽입 
    
    try:
        result = getPointFromImage(api_key, image_file, model_name)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
