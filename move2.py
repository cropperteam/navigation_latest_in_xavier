import cv2
from ultralytics import YOLO
import time
import serial
from lidar_package import LidarScanner

# person_class = 0
# model = YOLO("yolov8n.engine",task="detect")
# device="cuda"
# # model.to("cuda")
# cap = cv2.VideoCapture('/dev/video0')

#-----------------------Serial COM Port Connectoin-------------------------------
ser = serial.Serial("/dev/ttyACM0",9600,timeout=0.001)
time.sleep(5)
signal = ""

# ------------------------------YDLIDAR Connection ----------------------------------
# com_port = '/dev/ydlidar'  # Change this to your actual COM port
# scanner = LidarScanner(com_port)

# output_width = 640
# output_height = 480

# # Initialize variables for calculating FPS
# # fps_start_time = time.time()
# # fps_frame_counter = 0
# # frame_counter=0
# # current_fps = 0


def send_signal(signal_to_send):
    global signal


    # ---------------------------- COMMENT THIS PART IF NOT CONNECTED TO SERIAL PORT -------------------------
    if signal_to_send=="F":
        if ser.isOpen():
            ser.write(("F").encode("utf-8"))
            # print("signal sent",signal_to_send)
            # time.delay(2)
            # print("signal sent")
            count = 0
            while True :
                out1 = ser.readline().decode("utf-8")
                # print(out1,len(out1))
                if out1 == "forward\r\n":
                    print(out1,end="")
                    signal = signal_to_send
                    return True
                elif count > 15 :
                    signal = ""
                    print("Not Readline")
                    return False
                count = count + 1
                # print(count)
    elif signal_to_send=="M":
        # global signal
        if ser.isOpen():
            ser.write(("M").encode("utf-8"))
            # print("signal sent",signal_to_send)
            # print("signal sent")
            count = 0
            while True :

                # print("ready to receive")
                out1 = ser.readline().decode("utf-8")
                # print(out1,len(out1))
                if out1 == "leftmove\r\n":
                    print(out1,end="")
                    signal = signal_to_send
                    # print(signal)
                    return True
                elif count > 15 :
                    # ser.write(("Stop").encode("utf-8"))
                    signal = ""
                    print("Not Readline")
                    return False
                count = count + 1
    elif signal_to_send=="N":
        # global signal
        if ser.isOpen():
            ser.write(("N").encode("utf-8"))
            # print("signal sent",signal_to_send)
            count = 0
            while True :
                # print("ready to receive")
                out1 = ser.readline().decode("utf-8")
                # print(out1,len(out1))
                if out1 == "rightmove\r\n":
                    print(out1,end="")
                    signal = signal_to_send
                    # print(signal)
                    return True
                elif count > 15 :
                    # ser.write(("Stop").encode("utf-8"))
                    signal = ""
                    print("Not Readline")
                    return False
                count = count + 1
    elif signal_to_send=="Z":
        # global signal
        if ser.isOpen():
            ser.write(("Z").encode("utf-8"))
            # print("signal sent",signal_to_send)
            # print("signal sent")
            count = 0
            while True :
                # print("ready to receive")
                out1 = ser.readline().decode("utf-8")
                # print(out1,len(out1))
                if out1 == "straight\r\n":
                    print(out1,end="")
                    signal = signal_to_send
                    # print(signal)
                    return True
                elif count > 15 :
                    # ser.write(("Stop").encode("utf-8"))
                    signal = ""
                    print("Not Readline")
                    return False
                count = count + 1
    elif signal_to_send=="B":
        # global signal
        if ser.isOpen():
            ser.write(("B").encode("utf-8"))
            # print("signal sent",signal_to_send)
            # print("signal sent")
            count = 0
            while True :
                # print("ready to receive")
                out1 = ser.readline().decode("utf-8")
                # print(out1,len(out1))
                if out1 == "straight\r\n":
                    print(out1,end="")
                    signal = signal_to_send
                    # print(signal)
                    return True
                elif count > 15 :
                    # ser.write(("Stop").encode("utf-8"))
                    signal = ""
                    print("Not Readline")
                    return False
                count = count + 1
    else:
        # global signal
        if ser.isOpen():
            ser.write((signal_to_send).encode("utf-8"))
            # print("signal sent",signal_to_send)
            # print("signal sent")
            count = 0
            while True :
                # print("ready to receive")
                out1 = ser.readline().decode("utf-8")
                # print(out1,len(out1))
                if out1 == "stop\r\n":
                    print(out1,end="")
                    signal = signal_to_send
                    # print(signal)
                    return True
                elif count > 15 :
                    # ser.write(("Stop").encode("utf-8"))
                    signal = ""
                    print("Not Readline")
                    return False
# frame_counter=0    
# trigger_count=0
while True:
    signal=input("Input -")
    # success, img = cap.read()
    # frame_counter+=1
    # if not success:

    # trigger = scanner.scan()
    # if trigger:
    #     # print("Tigger ",trigger)
    #     if trigger[0]>0:
    #         trigger_count+=1
    #     else:
    #         trigger_count=0
    
    #     if trigger_count>5:
    #         print("Trigger",trigger[0])
    #         send_signal("S")
    #         signal = "S"
    #         trigger_count=0
    # #     break
    # # if frame_counter%5!=0:
    # #     continue
    # img = cv2.resize(img, (output_width, output_height))
    # # else:
    # #     print("Scan failed or no objects detected")
    
    # # Optional: add a small delay to prevent overwhelming the system
    # # time.sleep(0.1)
    # results = model.track(img, persist=True, classes=[person_class], show_labels=True, tracker="bytetrack.yaml", verbose=False,device=0)
    # # results = model.track(img, show_labels=True, verbose=False)
    # # Initialize bounding box coordinates
    # bbox = None
    # for result in results:
    #     for box in result.boxes:
    #         if box.cls == person_class:
    #             bbox = box.xywh.tolist()
    #             break
    #     if bbox:
    #         break

    # # print("frame")
    # # Draw bounding box if it exists
    # if bbox:
    #     # print("bbox")
    #     x, y, w, h = bbox[0]
    #     x, y, w, h = int(x) - int(w)/2, int(y)- int(h)/2, int(w), int(h)
    #     center_bbox = (int(x + w // 2), int(y + h // 2))  # Center of the bounding box

    #     # frame parameters
    #     frame_height, frame_width, _ = img.shape
    #     center_frame = (frame_width // 2, frame_height // 2)  # Center of the frame


    #     # Calculate the displacement of the adjusted bounding box center from the frame center
    #     displacement_x = center_bbox[0] - center_frame[0]
    #     # print("Displacement from center of frame (x):", (displacement_x))

    #     # frame center rectangle
    #     f_center_box_x = center_frame[0] - 50
    #     f_center_box_w = 100
    if signal=="F":
        print("F")
        if ser.isOpen():
            ser.write(("F").encode("utf-8"))
        
        # cnt = 0
        # while not send_signal("F") :
        #     send_signal("F")
        #     cnt = cnt + 1
        #     if cnt > 15:
        #         break


    elif signal == "Z":
        print("Straight")
        if ser.isOpen():
            ser.write(("Z").encode("utf-8"))
        

        # cnt = 0
        # while not send_signal("Z") :
        #     print("Straight")
        #     send_signal("Z")
        #     cnt = cnt + 1
        #     if cnt > 15:
        #         break

    elif signal=="N":
    # if signal != "N" :
        print("Right Forward")
        if ser.isOpen():
            ser.write(("N").encode("utf-8"))
        
            # cnt = 0
            # while not send_signal("N") :
            #     send_signal("N")
            #     cnt = cnt + 1
            #     if cnt > 15:
            #         break

    elif signal == "M":
    # if signa/ != "M":
        print("Left Move")
        if ser.isOpen():
            ser.write(("M").encode("utf-8"))
        
            # cnt = 0
            # while not send_signal("M") :
            #     send_signal("M")
            #     cnt = cnt + 1
            #     if cnt > 15:
            #         break

    elif signal == "B":
    # if signa/ != "M":
        print("Backward")
        if ser.isOpen():
            ser.write(("B").encode("utf-8"))

            # cnt = 0
            # while not send_signal("B") :
            #     send_signal("B")
            #     cnt = cnt + 1
            #     if cnt > 15:
            #         break

    elif signal == "L":
    # if signa/ != "M":
        print("Left")
        if ser.isOpen():
            ser.write(("L").encode("utf-8"))

            # cnt = 0
            # while not send_signal("L") :
            #     send_signal("L")
            #     cnt = cnt + 1
            #     if cnt > 15:
            #         break

    elif signal == "R":
    # if signa/ != "M":
        print("Right")
        if ser.isOpen():
            ser.write(("R").encode("utf-8"))

            # cnt = 0
            # while not send_signal("R") :
            #     send_signal("R")
            #     cnt = cnt + 1
            #     if cnt > 15:
            #         break


    # draw on screen

    elif signal == "S":
        print("Stop")
        if ser.isOpen():
            ser.write(("S").encode("utf-8"))

        # cnt = 0
        # while not send_signal("S") :
        #     send_signal("S")
        #     cnt = cnt + 1
        #     if cnt > 15:
        #         break

        # fps
        # fps_frame_counter += 1
        # if (time.time() - fps_start_time) > 1:
        #     current_fps = fps_frame_counter / (time.time() - fps_start_time)
        #     fps_frame_counter = 0
        #     fps_start_time = time.time()

        # Draw FPS on the frame
        # cv2.putText(img, f"FPS: {int(current_fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 

        # cv2.imshow("MYresult", img)
        # if cv2.waitKey(1) == ord('q'):
        #     print("program terminate")
        #     send_signal("S")
        #     signal = "S"
        #     break
        else:
            if ser.isOpen():
                ser.write(("S").encode("utf-8"))
                break

