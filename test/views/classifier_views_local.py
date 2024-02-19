from flask import Flask, render_template, Blueprint, request

import os
from ..ml_model import classify_img

# 1. Blueprint로 classifier라는 bp를 만들어주세요
classifier = Blueprint("classifier", __name__, url_prefix="/classifier")

@classifier.route("/upload", methods=["GET", "POST"])
def upload_file():
    # 파일이 함께 온 경우 (POST)
    if request.method == "POST":
    # 만약에 파일이 없으면 파일이 없습니다 메시지 출력
        if 'file' not in request.files:
            return "파일이 없습니다", 400
        # 파일이 어떤 방식으로 왔는지 확인
        file = request.files['file']

        # 파일이 있으면 uploads라는 폴더에 해당 파일을 특정 파일명으로 저장 
        file.save(os.path.join('test/static/uploads', file.filename))
        
        print(os.path.join('test/static/uploads'))
        # ml_model.py에 있는 모델 추론 함수를 실행합니다
        result = classify_img(os.path.join('test/static/uploads', file.filename))

        # 그 결과를 화면단에 뿌립니다. 이미지와, 추론결과를 달아서 
        return render_template('ml_model/result.html', result=result, filename=file.filename )
        # 그냥 텅 빈 파일 업로드용 화면을 보내줍니다.

    return render_template("ml_model/upload.html")