import os
from dotenv import load_dotenv

# .env 불러오기
load_dotenv()
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
AWS_STORAGE_OVERRIDE = os.environ.get('AWS_STORAGE_OVERRIDE') # 기존의 파일을 덮어쓰는 것을 허용할지 여부를 결정
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION') # 서울 리전 주소
myDBid = os.environ.get('DBid')
myDBpw = os.environ.get('DBpw')
mySecretKey = os.environ.get('FLASK_SECRET_KEY')

# db를 저장할 폴더/파일이름 
BASE_DIR = os.path.dirname(__file__)

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'test.db'))
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{myDBid}:{myDBpw}@woori-fisa2.cfnz7hfzq9bn.ap-northeast-2.rds.amazonaws.com/yeonji"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY= mySecretKey

# 또한 디버그모드를 False로 주고 ALLOWED_HOSTS를 '*'로 변경해줍니다.
DEBUG = False
ALLOWED_HOSTS = ['*'] # 모든 ip에서 접근 가능하도록 설정