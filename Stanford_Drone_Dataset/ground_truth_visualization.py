import cv2
import time

video_path = "./Videos/deathCircle/video1/video.mov"

cap = cv2.VideoCapture(video_path)

ret = True

frame_number = 0

annotation_file_path = "./annotations/" + video_path.split("/")[2] + "/" + video_path.split("/")[3] + "/" + "annotations.txt"

file_stream = open(annotation_file_path , "r")

fps_time = 0

seek_var = 0

cv2.namedWindow("output" , cv2.WINDOW_NORMAL)
while(ret):

    ret , frame = cap.read()
    # file_stream = open(annotation_file_path , "r")
    for line in file_stream:
        seek_var += len(line)
        print("+"*20)
        print(line)
        print("?"*20)
        print(len(line))
        if(int(line.split(",")[5]) == frame_number):
            # print(frame_number , "Inside at this frame")

            xmin = int(line.split(",")[1])
            ymin = int(line.split(",")[2])
            xmax = int(line.split(",")[3])
            ymax = int(line.split(",")[4])

            if(str(line.split(",")[9]) == "Biker\n"):
                if(int(line.split(",")[6]) == 1):
                    cv2.putText(frame, "lost Biker", (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0) , 2)
                cv2.rectangle(frame,(xmin - 5 , ymin - 10),(xmax,ymax) ,(100 , 0 , 0) , 3)
            elif(str(line.split(",")[9]) == "Pedestrian\n"):
                if(int(line.split(",")[6]) == 1):
                    cv2.putText(frame, "lost Pedestrian", (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0) , 2)
                cv2.rectangle(frame,(xmin - 5 , ymin - 10),(xmax,ymax) ,(0 , 0 , 100) , 3)
            elif(str(line.split(",")[9]) == "Skater\n"): 
                if(int(line.split(",")[6]) == 1):
                    cv2.putText(frame, "lost Scater", (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0) , 2)
                cv2.rectangle(frame,(xmin - 5 , ymin - 10),(xmax,ymax) ,(100 , 200 , 0) , 3)
            elif(str(line.split(",")[9]) == "Cart\n"):
                if(int(line.split(",")[6]) == 1):
                    cv2.putText(frame, "lost Cart", (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0) , 2)  
                cv2.rectangle(frame,(xmin - 5 , ymin - 10),(xmax,ymax) ,(100 , 0 , 0) , 3)
            elif(str(line.split(",")[9]) == "Car\n"):
                if(int(line.split(",")[6]) == 1):
                    cv2.putText(frame, "lost Car", (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0) , 2)
                cv2.rectangle(frame,(xmin - 5 , ymin - 10),(xmax,ymax) ,(100, 0 , 200) , 3)
            elif(str(line.split(",")[9])== "Bus\n"): 
                if(int(line.split(",")[6]) == 1):
                    cv2.putText(frame, "lost Bus", (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0) , 2) 
                cv2.rectangle(frame,(xmin - 5 , ymin - 10),(xmax,ymax) ,(0 , 0 , 0) , 3)

        else:
            break
        
    cv2.putText(frame,
            "FPS: %f" % (1.0 / (time.time() - fps_time)),
            (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (0, 255, 0), 2)
    cv2.putText(frame,
            "Frame number: %f" % frame_number,
            (10, 50),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (0, 0, 255), 2)   
    fps_time = time.time()
    cv2.imshow("output" , frame)
    frame_number +=1
    # print(frame_number)
    k  = cv2.waitKey(0)
    if (k==27):
        break

cv2.destroyAllWindows()
