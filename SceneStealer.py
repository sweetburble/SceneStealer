import cv2 as cv
import numpy as np

# 카메라 캡처 객체 생성
# stream = cv.VideoCapture('rtmp://210.99.70.120/live/cctv036.stream')
stream = cv.VideoCapture(0)

# 동영상 파일 저장을 위한 설정
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# 레코드 모드 상태
is_recording = False

# contrast, brightness 초기화 
contrast = 1.6
contrast_step = 0.1
brightness = 0
brightness_step = 1

while True:
    # 카메라로부터 영상 읽기
    valid, frame = stream.read()

    if not valid:
        print("영상을 읽을 수 없습니다!")
        break

    # 대비와 밝기 조절
    adjusted_frame = cv.convertScaleAbs(frame, alpha=contrast, beta=brightness)

    # 레코드 모드일 때 화면에 빨간색 원 표시
    if is_recording:
        cv.circle(adjusted_frame, (50, 50), 20, (0, 0, 255), -1)

    # 프레임 표시
    cv.imshow('SceneStealer', adjusted_frame)

    # 레코드 모드이면 동영상 파일에 현재 프레임 저장
    if is_recording:
        out.write(adjusted_frame)

    # 키보드 입력 대기
    key = cv.waitKey(1) & 0xFF

    # Tab 키: 레코드 모드 활성화 / 비활성화
    if key == ord(' '):
        is_recording = not is_recording

    # + 키: 대비 증가
    elif key == ord('+') or key == ord('='):
        contrast += 0.1

    # - 키: 대비 감소
    elif key == ord('-') or key == ord('_'):
        contrast = max(0.1, contrast - 0.1)

    # ] 키: 밝기 증가
    elif key == ord(']') or key == ord('}'):
        brightness += 5

    # [ 키: 밝기 감소
    elif key == ord('[') or key == ord('{'):
        brightness -= 5

    # ESC 키: 프로그램 종료
    elif key == 27:
        break

# 자원 해제
stream.release()
out.release()
cv.destroyAllWindows()