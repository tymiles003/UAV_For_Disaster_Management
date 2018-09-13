import argparse
import logging
import time
import skvideo.io
import cv2
import numpy as np
import os
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from keras.models import load_model

logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
save_counter = 0
fps_time = 0
xyz = 0
if __name__ == '__main__':
    ret_val = True
    #cv2.namedWindow('tf-pose-estimation result',cv2.WINDOW_NORMAL)
    #cv2.namedWindow("original",cv2.WINDOW_NORMAL)
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--camera', default=0,type = int)
    #parser.add_argument('--start_time',type = int,default = 0)
    #parser.add_argument('--end_time',type = int, required = True)

    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    args = parser.parse_args()

    logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))
    w, h = model_wh(args.resize)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368))
    logger.debug('cam read+')
    path = "/media/ayush/Extra/"
    cam = cv2.VideoCapture("/media/ayush/Extra/Video_Dataset/Two/sitting_1.mp4")
    cv2.namedWindow('tf-pose-estimation result',cv2.WINDOW_NORMAL)
    #ret_val , image = cam.read()
    count = 0
    i = 0
    out_vector = {}
    
    model_LSTM = load_model(path+"Numpy_dataset/first_model.h5")
    model_nn = load_model(path+"Numpy_dataset/first_model_nn.h5")

    #print("model loaded\n\n")
    our_counter = 0
    accuracy_counter = 0
    counter_1 = 0
    while(ret_val):
        #print(i)
        ret_val, image = cam.read()
        if(ret_val == False):
            break
        # print(image.shape)
        # frame = image.copy()
        # logger.debug('image process+')
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)

        #logger.debug('postprocess+')

        image,centers = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        angles_of_body = e.get_angles(humans,centers)

        angle_vector = e.get_final_angle_vector(angles_of_body)

        #print("\n\nThe no. of humans is {}\n\n".format(len(angle_vector)))
        for k in range(len(angle_vector)):   ## len(angle_vector) represents no. of humans detected in the frame
            #print("our_counter = {}".format(our_counter))
            if(our_counter ==41):
                break
            if(our_counter == 0 ):
                out_vector[k] = angle_vector[k+1]
            elif(k >= len(out_vector)):
                out_vector[k] = angle_vector[k+1]
            else:
                # print("Inside else")
                out_vector[k] = np.hstack((out_vector[k],angle_vector[k+1]))
                # print(out_vector[k].shape,angle_vector[k+1].shape)
        our_counter+=1
        # print(our_counter)
        if(our_counter == 40):
            # print("Inside if")
            for k in range(len(out_vector)):
                # print("Inside the for loop now")
                # print(out_vector[k].T[0])
                out_vector[k] = out_vector[k].reshape((1,out_vector[k].shape[1],out_vector[k].shape[0]))
                # print("Out_vector[k] shape is {}".format(out_vector[k].shape[1]))
                if(out_vector[k].shape[1] == 40):
                    # print("Inside the second if")
                    # out_vector[k] = np.load("/media/ayush/Extra/Numpy_dataset/One/class_1_0rotate_1.mp4.npy")
                    # out_vector[k] = np.expand_dims(out_vector[k],axis = 0)
                    y_LSTM = model_LSTM.predict(out_vector[k])
                    y_nn = model_nn.predict(out_vector[k].reshape(1,480))
                    #np.save("/media/ayush/Extra/Numpy_dataset/run_video/"+"class_2_"+str(count)+".npy",out_vector[k])
                    #print("numpy vector saved")
                    print("\n\n y_LSTM :{}\n".format(y_LSTM))
                    print("\n\n y_nn :{}\n".format(y_nn))
                    class_pred_LSTM = np.argmax(y_LSTM)
                    class_pred_nn = np.argmax(y_nn)
                    print("class_pred_LSTM : {} for k = {}".format(class_pred_LSTM,k))
                    print("class_pred_nn: {} for k = {}" .format(class_pred_nn,k))
            our_counter = 0
            out_vector = {}
        #         print(out_vector[k])
        #         print(out_vector[k].shape)
        #     our_counter = 0
        # if(our_counter == 40):
        #     for k in range(len(out_vector)):
        #         out_vector[k] = out_vector[k].reshape((out_vector[k].shape[1],out_vector[k].shape[0]))
        #     #for k in range(len(out_vector)):
        #         #print("\nour_vector[{}]'s shape is {} \n".format(k,out_vector[k].shape))
        #     for k in range(len(out_vector)):
        #         out_vector[k] = out_vector[k].reshape((1,out_vector[k].shape[0],out_vector[k].shape[1]))
        #         if(out_vector[k].shape[1] == 40):
        #             # out_vector[k] = (out_vector[k] - np.mean(out_vector[k]))/np.std(out_vector[k])
        #             # accuracy_counter +=1
        #             y = model_LSTM.predict(out_vector[k])
        #             #np.save(path+"Numpy_dataset/run_video/",out_vector[k])
        #             print("\n\n y :{}\n".format(y))
        #             #if(y[0][1] < 0.5):
        #             #    y[0][1] = 0
        #             class_pred = np.argmax(y)

        #             if(class_pred ==1):
        #                 counter_1+=1
        #                 #print(out_vector[k])	
        #             print("class_pred : {} for k = {}".format(class_pred,k))
        #     our_counter = 0
        #     out_vector = {}
        #     print("\n\n\nForty frames are read and hopefully predicted")
        #     print("\n\nRefreshing the our_counter and out_vector variables now \n\n")

        
        

        # print(out_vector)
    
        # if(count>=40):
        #    logger.debug("Video name :{} , slice_number :{} is now saved\n\n".format(video_name,count_1))
        #    print("\n The numpy array saved has the shape of {} \n".format(out_vector.T.shape))
        #     np.save("./dataset_numpy/One/class_1"+"video_"+video_name+"_"+str(count_1)+".npy",out_vector.T)
        #    count_1+=1
        #    count = 0
        #    i=0
        #    continue
        # logger.debug('show+')    
        
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('tf-pose-estimation result', image)
        #cv2.imshow("original" , frame)

        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        #logger.debug('finished+')
        #i+=1
        #xyz+=1
        #print("Frame number {}".format(xyz))
        count +=1
        print(count)
    cv2.destroyAllWindows()


