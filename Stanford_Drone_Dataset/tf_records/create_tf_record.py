import tensorflow as tf
import yaml
import os
from object_detection.utils import dataset_util
import cv2

flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

LABEL_DICT =  {
    "Person" : 1,
    "Cart" : 2,
    "Car" : 3,
    "Bus" : 4,
    }

def _bytes_feature(value):
    """
    Kuch toh karta hai 
    """
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def create_tf_example(examples_per_frame , cap , path) :
    
    # Bosch
    height = int(cap.get(3))
    width = int(cap.get(4))

    # filename = example['path'] # Filename of the frame. Empty if frame is not from file
    # filename = filename.encode()

    with tf.gfile.GFile(path, 'rb') as fid:
        encoded_frame = fid.read()

    # frame_format = 'png'.encode() 
            
    
    xmins = [] # List of normalized left x coordinates in bounding box (1 per box)
    xmaxs = [] # List of normalized right x coordinates in bounding box
                # (1 per box)
    ymins = [] # List of normalized top y coordinates in bounding box (1 per box)
    ymaxs = [] # List of normalized bottom y coordinates in bounding box
                # (1 per box)
    classes_text = [] # List of string class name of bounding box (1 per box)
    classes = [] # List of integer class id of bounding box (1 per box)

    for line in examples_per_frame:
            xmins.append(int(line.split(",")[1]))
            ymins.append(int(line.split(",")[2]))
            xmaxs.append(int(line.split(",")[3]))
            ymaxs.append(int(line.split(",")[4]))
            
            if(str(line.split(",")[9]) == "Biker\n" or str(line.split(",")[9]) == "Pedestrian\n" or str(line.split(",")[9]) == "Skater\n"):
                classes_text.append("Person")
            elif(str(line.split(",")[9]) == "Cart\n"):
                classes_text.append("Cart")
            elif(str(line.split(",")[9]) == "Car\n"):
                classes_text.append("Car")           
            elif(str(line.split(",")[9]) == "Bus\n"):
                classes_text.append("Bus")
            classes.append(int(LABEL_DICT[classes_text[-1]]))
            classes_text[-1] = classes_text[-1].encode()
    

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'frame/height': dataset_util.int64_feature(height),
        'frame/width': dataset_util.int64_feature(width),
        'frame/encoded': dataset_util.bytes_feature(encoded_frame),
        'frame/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'frame/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'frame/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'frame/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'frame/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'frame/object/class/label': dataset_util.int64_list_feature(classes),
    }))

    return tf_example


def main(_):
    
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

    path ="/media/ayush/Extra/The_Eternal_Dataset/var_img.jpeg"

    ret = True
    step = 3
    frame_number = 0
    cap = cv2.VideoCapture("/media/ayush/Extra/The_Eternal_Dataset/Videos/quad/video1/video.mov")   

    while(ret):
        for i in range(step):
            ret , frame = cap.read()
            frame_number+=1

        if(frame_number == step):
            frame_number -=1

        examples_per_frame = []
        cv2.imwrite(path , frame)
        file_stream = open("/media/ayush/Extra/The_Eternal_Dataset/annotations/quad/video1/annotations.txt","r")
        for line in file_stream:
            if(int(line.split(",")[5]) <= frame_number):

                if(int(line.split(",")[5]) == frame_number):
                    examples_per_frame.append(line)
            else:
                tf_example = create_tf_example(examples_per_frame , cap , path)
                # os.system("rm /media/ayush/Extra/The_Eternal_Dataset/var_img.jpeg")
                writer.write(tf_example.SerializeToString())
                break


if __name__ == '__main__':
    tf.app.run()

