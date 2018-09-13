import argparse
import logging
import time
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from tf_pose import common
from tf_pose.common import CocoPart
logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0


if __name__ == '__main__':
    cv2.namedWindow('tf-pose-estimation result', cv2.WINDOW_NORMAL)
    cv2.namedWindow('original', cv2.WINDOW_NORMAL)
    cv2.namedWindow('zero_image', cv2.WINDOW_NORMAL)
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--camera', type=int, default=0)

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
    cam = cv2.VideoCapture(0)
    help = 0
    frame_counter = 0
    while True:
        ret_val, image = cam.read()
        frame_counter +=1
        frame = image.copy()
        image_zero = np.zeros(image.shape)

        #logger.debug('image process+')
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)

    ###########################################################################################################################
        # def draw_humans(npimg, humans, imgcopy=False):
        centers = {}
        for human in humans:
            # print(human.body_parts.keys())
            # draw point
            #print("\n\n Printing common.Coco ........ \n\n")
            #print(common.CocoPart.Background.value)
            for i in range(common.CocoPart.Background.value):
                if i not in human.body_parts.keys():
                    continue

                body_part = human.body_parts[i]
                center = (int(body_part.x * image.shape[1] + 0.5), int(body_part.y * image.shape[0] + 0.5))
                centers[i] = center
                # if(i==2 or i== 3 or i ==4):
                #     print(centers[i] , i)
                # cv2.circle(npimg, center, 3, common.CocoColors[i], thickness=3, lineType=8, shift=0)
            # # draw line
            # for pair_order, pair in enumerate(common.CocoPairsRender):
            #     if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
            #         continue

            #     # npimg = cv2.line(npimg, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)
            #     cv2.line(npimg, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)

            if((2 in human.body_parts.keys() and 3 in human.body_parts.keys() and 4 in human.body_parts.keys()) or (5 in human.body_parts.keys() and 6 in human.body_parts.keys() and 7 in human.body_parts.keys())):
                if(2 in human.body_parts.keys() and 3 in human.body_parts.keys() and 4 in human.body_parts.keys()):
                    if((centers[2][1]>centers[3][1] and centers[3][1]>centers[4][1])):
                        # print("Help required")
                        help +=1
                elif(5 in human.body_parts.keys() and 6 in human.body_parts.keys() and 7 in human.body_parts.keys()):
                    if((centers[5][1]>centers[6][1] and centers[6][1]>centers[7][1])):
                        # print("Help required")
                        help+=1
            # else:
            #     print("Help not required")

        ##############################################################################################################################

        #logger.debug('postprocess+')
        image,centers = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        image_zero,centers = TfPoseEstimator.draw_humans(image_zero, humans, imgcopy=False)
        #logger.debug('show+')
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('tf-pose-estimation result', image)
        cv2.imshow('original', frame)
        cv2.imshow('zero_image',image_zero)
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        #logger.debug('finished+')

        if(frame_counter == 40):
            if(help > 10):
                print("\n\n")
                print("="*140)
                print("Help required")
            frame_counter = 0
            help = 0
        # print("frame number is {}".format(frame_counter))
        # print("Help counter is {}".format(help)) 
         
    cv2.destroyAllWindows()
