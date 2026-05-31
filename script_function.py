from olt_class import OLT

olt1=OLT()
olt1.NAME='S.jeung-TOD-FS10'
olt1.LOOPBACK='112.190.206.160'
olt1.ACT_OLD_SEJ='SEJ047W'
olt1.ACT_OLD_INT='xe-4/1/1'
olt1.ACT_OLD_AE='ae73'
olt1.ACT_NEW_SEJ='SEJ043W'
olt1.ACT_NEW_INT='xe-4/0/4'
olt1.ACT_NEW_AE='ae44'
olt1.ACT_REMOTE_IP='112.190.207.82/30'
olt1.BK_OLD_SEJ='SEJ048N'
olt1.BK_OLD_INT='xe-4/3/1'
olt1.BK_OLD_AE='ae83'
olt1.BK_NEW_SEJ='SEJ044N'
olt1.BK_NEW_INT='xe-4/1/4'
olt1.BK_NEW_AE='ae144'
olt1.BK_REMOTE_IP='112.190.208.82/30'

olt2=OLT()
olt2.NAME='S.jeung-XLG152'
olt2.LOOPBACK='112.190.206.152'
olt2.ACT_OLD_SEJ='SEJ047W'
olt2.ACT_OLD_INT='xe-11/0/1'
olt2.ACT_OLD_AE='ae51'
olt2.ACT_NEW_SEJ='SEJ043W'
olt2.ACT_NEW_INT='xe-7/0/8'
olt2.ACT_NEW_AE='ae78'
olt2.ACT_REMOTE_IP='112.190.209.82/30'
olt2.BK_OLD_SEJ='SEJ048N'
olt2.BK_OLD_INT='xe-11/2/1'
olt2.BK_OLD_AE='ae61'
olt2.BK_NEW_SEJ='SEJ044N'
olt2.BK_NEW_INT='xe-7/1/8'
olt2.BK_NEW_AE='ae178'
olt2.BK_REMOTE_IP='112.190.210.82/30'

olt3=OLT()
olt3.NAME='W.Gwang-OCV002'
olt3.LOOPBACK='112.190.206.2'
olt3.ACT_OLD_SEJ='SEJ048N'
olt3.ACT_OLD_INT='xe-7/1/2'
olt3.ACT_OLD_AE='ae16'
olt3.ACT_NEW_SEJ='SEJ044N'
olt3.ACT_NEW_INT='xe-7/0/7'
olt3.ACT_NEW_AE='ae77'
olt3.ACT_REMOTE_IP='112.190.208.58/30'
olt3.BK_OLD_SEJ='SEJ047W'
olt3.BK_OLD_INT='xe-7/3/2'
olt3.BK_OLD_AE='ae26'
olt3.BK_NEW_SEJ='SEJ043W'
olt3.BK_NEW_INT='xe-7/1/7'
olt3.BK_NEW_AE='ae177'
olt3.BK_REMOTE_IP='112.190.209.58/30'



def get_ip_only(ip_string):
    if not ip_string:
        return ""
    # '/' 문자가 있으면 쪼개서 앞부분만 취하고, 없으면 그대로 반환
    return str(ip_string).split('/')[0].strip()
def get_ip_only_olt(olt:OLT):
    olt.LOOPBACK = get_ip_only(olt.LOOPBACK)
    olt.ACT_REMOTE_IP = get_ip_only(olt.ACT_REMOTE_IP)
    olt.BK_REMOTE_IP = get_ip_only(olt.BK_REMOTE_IP)
    return olt

# print(olt)
def TITLE_OLT_CONNECT_script(olt:OLT,order:int):
    script=f'''
{order}.{olt.NAME}연동\n
가. {olt.NAME}연동
    '''
    return script

def BK_OLD_SEJ_to_BK_NEW_SEJ_script_1234(olt:OLT):
    script =f'''
1) {olt.NAME} Backup 회선 Traffic 제거
## {olt.BK_OLD_SEJ} interface disable ##

*절체 전 트래픽 확인
show interfaces {olt.BK_OLD_AE} | match rate

*PREMIUM 트래픽 절체

edit

set interfaces {olt.BK_OLD_AE} disable

show | compare
commit check
commit

## {olt.BK_OLD_SEJ} 확인 ##
run show interfaces {olt.BK_OLD_AE} | match rate

* {olt.NAME} 관련 static deactivate
deactivate routing-options static route {olt.LOOPBACK}/32
deactivate protocols bgp group NTOPIA-PEER neighbor {olt.LOOPBACK}

show | compare
commit check
commit

exit

## {olt.BK_OLD_SEJ} 확인 ##
show bgp summary
show route {olt.LOOPBACK}/32

2) {olt.NAME} 신규 SEJ 연동을 위한 config 변경
[{olt.NAME} configuration 작성 필요 / {olt.NAME} 에서 진행]
*Interface description 변경
*{olt.BK_NEW_SEJ} lo0 Static 설정
*{olt.BK_NEW_SEJ} BGP neighbor / BGP policy 설정

3) {olt.BK_NEW_SEJ} <-> {olt.NAME} 회선(Backup) BGP 연동
## {olt.BK_NEW_SEJ} BGP 설정 ##
edit
activate protocols bgp group ACCESS-PEER neighbor {olt.LOOPBACK}

show | compare
commit check
commit

## 확인 ##
run show bgp summary

4) {olt.BK_NEW_SEJ} <-> {olt.NAME} 회선(Backup) 물리회선 연동 및 테스트 (Ping test, dBm check) , PREMIUM traffic 확인
[{olt.BK_NEW_SEJ} 물리회선 연동 / disable 설정 삭제 후 PREMIUM 트래픽 인가]
## {olt.BK_NEW_SEJ} interface 설정 ##

delete interfaces {olt.BK_NEW_AE} disable

show | compare
commit check
commit

exit

## 물리회선 연동 후 확인 ##
show interfaces terse {olt.BK_NEW_AE}
show interfaces diagnostics optics {olt.BK_NEW_INT} | no-more
clear interfaces statistics {olt.BK_NEW_INT}
ping rapid count 500 size 1000 ttl 1 {olt.BK_REMOTE_IP}
show interfaces {olt.BK_NEW_AE} | match rate
show interfaces {olt.BK_NEW_INT} extensive | match error
show route {olt.LOOPBACK}/32
show pim neighbors
show pim interfaces

    '''
    return script

def ACT_OLD_SEJ_to_ACT_NEW_SEJ_script_5678(olt:OLT):
    script =f'''
5) {olt.NAME} Active 회선 traffic 제거

## {olt.ACT_OLD_SEJ} interface disable ##

*절체 전 트래픽 확인
show interfaces {olt.ACT_OLD_AE} | match rate

*KORNET 트래픽 절체

edit

set interfaces {olt.ACT_OLD_AE} disable

show | compare
commit check
commit

## {olt.ACT_OLD_SEJ} 확인 ##
run show interfaces {olt.ACT_OLD_AE} | match rate

* {olt.NAME} 관련 static deactivate

deactivate routing-options static route {olt.LOOPBACK}/32
deactivate protocols bgp group NTOPIA-PEER neighbor {olt.LOOPBACK}

show | compare
commit check
commit

exit

*{olt.ACT_OLD_SEJ} 에서 {olt.NAME} 가입자 session clear
clear dhcp relay binding interface {olt.ACT_OLD_AE}

## {olt.ACT_OLD_SEJ} 확인 ##
show dhcp relay binding interface {olt.ACT_OLD_AE} summary
show bgp summary
show route {olt.LOOPBACK}/32

6) {olt.NAME} 신규 SEJ 연동을 위한 config 변경
[{olt.NAME} configuration 작성 필요 / {olt.NAME} 에서 진행]
*Interface description 변경
*{olt.ACT_NEW_SEJ} lo0 Static 설정
*{olt.ACT_NEW_SEJ} BGP neighbor / BGP policy 설정


7) {olt.ACT_NEW_SEJ} <-> {olt.NAME} 회선(Active) BGP 연동
## {olt.ACT_NEW_SEJ} BGP 설정 ##
edit
activate protocols bgp group ACCESS-PEER neighbor {olt.LOOPBACK}

show | compare
commit check
commit

8) {olt.ACT_NEW_SEJ} <-> {olt.NAME} 회선(Active) 물리회선 연동 및 테스트 (Ping test, dBm check) , KORNET traffic 확인
[{olt.ACT_NEW_SEJ} 물리회선 연동 / disable 설정 삭제 후 KORNET 트래픽 인가]

delete interfaces {olt.ACT_NEW_AE} disable

show | compare
commit check
commit

exit

## 물리회선 연동 후 확인 ##
show interfaces terse {olt.ACT_NEW_AE}
show interfaces diagnostics optics {olt.ACT_NEW_INT} | no-more
clear interfaces statistics {olt.ACT_NEW_INT}
ping rapid count 500 size 1000 ttl 1 {olt.ACT_REMOTE_IP}
show interfaces {olt.ACT_NEW_AE} | match rate
show interfaces {olt.ACT_NEW_INT} extensive | match error
show route {olt.LOOPBACK}/32
show pim neighbors
show pim interfaces
show dhcp relay binding interface {olt.ACT_NEW_AE}
show subscribers summary port
show dhcp relay statistics
show network-access aaa statistics authentication
show network-access aaa statistics accounting
'''
    return script

def ACT_NEW_SEJ_cut_BK_NEW_SEJ_check_script_9(olt:OLT):
    script = f'''
9) {olt.NAME} Backup -> Active 회선으로 PREMIUM traffic 절체 테스트
## {olt.BK_NEW_SEJ} interface disable ##

edit

set interfaces {olt.BK_NEW_AE} disable

show | compare
commit check
commit

[PREMIUM traffic 절체 확인 후]

delete interfaces {olt.BK_NEW_AE} disable

show | compare
commit check
commit

exit

## {olt.ACT_NEW_SEJ}에서 확인 ##
show interfaces {olt.ACT_NEW_AE} | match rate

'''
    return script

def MAIN_WORK_FULL_SCRIPT(olt:OLT,order:int):
    olt = get_ip_only_olt(olt)
    title = TITLE_OLT_CONNECT_script(olt=olt,order=order)
    script1234 = BK_OLD_SEJ_to_BK_NEW_SEJ_script_1234(olt=olt)
    script5678 = ACT_OLD_SEJ_to_ACT_NEW_SEJ_script_5678(olt=olt)
    script9 = ACT_NEW_SEJ_cut_BK_NEW_SEJ_check_script_9(olt=olt)
    full_script = f'''
        {title}
        {script1234}
        {script5678}
        {script9}
        '''
    return full_script


import re


def search_lines_by_value(file_path, search_dict):
    """
    파일을 읽어 search_dict에 정의된 값을 포함하는 라인을 찾습니다.
    """
    found_data = {key: [] for key in search_dict.keys()}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            for label, value in search_dict.items():
                # re.escape를 사용하여 IP 주소의 '.' 등을 일반 문자로 처리
                # 예: 192.168.0.1 -> 192\.168\.0\.1
                pattern = re.compile(re.escape(str(value)))

                # 해당 값을 포함하는 모든 라인 추출
                found_data[label] = [line.strip() for line in lines if pattern.search(line)]

    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return None

    return found_data


def FIND_DEACTIVATE_IP_SCRIPT(olt, file_act, file_bk):
    olt = get_ip_only_olt(olt)
    # 1. ACT 관련 검색 대상 설정
    act_targets = {
        'ACT_REMOTE_IP': olt.ACT_REMOTE_IP,
        'ACT_LOOPBACK': olt.LOOPBACK
    }

    # 2. BK 관련 검색 대상 설정
    bk_targets = {
        'BK_REMOTE_IP': olt.BK_REMOTE_IP,
        'BK_LOOPBACK': olt.LOOPBACK
    }

    # 3. 파일 검색 실행
    act_results = search_lines_by_value(file_act, act_targets)
    bk_results = search_lines_by_value(file_bk, bk_targets)
    print(f"ACT={file_act}///BK={file_bk}")
    print(f"LOOPBACK={olt.LOOPBACK}\nACT_REMOTE_IP={olt.ACT_REMOTE_IP}\nBK_REMOTE_IP={olt.BK_REMOTE_IP}")

    return {
        "ACT_FILE_RESULTS": act_results,
        "BK_FILE_RESULTS": bk_results
    }
# 함수 실행
results = FIND_DEACTIVATE_IP_SCRIPT(olt3, "W.Gwan-SEJ047W_사전자료 copy.txt", "W.Gwang-SEJ048N_사전자료 copy.txt")

# 결과 확인
for file_key, data in results.items():
    print(f"--- {file_key} ---")
    for var_name, lines in data.items():
        print(f"변수 [{var_name}] 관련 라인:")
        for line in lines:
            print(f"  > {line}")
print("#########################거꾸로###################")
results = FIND_DEACTIVATE_IP_SCRIPT(olt3, "W.Gwang-SEJ048N_사전자료 copy.txt", "W.Gwan-SEJ047W_사전자료 copy.txt")

# 결과 확인
for file_key, data in results.items():
    print(f"--- {file_key} ---")
    for var_name, lines in data.items():
        print(f"변수 [{var_name}] 관련 라인:")
        for line in lines:
            print(f"  > {line}")