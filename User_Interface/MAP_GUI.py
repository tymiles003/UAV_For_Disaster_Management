import cv2
import numpy as np 
import math
r = 30        ## Radius of coverage of the drone ##
R = 450       ## Total radius of the disaster affected area ##
radius = R    ## Total radius of the disaster affected area ##
n = 60        ## no of drones ##
no_of_drones = n ## no of drones ##
l = []        ## A list which will have the no of drones for each ring (starting from the outermost ring)

points = {}   ## The dictionary of lists where each key represents the ring number and has the final co-ordinates of each drone in the ring
point_next = {} ## For storing the current value of the coordinate (when it travels from the starting point to the final point)
decay = {}    ## A dictionary which stores the inverse step size of each and every drone ##

image = cv2.imread("./guindy.jpeg")

image = cv2.resize(image,(640*2,640*2))

angle = []    ## Will store the angle the drone has to rotate per ring in consideration ##


########################### DISTRIBUTOR ################################
################### THIS HAS TO BE FURTHER DEVELOPED ###################
def distribute(n):
    """
    Takes in input n (NO OF DRONES) and returns a list
    which contains the number of drones per ring starting
    from the outermost ring

    """
    global l
    N = n
    while(n):
        l.append(math.ceil(n/2))
        # if(sum(l) == N ):
            # break
        n = n//2 
        # print(n)
        # print(",")
        # print(l)
    return l
################## NEED TO MAKE THIS BETTER #############################

cv2.namedWindow("map",cv2.WINDOW_NORMAL)

start = (0,0)  ## The point from where the drones will originate (GPS coordinates of the company) ##
center = (image.shape[1]//2,image.shape[0]//2) ## center of the concentric circles which is currently hardcoded to the center of the image ##


################# CIRCLE DRAWER ################################
for i in range(int(R/(2*r))):
    cv2.circle(image,center,radius,(0,0,255),8)
    radius -= 2*r
###############################################################



l = distribute(n)
for i in range(len(l)):
    angle.append(0)
# l = [1,1,1,1,1]
# print(l)

############ FUNCCTION TO ROTATE A POINT ######################
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return (qx, qy)

###############################################################


################## FINAL POINT GENERATOR ######################
for i,n in enumerate(l) :
    points[i] = []
    coord = (center[0]+0,center[1]+R-((2*i+1)*r))
    for x in range(n):
        theta = (2*np.pi/n)*x 
        x_coord , y_coord = rotate(center,coord,theta)
        points[i].append((x_coord,y_coord))
        cv2.circle(image,(int(x_coord),int(y_coord)),3,(255,0,0),-1)
###############################################################

################### POINT INITIALIZATION ######################
for i,n in enumerate(l):
    point_next[i] = []
    for x in range(n):
        point_next[i].append(np.asarray(start))
###############################################################


################### DECAY INITIALIZATION ######################
for i,n in enumerate(l):
    decay[i] = []
    for x in range(n):
        decay[i].append(300)
###############################################################



drone_reach_array = np.zeros((len(l),max(l))) ## An array initialized with zeros which will be later used to check whether all the drones have reached the final position or not ##

############# LOOP FOR MAKING THE DRONES REACH FROM THERE STARTING POSN'S TO THE FINAL POSITIONS ######
while(True and np.sum(drone_reach_array) != n):
    for i,_ in enumerate(points):
        for n_ring in range(len(points[i])):
            if(int(points[i][n_ring][0]- point_next[i][n_ring][0]) == 0 and int(points[i][n_ring][1]- point_next[i][n_ring][1]) == 0):
                continue
            if(abs(int(points[i][n_ring][0]- point_next[i][n_ring][0])) < 8 and abs(int(points[i][n_ring][1]- point_next[i][n_ring][1]) < 8)):
                cv2.circle(image,(point_next[i][n_ring][0],point_next[i][n_ring][1]),r-7,(0,255,0),-1)
                drone_reach_array[i][n_ring] = 1
            # print(np.sum(drone_reach_array))
            decay[i][n_ring] *= 0.8
            # if(i == 0):
            #     print(point_next[i][0])
            point_next[i][n_ring][0] += int(((points[i][n_ring][0]- point_next[i][n_ring][0])/decay[i][n_ring]))
            point_next[i][n_ring][1] += int(((points[i][n_ring][1]- point_next[i][n_ring][1])/decay[i][n_ring]))
            cv2.line(image,(start),(point_next[i][n_ring][0],point_next[i][n_ring][1]),(0,100,100),2)
            cv2.imshow("map",image)
    k = cv2.waitKey(200)
    if k == 27:
        # print("ESC key is pressed !!!!!!!!")
        break
    if((int(np.sum(drone_reach_array)) == no_of_drones)):
        # print("\n\nDrones have been placed now !!!!!!!!!!!!!\n\n")
        break

#######################################################################################################


################### PAUSE FOR TWO SECONDS #####################
cv2.waitKey(2000)
###############################################################

################ LOOP FOR ROTATING THE DRONES ###############
while(True):
    # angle+=10
    for i,_ in enumerate(l):
        angle[i] +=0.025*(1/(R-(2*i+1)*r))
        for n_ring in range(len(points[i])):
            rotated_x , rotated_y = rotate(center,points[i][n_ring],np.degrees(angle[i]))
            cv2.circle(image,(int(rotated_x),int(rotated_y)),r-7,(0,0,0),-1)            
    k = cv2.waitKey(150)
    if k ==27:
        break
    cv2.imshow("map",image)
##############################################################

# cv2.waitKey(0)
cv2.destroyAllWindows()

