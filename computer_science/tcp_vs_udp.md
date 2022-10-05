# TCP & UDP



### TCP와 UDP의 위치

![img](./cs.assets/network_model.png)



- **OSI 7계층**과 **TCP/IP 4계층**은 모두 계층적 네트워크 모델이다.

- OSI 7계층이 역할 기반이라면, TCP/IP 4계층은 프로토콜 기반이다.

- TCP와 UDP는 OSI 7계층과 TCP/IP 4계층에서 모두 **전송 계층**에 해당한다.

<br>

### TCP vs UDP

- TCP는 연결지향형 프로토콜이고, 순서를 보장하며, 데이터의 전송을 보장한다.
  - **가상회선 패킷 교환 방식**을 사용한다.
    - 관련된 패킷을 전부 같은 경로로 전송한다. 따라서 순서가 보장된다.
  
  - HTTP 통신, 이메일, 파일 전송 등에 사용된다.
  - 단, HTTP/3은 UDP를 사용한다.
  
- UDP는 비연결지향형 프로토콜이고, 순서를 보장하지 않으며, 데이터의 전송을 보장하지 않는다.
  - **데이터그램 패킷 교환 방식**을 사용한다.
    - 패킷마다 독립적으로 최적의 경로를 선택한다. 따라서 순서가 보장되지 않는다.

  - 실시간 스트리밍, DNS 등에 사용된다.
    - Q. DNS에서 UDP를 사용하는 이유는 무엇인가?
    - DNS는 신뢰성보다 속도가 더 중요하기 때문이다. 도메인 이름에 해당하는 IP 주소를 못 찾으면, 다시 탐색하면 된다.
    - DNS는 연결 상태를 유지할 필요가 없기 때문이다. 
    - 단, DNS에서는 응답 데이터 크기가 512byte를 넘어가면 TCP를 사용한다.
    - UDP 데이터가 512byte 이하면, DNS 패킷이 전송 중 쪼개졌더라도 다시 재조립될 수 있기 때문이다.
  - 실시간 스트리밍 서비스의 경우에도 많은 경우 TCP를 사용한다.

- UDP는 TCP보다 빠르다.

<br>

### 3-way handshake

> TCP의 연결 성립 과정

1. 클라이언트가 서버에게 요청의 의미로 **SYN** 패킷 전송
   - 임의의 시퀀스 번호인 **ISN**을 담아 보낸다. (ex. 10000)
2. 서버는 클라이언트의 요청을 수락하는 의미로 **SYN + ACK** 플래그 전송
   - 서버 자신의 ISN을 담아 보낸다. (ex. 8000)
   - 클라이언트가 보낸 ISN + 1을 승인번호로 담아 보낸다. (ex. 10001)
3. 클라이언트는 최종 수락의 의미로 **ACK** 플래그 전송
   - 서버가 보낸 ISN + 1을 승인번호로 담아 보낸다. (ex. 8001)

- cf) HTTPS는 3-way handshake 이후, **SSL Handshake**를 함께 진행한다. ([참고 링크](https://github.com/by-gramm/TIL/blob/master/computer_science/hashing_and_encryption.md#ssl-handshake))

<br>

### 4-way handshake

> TCP의 연결 해제 과정

1. 클라이언트가 서버에게 **FIN** 패킷 전송
   - 클라이언트는 `FIN_WAIT_1` 상태가 되어 서버의 응답을 기다린다.
2. 서버는 확인의 의미로 클라이언트에게 **ACK** 패킷으로 답장
   - 서버는 남은 데이터를 마저 보내기 위해 `CLOSE_WAIT` 상태로 전환
   - 패킷을 받은 클라이언트는 `FIN_WAIT_2` 상태로 전환
3. 데이터를 모두 보냈다면, 서버는 **FIN** 패킷을 클라이언트에게 전송
4. 클라이언트는 확인의 의미로 **ACK** 패킷을 서버로 전송
   - 클라이언트는 뒤늦게 도착하는 지연 패킷에 대비하기 위해 `TIME_WAIT` 상태로 전환
   - 이후 서버와 클라이언트는 `CLOSED` 상태가 되고, 클라이언트와 서버의 자원 연결이 해제된다.

<br>

### 참고 출처

https://velog.io/@hidaehyunlee/TCP-%EC%99%80-UDP-%EC%9D%98-%EC%B0%A8%EC%9D%B4

https://serverfault.com/questions/587625/why-dns-through-udp-has-a-512-bytes-limit

https://aws-hyoh.tistory.com/entry/HTTPS-%ED%86%B5%EC%8B%A0%EA%B3%BC%EC%A0%95-%EC%89%BD%EA%B2%8C-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0-3SSL-Handshake

https://ko.wikipedia.org/wiki/%ED%8C%A8%ED%82%B7_%EA%B5%90%ED%99%98
