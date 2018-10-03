import cv2
import time
video_path = "/home/uav/Videos/bookstore/video2/video.mov"

cap = cv2.VideoCapture(video_path)

ret = True

step = 3
frame_number = 0

annotation_file_path = "./annotations/" + video_path.split("/")[2] + "/" + video_path.split("/")[3] + "/" + "annotations.txt"

file_stream = open(annotation_file_path , "r")

fps_time = 0
flag = 0
cv2.namedWindow("output" , cv2.WINDOW_NORMAL)
while(ret):
    for i in range(step):
        frame_number+=1
        ret , frame = cap.read()

    if(frame_number == step):
        frame_number -=1
    for line in file_stream:
        if(int(line.split(",")[5]) <= frame_number):

            if(int(line.split(",")[5]) == frame_number):
                xmin = int(line.split(",")[1])
                ymin = int(line.split(",")[2])
                xmax = int(line.split(",")[3])
                ymax = int(line.split(",")[4])

                if(str(line.split(",")[9]) == "Biker\n"):
                    cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(100 , 0 , 0) , 3)
                elif(str(line.split(",")[9]) == "Pedestrian\n"):
                    cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(0 , 0 , 100) , 3)
                elif(str(line.split(",")[9]) == "Skater\n"): 
                    cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(100 , 200 , 0) , 3)
                elif(str(line.split(",")[9]) == "Cart\n"):  
                    cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(100 , 0 , 0) , 3)
                elif(str(line.split(",")[9]) == "Car\n"):
                    cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(100, 0 , 200) , 3)
                elif(str(line.split(",")[9])== "Bus\n"):  
                    cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(0 , 0 , 0) , 3)

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
    # file_stream.seek(0)

    fps_time = time.time()
    cv2.imshow("output" , frame)
    k  = cv2.waitKey(1)  
    if (k==27):
        break

cv2.destroyAllWindows()

# file_stream.seek()




