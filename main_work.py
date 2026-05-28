## OLt 1개 절차 작업을 위한 스크립트// ****부분 확인 필요
class OLT:
    def __init__(self, oltname,oldsej, newsej, oldint, newint, oldae, newae, loopback):
        self.oltname = oltname
        self.oldsej = oldsej
        self.newsej = newsej
        self.oldint = oldint
        self.newint = newint
        self.oldae = oldae
        self.newae = newae
        self.loopback = loopback

    def __repr__(self):
        return (f"OLT(oldsej={self.oldsej!r}, newsej={self.newsej!r}, "
                f"oldint={self.oldint!r}, newint={self.newint!r}, "
                f"oldae={self.oldae!r}, newae={self.newae!r}, "
                f"loopback={self.loopback!r})")


# ==========================================
# 사용 예시 (어떻게 쓰나요?)
# ==========================================
if __name__ == "__main__":
    # 1. OLT 클래스의 인스턴스(객체) 생성
    my_olt = OLT(
        oltname= "oltolt213",
        oldsej="sej_v1",
        newsej="sej_v2",
        oldint="10.1.1.1",
        newint="10.1.1.2",
        oldae="ae1",
        newae="ae2",
        loopback="172.16.0.1"
    )

    # 2. 특정 변수(속성)에 접근하여 출력
    print("--- 개별 변수 확인 ---")
    print(f"Loopback IP: {my_olt.loopback}")
    print(f"New INT: {my_olt.newint}")

    print("\n--- 전체 객체 정보 확인 ---")
    # __repr__ 메서드 덕분에 객체 자체를 출력해도 예쁘게 나옵니다.
    print(my_olt)

def olt_bkup_cutover_block(olt,
                           bkup_sej_old,
                           bkup_sej_new,
                           old_sej_ae,
                           new_sej_ae,
                           olt_loopback,
                           new_sej_int,
                           new_sej_remote_ip
                           ):
    script=f"""
1) {olt} Backup 회선 traffic 제거
## {bkup_sej_old} interface disable ##

*절체 전 트래픽 확인
show interfaces {old_sej_ae} | match rate

*PREMIUM 트래픽 절체

edit

set interfaces {old_sej_ae} disable

show | compare
commit check
commit

## {bkup_sej_old} 확인 ##
run show interfaces {old_sej_ae} | match rate

* {olt} 관련 static deactivate

deactivate routing-options static route {olt_loopback}/32
deactivate routing-options static route 112.191.68.16/30*****
deactivate routing-options static route 112.191.68.48/30*****
deactivate protocols bgp group NTOPIA-PEER neighbor {olt_loopback}

show | compare
commit check
commit

exit

## {bkup_sej_old} 확인 ##
show bgp summary
show route {olt_loopback}/32
show route 112.191.68.16/30*****
show route 112.191.68.48/30*****

2) {olt} 신규 SEJ 연동을 위한 config 변경
[{olt} configuration 작성 필요 / {olt} 에서 진행]
*Interface description 변경
*{bkup_sej_new} lo0 Static 설정
*{bkup_sej_new} BGP neighbor / BGP policy 설정

3) {bkup_sej_new} <-> {olt} 회선(Backup) BGP 연동
## {bkup_sej_new} BGP 설정 ##
edit
activate protocols bgp group ACCESS-PEER neighbor {olt_loopback}

show | compare
commit check
commit

## 확인 ##
run show bgp summary

4) {bkup_sej_new} <-> {olt} 회선(Backup) 물리회선 연동 및 테스트 (Ping test, dBm check) , PREMIUM traffic 확인
[{bkup_sej_new} 물리회선 연동 / disable 설정 삭제 후 PREMIUM 트래픽 인가]
## {bkup_sej_new} interface 설정 ##

delete interfaces {new_sej_ae} disable

show | compare
commit check
commit

exit

## 물리회선 연동 후 확인 ##
show interfaces terse {new_sej_ae}
show interfaces diagnostics optics {new_sej_int} | no-more
clear interfaces statistics {new_sej_int}
ping rapid count 500 size 1000 ttl 1 {new_sej_remote_ip}
show interfaces {new_sej_ae} | match rate
show interfaces {new_sej_int} extensive | match error
show route {olt_loopback}/32
show route 112.191.68.16/30*****
show route 112.191.68.48/30*****
show pim neighbors
show pim interfaces
"""
    return script

dd = olt_bkup_cutover_block(olt="Gwangsan-TOD-FK06",
                           bkup_sej_old="SEJ048N",
                           bkup_sej_new="SEJ044N",
                           old_sej_ae="ae47",
                           new_sej_ae="ae179",
                           olt_loopback="112.190.206.170",
                           new_sej_int="xe-7/1/9",
                           new_sej_remote_ip="112.190.208.158"
                           )
#print(dd)

## ACT회선 절체 단계 5,6,7,8
def olt_act_cutover_block(olt,
                           act_sej_old,
                           act_sej_new,
                           old_sej_ae,
                           new_sej_ae,
                           olt_loopback,
                           new_sej_int,
                           new_sej_remote_ip
                           ):
    script=f"""
5) {olt} Active 회선 traffic 제거

## {act_sej_old} interface disable ##

*절체 전 트래픽 확인
show interfaces {old_sej_ae} | match rate

*KORNET 트래픽 절체

edit

set interfaces {old_sej_ae} disable

show | compare
commit check
commit

## {act_sej_old} 확인 ##
run show interfaces {old_sej_ae} | match rate

* {olt} 관련 static deactivate

deactivate routing-options static route {olt_loopback}/32
deactivate routing-options static route 112.191.68.16/30*****
deactivate routing-options static route 112.191.68.48/30*****
deactivate protocols bgp group NTOPIA-PEER neighbor {olt_loopback}

show | compare
commit check
commit

exit

*{act_sej_old}에서 {olt} 가입자 session clear
clear dhcp relay binding interface {old_sej_ae}

## {act_sej_old} 확인 ##
show dhcp relay binding interface {old_sej_ae} summary
show bgp summary
show route {olt_loopback}/32
show route 112.191.68.16/30*****
show route 112.191.68.48/30*****

6) {olt} 신규 SEJ 연동을 위한 config 변경
[{olt} configuration 작성 필요 / {olt} 에서 진행]
*Interface description 변경
*{act_sej_new} lo0 Static 설정
*{act_sej_new} BGP neighbor / BGP policy 설정

7) {act_sej_new} <-> {olt} 회선(Active) BGP 연동
## {act_sej_new} BGP 설정 ##
edit
activate protocols bgp group ACCESS-PEER neighbor {olt_loopback}
show | compare
commit check
commit

8) {act_sej_new} <-> {olt} 회선(Active) 물리회선 연동 및 테스트 (Ping test, dBm check), KORNET traffic 확인
[{act_sej_new} 물리회선 연동 / disable 설정 삭제 후 KORNET 트래픽 인가]

delete interfaces {new_sej_ae} disable

show | compare
commit check
commit

exit

## 물리회선 연동 후 확인 ##
show interfaces terse {new_sej_ae}
show interfaces diagnostics optics {new_sej_int} | no-more
clear interfaces statistics {new_sej_int}
ping rapid count 500 size 1000 ttl 1 {new_sej_remote_ip}
show interfaces {new_sej_ae} | match rate
show interfaces {new_sej_int} extensive | match error
show route {olt_loopback}/32
show route 112.191.68.16/30*****
show route 112.191.68.48/30*****
show pim neighbors
show pim interfaces
show dhcp relay binding interface {new_sej_ae}
show subscribers summary port
show dhcp relay statistics
show network-access aaa statistics authentication
show network-access aaa statistics accounting 
"""
    return script

print(olt_act_cutover_block(olt="Gwangsan-TOD-FK06" ,
                           act_sej_old="SEJ047W",
                           act_sej_new="SEJ043W",
                           old_sej_ae="ae37",
                           new_sej_ae="ae79",
                           olt_loopback="112.190.206.170",
                           new_sej_int="xe-7/0/9",
                           new_sej_remote_ip="112.190.207.158"
                           ))
## 9.
def final_cutover_block(
    olt,
    act_sej_old,
):
    script = """
    9) Hanam-TOD-FH20 Backup -> Active 회선으로 PREMIUM traffic 절체 테스트
## SEJ043W interface disable ##

edit

set interfaces ae177 disable

show | compare
commit check
commit

[PREMIUM traffic 절체 확인 후]

delete interfaces ae177 disable

show | compare
commit check
commit

exit

## SEJ044N에서 확인 ##
show interfaces ae77 | match rate

    """