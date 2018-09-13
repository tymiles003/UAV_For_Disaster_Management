
# coding: utf-8

# In[1]:


from darkflow.net.build import TFNet
import cv2
#import matplotlib.pyplot as plt
import numpy as np
import time
#get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg'")


# In[52]:


options ={
    'model':'cfg/yolo.cfg',
    'load':'bin/yolov2.weights',
    'threshold':0.33,
    'gpu' : 1.0
}


# In[53]:


tfnet= TFNet(options)


# In[45]:


"""img=cv2.imread('image.png',cv2.IMREAD_COLOR)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
result = tfnet.return_predict(img)
result
length=len(result)


# In[46]:


e1 = cv2.getTickCount()
for i in range(0,length):

    tl= (result[i]['topleft']['x'],result[i]['topleft']['y'])
    br=(result[i]['bottomright']['x'],result[i]['bottomright']['y'])
    label= result[i]['label']
    img= cv2.rectangle(img, tl,br,(0,255.0),7)
    img=cv2.putText( img,label,tl,cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
e2 = cv2.getTickCount()
time = (e2-e1)/(cv2.getTickFrequency())
print("One image processed in %f seconds",time)
e3 = cv2.getTickCount()
plt.imshow(img)
plt.show()
e4 = cv2.getTickCount()
time2 = (e4-e3)/(cv2.getTickFrequency())
print("One image plotted in %f seconds",time2)"""




# In[47]:
capture =cv2.VideoCapture(0)

colors = [tuple(255*np.random.rand(3)) for i in range(100)]

check = True
fps_time = 0
cv2.namedWindow('frame',cv2.WINDOW_NORMAL)

while(check):
    #e1 = cv2.getTickCount()
    #stime = time.time()
    check,frame = capture.read()
    print(check)
    if check == False:
        capture.release()
        cv2.destroyAllWindows()
        break
    frame = np.asarray(frame)
    result = tfnet.return_predict(frame)

    #print(result)
    person_counter = 0
    if check:
        for color,result_2 in zip(colors,result):
            tl= (result_2['topleft']['x'],result_2['topleft']['y'])
            br=(result_2['bottomright']['x'],result_2['bottomright']['y'])
            label= result_2['label']
            if(label == "person"  or label == "bench" or label == "bottle" or label == "cup" or label == "chair" or label == "laptop" or label == "clock" or label == "suitcase" or label == "cell phone"):
                frame = cv2.rectangle(frame,tl,br,color,7)
                frame=cv2.putText( frame,label,tl,cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
            # print(label)
        for color,result in zip(colors,result):
        #     #print("result is " , result)
            label= result['label']
            if(label == "person"):
                person_counter+=1

        print("\n\n {} persons found \n".format(person_counter))
        # cv2.imshow('frame',frame)
        #print('FPS {:.1f}'.format(1/(time.time()-stime)))
        # if cv2.waitKey(0) == 27:
        #     capture.release()
        #     cv2.destroyAllWindows()
        #     break
        cv2.putText(frame,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        # cv2.imshow('tf-pose-estimation result', image)
        # cv2.imshow("original" , frame)

        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        cv2.imshow('frame',frame)
        #logger.debug('finished+')
        #i+=1
        #xyz+=1
        #print("Frame number {}".format(xyz))
        # count +=1
        # print(count)
cv2.destroyAllWindows()
