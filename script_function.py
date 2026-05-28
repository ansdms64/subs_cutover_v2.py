from olt_class import OLT

olt = OLT(name="Naju-TOD-FR05")

olt.LOOPBACK = "112.190.206.167"
olt.ACT_OLD_SEJ = "SEJ047W"
olt.ACT_OLD_INT = "xe-7/0/1"
olt.ACT_OLD_AE = "ae13"

olt.ACT_NEW_SEJ = "SEJ043W"
olt.ACT_NEW_INT = "xe-4/0/7"
olt.ACT_NEW_AE = "ae47"
olt.ACT_REMOTE_IP = "112.190.209.126"

olt.BK_OLD_SEJ = "SEJ048N"
olt.BK_OLD_INT = "xe-7/2/1"
olt.BK_OLD_AE = "ae23"

olt.BK_NEW_SEJ = "SEJ044N"
olt.BK_NEW_INT = "xe-4/1/7"
olt.BK_NEW_AE = "ae147"
olt.BK_REMOTE_IP = "112.190.210.126"

######################################
olt2 = OLT(name="Neungju-TOD-FR02")

olt2.LOOPBACK = "112.190.206.45"
olt2.ACT_OLD_SEJ = "SEJ048N"
olt2.ACT_OLD_INT = "xe-7/0/3"
olt2.ACT_OLD_AE = "ae18"

olt2.ACT_NEW_SEJ = "SEJ044N"
olt2.ACT_NEW_INT = "xe-7/0/4"
olt2.ACT_NEW_AE = "ae74"
olt2.ACT_REMOTE_IP = "112.190.207.90"

olt2.BK_OLD_SEJ = "SEJ047W"
olt2.BK_OLD_INT = "xe-7/2/3"
olt2.BK_OLD_AE = "ae28"

olt2.BK_NEW_SEJ = "SEJ043W"
olt2.BK_NEW_INT = "xe-7/1/4"
olt2.BK_NEW_AE = "ae174"
olt2.BK_REMOTE_IP = "112.190.208.90"

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
## {olt.BK_NEW_SEJ} Interface 설정 ##

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
print(TITLE_OLT_CONNECT_script(olt=olt2,order=2))
print(BK_OLD_SEJ_to_BK_NEW_SEJ_script_1234(olt=olt2))
print(ACT_OLD_SEJ_to_ACT_NEW_SEJ_script_5678(olt=olt2))
print(ACT_NEW_SEJ_cut_BK_NEW_SEJ_check_script_9(olt=olt2))

print(olt)
print(olt)