# CVI project review

## UAV's For Disaster Management

## Questions

### What 

Team of drones for Disaster Management using Computer Vision and DL.

##### Each drone will serve these purposes :

  1)  Using deep learning, detecting the people from a height of 30 metres (almost looks like dots to human eyes)

  2) Send the GPS coordinates along with image of the detected people to be rescued, to the army or relief task forces.
  
  3) At lower heights the drones can also do activity recognition and detect out the people who are in need of help using Video Analysis and Deep Pose Estimation.
  
### Why

Because most of the times in any disaster the the majority of the army and relief services are directed towards the location which is affected in the worst way.(e.g. The areas very close to the epicenter of the earthquake). Thus in order to keep a check also on the other affected areas,we are planning to deploy a team of drones.

Also the fact that todays rescue ops depend a lot on Satellite Imagery , however satellite imagery presents a number of limitations including cost, data sharing restrictions, cloud cover, and the time needed to acquire images.

In contrast, UAV's can capture aerial imagery at a far higher resolution, more quickly and at much lower cost. And unlike satellites, members of the public can actually own UAV's. This means that disaster-affected communities can launch their own UAVs in response to a crisis.

Also most of the times the task forces and army takes a lot of time to respond since they dont know where to exactly look for the people who need to be rescued untill and unless they recieve a distress call from someone , our drones will solve the exact issue

### How

  1) For people detection at a huge height we have trained a faster-rcnn detector on a dataset taken from a drone and this model can solve the issue with a good accuracy as of now
  
  2) For detecting whether the person is in need of help or not we can use pose estimation and perform activity recognition on top of this to solve this , as of now we can detect the activity from 0-8 metres height of the drone
  
  3) For sending out the GPS coordinates the drone has a GPS module on it and a pixhawk which can be connected to an Rpi and these outputs can be transferred to the laptop via wifi (we will switch to better comms soon)
  
  4) At a small height the drones can do object-detection trained on COCO dataset with a very lite and real time model using ssd_mobilent_thin.
  
  5) But this all is for one drone only , but for covering the entire city we need many drones and we have made a path-planning algo which can automatically spread out the drones for covering maximum area in minimum time, keeping in mind constraints of number of drones, battery life, and field of view of each drone.
  
### Immediate goals

  1) Improving our model used for object-detection and optimising it 
  
  2) Improving pose estimation model 
  
  3) Trying a lot to run ROS with Python3
  
  3) Looking out for better ways of communication since we cant carry on with wifi any more
  
  4) Trying to optimize our models using tensorrt and testing the lag and fps we can get with Nvidia-Jetson TX2 as the onboard processing computer
  
  5) Looking out for better cameras to be placed on a drone rather than Go-Pro and USB webcam.
  
### Long-term goals

  1) Testing out our codes on cloud as well as on the onboard computer to check which one is better
  
  2) Working on obstacle avoidance so as to make the drones autonomous at lower heights
  
  2) Finding out ways on how to perform wireless comms so that the drone can talk to the army headquarters through huge distances
  
  








