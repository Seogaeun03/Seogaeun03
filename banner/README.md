# 프로필 배너

320 x 80 원판에 한 점씩 찍고 4배로 키운 움직이는 PNG(APNG)입니다.

```
pip install pillow
python room.py
```

`fonts/` 에 [갈무리](https://github.com/quiple/galmuri) `Galmuri11.ttf`, `Galmuri11-Bold.ttf` 를 넣어야 합니다(부제 글자용, OFL).
결과는 `../assets/banner-room.png` 로 나옵니다.

- `room.py` 방 장면, 말랑이 움직임, 프레임 생성
- `names_en.py` 영문 이름 글자 (획 굵기 3점 고정)
- `names.py` 글자 시안을 만들 때 쓴 도구
