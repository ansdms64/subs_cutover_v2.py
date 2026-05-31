from olt_class import OLT


def full_name_to_sej(sej_full_name):
    # 대소문자 구분 없이 찾기 위해 모두 대문자로 변환 후 "SEJ"의 시작 위치를 찾습니다.
    # 만약 대소문자를 엄격하게 구분해야 한다면 .upper()를 빼고 "SEJ"나 "sej"로 적으시면 됩니다.
    start_index = sej_full_name.upper().find("SEJ")
    # "SEJ"를 찾지 못한 경우 (-1 반환 시) 빈 문자열 리턴
    if start_index == -1:
        return ""
    # 찾은 위치(start_index)부터 문자열의 끝까지 슬라이싱하여 반환
    return sej_full_name[start_index:]

# 4. 작업순서 - 주요작업사항 - 본작업
def olt_cutover_block(olt,full_name_act_sej,full_name_bkup_sej):

    act_sej = full_name_to_sej(full_name_act_sej)
    bkup_sej = full_name_to_sej(full_name_bkup_sej)
    script = f"""
[{full_name_act_sej} / {full_name_bkup_sej} - {olt} 연동 ] 
- {olt} -> Active 회선 traffic 절체
- {olt} 신규 SEJ 연동을 위한 config 변경
- {bkup_sej}  {olt} 회선(Backup) BGP 연동
- {bkup_sej}  {olt} 회선(Backup) 물리회선 연동 및 테스트 (Ping test, dBm check) , PREMIUM traffic 확인
- {olt} Active -> Backup 회선 traffic 절체(SEJ044N KORNET traffic 인가)
- {act_sej}  {olt} 회선(Active) BGP 연동
- {act_sej}  {olt} 회선(Active) 물리회선 연동 및 테스트 (Ping test, dBm check) , KORNET traffic 확인
- {olt} Backup -> Active 회선으로 PREMIUM traffic 절체 테스트
"""
    return script



print(
    olt_cutover_block(
    olt="Gwangsan-TOD-FK06",
    full_name_act_sej="W.Gwan-SEJ043W",
    full_name_bkup_sej="W.Gwan-SEJ044N",
    )
)
print(
    olt_cutover_block(
    olt="Hanam-TOD-FH10",
    full_name_act_sej="W.Gwan-SEJ044N",
    full_name_bkup_sej="W.Gwan-SEJ043N",
    )
)

olt_2_1 = OLT(name="Naju-TOD-FR05", loopback="112.190.206.167")
olt_2_1.ACT_OLD_SEJ = "SEJ047W"
olt_2_1.ACT_OLD_INT = "xe-7/0/1"
olt_2_1.ACT_OLD_AE = "ae13"

olt_2_1.ACT_NEW_SEJ = "SEJ043W"
olt_2_1.ACT_NEW_INT = "xe-4/0/7"
olt_2_1.ACT_NEW_AE = "ae47"
olt_2_1.ACT_REMOTE_IP = "112.190.209.126/30"

olt_2_1.BK_OLD_SEJ = "SEJ048N"
olt_2_1.BK_OLD_INT = "xe-7/2/1"
olt_2_1.BK_OLD_AE = "ae23"

olt_2_1.BK_NEW_SEJ = "SEJ044N"
olt_2_1.BK_NEW_INT = "xe-4/1/7"
olt_2_1.BK_NEW_AE = "ae147"
olt_2_1.BK_REMOTE_IP = "112.190.210.126/30"

print(olt_2_1)