## OLt 1개 절차 작업을 위한 스크립트// ****부분 확인 필요
class OLT:
    """네트워크 OLT 장비 정보를 대문자 변수로 관리하는 클래스"""
    def __init__(self, name: str):
        # 기본 장비 정보
        self.NAME = name
        self.LOOPBACK = None

        # Active (ACT) OLD 정보
        self.ACT_OLD_SEJ = None
        self.ACT_OLD_INT = None
        self.ACT_OLD_AE = None

        # Active (ACT) NEW 정보
        self.ACT_NEW_SEJ = None
        self.ACT_NEW_INT = None
        self.ACT_NEW_AE = None
        self.ACT_REMOTE_IP = None

        # Backup (BK) OLD 정보
        self.BK_OLD_SEJ = None
        self.BK_OLD_INT = None
        self.BK_OLD_AE = None

        # Backup (BK) NEW 정보
        self.BK_NEW_SEJ = None
        self.BK_NEW_INT = None
        self.BK_NEW_AE = None
        self.BK_REMOTE_IP = None

    def __repr__(self):
        # 모든 인스턴스 변수명(대문자)과 값을 일렬로 나열
        lines = [f"{key} = {value}" for key, value in self.__dict__.items()]
        return "\n".join(lines)
# ==========================================
# 사용 예시 (어떻게 쓰나요?)
# ==========================================
# 객체 생성 및 데이터 대입
# olt = OLT(name="Naju-TOD-FR05", loopback="112.190.206.167")
#
# olt.ACT_OLD_SEJ = "SEJ047W"
# olt.ACT_OLD_INT = "xe-7/0/1"
# olt.ACT_OLD_AE = "ae13"
#
# olt.ACT_NEW_SEJ = "SEJ043W"
# olt.ACT_NEW_INT = "xe-4/0/7"
# olt.ACT_NEW_AE = "ae47"
# olt.ACT_REMOTE_IP = "112.190.209.126/30"
#
# olt.BK_OLD_SEJ = "SEJ048N"
# olt.BK_OLD_INT = "xe-7/2/1"
# olt.BK_OLD_AE = "ae23"
#
# olt.BK_NEW_SEJ = "SEJ044N"
# olt.BK_NEW_INT = "xe-4/1/7"
# olt.BK_NEW_AE = "ae147"
# olt.BK_REMOTE_IP = "112.190.210.126/30"

# 출력
