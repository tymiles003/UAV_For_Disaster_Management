import tensorflow as tf
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
    video_paths = open("/media/ayush/Extra/The_Eternal_Dataset/Tf-Records/research/path_to_videos_test.txt","r")
    num_videos = 0
    for video_path in video_paths:
        num_videos +=1
    video_number = 0
    video_paths.seek(0)
    for video_path in video_paths:
        ret = True
        step = 3
        frame_number = 0
        video_number +=1
        video_path = video_path.replace("\n","")
        cap = cv2.VideoCapture(video_path)
        print(video_path)
        annotation_file_path = "/media/ayush/Extra/The_Eternal_Dataset/annotations/"+ video_path.split("/")[6] + "/" + video_path.split("/")[7] + "/" + "annotations.txt"
        file_stream = open(annotation_file_path,"r")
        print("="*30)
        print("Reading from {}".format(video_path))
        print("Video number {} of {}".format(video_number , num_videos))
        while(ret):
            for i in range(step):
                ret , frame = cap.read()
                frame_number+=1

            if(frame_number == step):
                frame_number -=1

            examples_per_frame = []
            cv2.imwrite(path , frame)

            for line in file_stream:
                if(int(line.split(",")[5]) <= frame_number):

                    if(int(line.split(",")[5]) == frame_number):
                        examples_per_frame.append(line)
                else:
                    tf_example = create_tf_example(examples_per_frame , cap , path)
                    # os.system("rm /media/ayush/Extra/The_Eternal_Dataset/var_img.jpeg")
                    writer.write(tf_example.SerializeToString())
                    break

            print("percentage of video done is {}".format((frame_number/cap.get(7))*100) , end ='\r')


        print("{} is done moving on to the next video".format(video_path))
        os.system("rm /media/ayush/Extra/The_Eternal_Dataset/var_img.jpeg")


if __name__ == '__main__':
    tf.app.run()

