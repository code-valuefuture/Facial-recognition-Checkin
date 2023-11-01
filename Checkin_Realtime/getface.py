import cv2
import os

capture = cv2.VideoCapture(0) # Mở camera

# Tạo thư mục để lưu ảnh
dataset_dir = "dataset"
members = ["member1", "member2", "member3"]

# Tạo danh sách để theo dõi trạng thái lưu ảnh của từng thành viên
save_status = {member: False for member in members}

# Trích xuất số lượng ảnh đã lưu trong mỗi thư mục
image_counts = {member: 0 for member in members}

#accessing pretrained model
pretrained_model = cv2.CascadeClassifier("face_detector.xml") 
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

while True:
    boolean, frame = capture.read()
    if boolean == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        coordinate_list = pretrained_model.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3) 
        
        # Vẽ hình chữ nhật trên khuôn mặt
        for (x, y, w, h) in coordinate_list:
            cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (0, 255, 0), 2)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            if roi_color.any() != False:
                # Hiển thị ảnh trên màn hình
                cv2.imshow("Face Image", roi_color)

                # Lưu ảnh khi trạng thái lưu ảnh của thành viên được kích hoạt
                for member in members:
                    if save_status[member]:
                        member_dir = os.path.join(dataset_dir, member)
                        if not os.path.exists(member_dir):
                            os.makedirs(member_dir)
                        
                        image_counts[member] += 1
                        image_path = os.path.join(member_dir, f"{member}{image_counts[member]:04}.jpg")
                        cv2.imwrite(image_path, roi_color)
                        print(f"Đã lưu ảnh cho thành viên: {member}")
                        save_status[member] = False  # Đặt trạng thái lưu ảnh về False
                
        
        # Hiển thị khuôn mặt được phát hiện   
        cv2.imshow("Live Face Detection", frame)
        
        # Kiểm tra phím bấm
        key = cv2.waitKey(1)
        
        if key in [ord(str(i)) for i in range(1, len(members)+1)]:
            # Kích hoạt trạng thái lưu ảnh cho thành viên tương ứng
            member_index = key - ord('1')
            member = members[member_index]
            save_status[member] = True
            print(f"Đang lưu ảnh cho thành viên: {member}")
        
        if key == ord('x'):
            # Hủy lưu ảnh nếu không cần lưu nữa
            for member in members:
                save_status[member] = False
            print("Đã hủy lưu ảnh")
        
        if key == ord('q'):
            # Kết thúc chương trình
            break
        
capture.release()
cv2.destroyAllWindows()
