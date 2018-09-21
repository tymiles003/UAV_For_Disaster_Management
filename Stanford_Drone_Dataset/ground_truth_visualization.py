import cv2
import time
video_path = "./Videos/little/video0/video.mov"

cap = cv2.VideoCapture(video_path)

ret = True

frame_number = 0

annotation_file_path = "./annotations/" + video_path.split("/")[2] + "/" + video_path.split("/")[3] + "/" + "annotations.txt"

file_stream = open(annotation_file_path , "r")

fps_time = 0

cv2.namedWindow("output" , cv2.WINDOW_NORMAL)
while(ret):

    ret , frame = cap.read()
    boxes = {}
    # file_stream = open(annotation_file_path , "r")
    for line in file_stream:
        if(int(line.split(" ")[5]) == frame_number):
            # print(frame_number , "Inside at this frame")

            xmin = int(line.split(" ")[1])
            ymin = int(line.split(" ")[2])
            xmax = int(line.split(" ")[3])
            ymax = int(line.split(" ")[4])

            # print(str(line.split(' ')[9]))

            if(str(line.split(" ")[9].split("\"")[1]) == "Biker"):  
                cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(100 , 0 , 0) , 3)
            elif(str(line.split(" ")[9].split("\"")[1]) == "Pedestrian"):
                cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(0 , 0 , 100) , 3)
            elif(str(line.split(" ")[9].split("\"")[1]) == "Skater"): 
                cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(100 , 200 , 0) , 3)
            elif(str(line.split(" ")[9].split("\"")[1]) == "Cart"):  
                cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(100 , 0 , 0) , 3)
            elif(str(line.split(" ")[9].split("\"")[1]) == "Car"):
                print("Car found")  
                cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(100, 0 , 200) , 3)
            elif(str(line.split(" ")[9].split("\"")[1])== "Bus"):  
                cv2.rectangle(frame,(xmin,ymin),(xmax,ymax) ,(0 , 0 , 0) , 3)
            
            # print(xmin , ymin , xmax , ymax)
    file_stream.seek(0)
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
    k  = cv2.waitKey(25)
    if (k==27):
        break

cv2.destroyAllWindows()




