# import the necessary packages
import cv2
import numpy as np
# now let's initialize the list of reference point
ref_point = []
count = 0
disp_counter = 0
w_glob , h_glob = 0, 0
def draw_rectangle(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, crop , count , w_glob , h_glob

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        count +=1
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))
        if(count>=1 and count <=2):
            count+=1
            w = ref_point[1][0] - ref_point[0][0]
            h = ref_point[1][1] - ref_point[0][1]
            w_glob = w
            h_glob = h
        # draw a rectangle around the region of interest
        cv2.rectangle(image, ref_point[0], ref_point[1], (0,255,0), 2)
        cv2.imshow("image", image)


# construct the argument parser and parse the arguments

# load the image, clone it, and setup the mouse callback function
image = cv2.imread("kerala_idukki.png")
clone = image.copy()
image_2 = image.copy()
cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.namedWindow("image_2",cv2.WINDOW_NORMAL)
cv2.setMouseCallback("image", draw_rectangle)

alpha = 0.3
alpha_2 = 0.2
num_frames = 100
point_next = {}
decay = 100
# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    key = cv2.waitKey(500)
    decay *= 0.8
    # press 'r' to reset the window
    # if key == ord("r"):
    #     image = clone.copy()

    # if the 'c' key is pressed, break from the loop
    if key == 27:
        break
    # print(ref_point[0])
    # print(ref_point[-1])
    # if(len(ref_point)>0):
    #     if(count<=0 and count >= -2):
    #         count-=1
    #         print(ref_point[0])
    #         print(ref_point[-1])
    if(w_glob > 0 and h_glob>0):

        if(disp_counter<=0):
            disp_counter+=1
            # print(w_glob,h_glob)

            start = ref_point[0] 
            end = ref_point[1]

            #cv2.circle(image,(int(start[0]+w_glob/2),int(start[1]+h_glob/2)),h_glob//5,(0,255,0),3)

            points = {}
            points[0] = (int(start[0]+ 7 + h_glob/8),int(start[1] +h_glob/8 ))
            points[1] = (int(start[0] -6 +w_glob - h_glob/8),int(start[1] +h_glob/8 ))
            points[2] = (int(start[0]+ 8 + h_glob/8),int(start[1] + h_glob - h_glob/8 - 10))
            points[3] = (int(start[0] -5 +w_glob - h_glob/8),int(start[1] -h_glob/8 + h_glob - 7))
            points[4] = (int(start[0]+ w_glob/2 + 25),int(start[1] +h_glob/2 ))

            start = (start[0],start[1]+ h_glob//2)
            # print(points)

            for i  in range(5):
                point_next[i] = np.asarray(start)

        for i ,_ in enumerate(points):
            cv2.circle(image,(point_next[i][0],point_next[i][1]),7,(0,255,0),-1)
            image_2 = cv2.addWeighted(image,alpha,image_2,1-alpha,0 , image_2)
            #cv2.circle(image,start,5,(0,0,0),-1)
            point_next[i][0] += int(((points[i][0]- point_next[i][0])/decay))
            point_next[i][1] += int(((points[i][1]- point_next[i][1])/decay))
            # print("point_next for {} is {}".format(i,point_next[i]))
            # print(point_next[0][0])
            # print(point_next[0][1])
            # print(start)
            cv2.line(image_2,(start),(point_next[i][0],point_next[i][1]),(0,0,0),2)
        our_counter = 0
        for i ,_ in enumerate(points):
            if(int(((points[i][0]- point_next[i][0])/decay)) == 0 and int(((points[i][1]- point_next[i][1])/decay)) == 0 and our_counter <5):
                our_counter +=1
                cv2.circle(image,(points[i][0],points[i][1]),int(h_glob/13),(0,255,0),-1)
            # if(count>=6):
            #     image_2 = cv2.addWeighted(image,alpha_2,image_2,1-alpha_2,0 , image_2)

            
            
    cv2.imshow("image_2", image_2)
    cv2.imshow("image",image)

        
        
    


    


# close all open windows
cv2.destroyAllWindows() 