import sys, os

# 현재 파일(submodule.py)의 부모 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bass import Stamp

class DeployStamp(Stamp) :
    """
    배치 스탬프이다.
    """