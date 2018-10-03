# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

r"""Convert raw PASCAL dataset to TFRecord for object_detection.
Example usage:
    python object_detection/dataset_tools/create_pascal_tf_record.py \
        --data_dir=/home/user/VOCdevkit \
        --output_path=/home/user/pascal.record
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import io
import logging
import os
import cv2
import time

import PIL.Image
import tensorflow as tf

from object_detection.utils import dataset_util
from object_detection.utils import label_map_util

flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('type','train','Whether to use train or test.')
FLAGS = flags.FLAGS

if FLAGS.type =='train':
    video_paths="/home/uav/UAV_For_Disaster_Management/Stanford_Drone_Dataset/paths/path_to_videos.txt"
else:
    video_paths="/home/uav/UAV_For_Disaster_Management/Stanford_Drone_Dataset/paths/path_to_videos_test.txt"

LABEL_DICT =  {
    "Pedestrian" : 1,
    "Skater" : 2,
    "Biker" : 3 ,
    "Cart" : 4,
    "Car" : 5,
    "Bus" : 6,
    }

def create_tf_example(examples_per_frame , cap , path):
    """Convert XML derived dict to tf.Example proto.
    Notice that this function normalizes the bounding box coordinates provided
    by the raw data.
    Args:
    data: dict holding PASCAL XML fields for a single image (obtained by
        running dataset_util.recursive_parse_xml_to_dict)
    dataset_directory: Path to root directory holding PASCAL dataset
    label_map_dict: A map from string label names to integers ids.
    ignore_difficult_instances: Whether to skip difficult instances in the
        dataset  (default: False).
    image_subdirectory: String specifying subdirectory within the
        PASCAL dataset directory holding the actual image data.
    Returns:
    example: The converted tf.Example.
    Raises:
    ValueError: if the image pointed to by data['filename'] is not a valid JPEG
    """
    full_path = path
    with tf.gfile.GFile(full_path, 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = PIL.Image.open(encoded_jpg_io)
    if image.format != 'JPEG':
        raise ValueError('Image format not JPEG')
    key = hashlib.sha256(encoded_jpg).hexdigest()
    filename = full_path
    width = int(cap.get(4))
    height = int(cap.get(3))

    xmin = []
    ymin = []
    xmax = []
    ymax = []
    classes = []
    classes_text = []
    truncated = []
    difficult_obj = []
    '''
    if 'object' in data:
        for obj in data['object']:
            difficult = bool(int(obj['difficult']))
            if ignore_difficult_instances and difficult:
                continue

        difficult_obj.append(int(difficult))

        xmin.append(float(obj['bndbox']['xmin']) / width)
        ymin.append(float(obj['bndbox']['ymin']) / height)
        xmax.append(float(obj['bndbox']['xmax']) / width)
        ymax.append(float(obj['bndbox']['ymax']) / height)
        classes_text.append(obj['name'].encode('utf8'))
        classe.append(label_map_dict[obj['name']])
        truncated.append(int(obj['truncated']))
        poses.append(obj['pose'].encode('utf8'))
    '''

    for line in examples_per_frame:
        x = line.replace("\n","")
        x = x.replace("\"","")
        line = x
        if(int(line.split(" ")[6]) == 0): 
            xmin.append(int(line.split(" ")[1])/width)
            ymin.append(int(line.split(" ")[2])/height)
            xmax.append(int(line.split(" ")[3])/width)
            ymax.append(int(line.split(" ")[4])/height)
            
            if(str(line.split(" ")[9]) == "Biker"):
                class_name = "Biker"
                classes_text.append("Biker".encode('utf8'))
            elif(str(line.split(" ")[9]) == "Cart"):
                class_name = "Cart"
                classes_text.append("Cart".encode('utf8'))
            elif(str(line.split(" ")[9]) == "Car"):
                class_name = "Car"
                classes_text.append("Car".encode('utf8'))           
            elif(str(line.split(" ")[9]) == "Bus"):
                class_name = "Bus"
                classes_text.append("Bus".encode('utf8'))
            elif(str(line.split(" ")[9]) == "Pedestrian"):
                class_name = "Pedestrian"
                classes_text.append("Pedestrian".encode('utf8'))
            elif(str(line.split(" ")[9]) == "Skater"):
                class_name = "Skater"
                classes_text.append("Skater".encode('utf8'))            
            classes.append(int(LABEL_DICT[class_name]))
            truncated.append(0)
            difficult_obj.append(0)
        

    example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(
            filename.encode('utf8')),
        'image/source_id': dataset_util.bytes_feature(
            filename.encode('utf8')),
        'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmin),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmax),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymin),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymax),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
        'image/object/difficult': dataset_util.int64_list_feature(difficult_obj),
        'image/object/truncated': dataset_util.int64_list_feature(truncated)
    }))
    return example


def main(_):


    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

    path ="/home/uav/var_img.jpeg"
    video_paths = open(video_paths,"r")
    num_videos = 0

    for video_path in video_paths:
        num_videos +=1
    video_number = 0
    video_paths.seek(0)
    start = time.time()
    for video_path in video_paths:
        ret = True
        step = 5
        frame_number = 0
        video_number +=1
        video_path = video_path.replace("\n","")
        cap = cv2.VideoCapture(video_path)
        annotation_file_path = "/home/uav/annotations/"+ video_path.split("/")[4] + "/" + video_path.split("/")[5] + "/" + "annotations.txt"
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
                if(int(line.split(" ")[5]) <= frame_number):

                    if(int(line.split(" ")[5]) == frame_number):
                        examples_per_frame.append(line)
                else:
                    tf_example = create_tf_example(examples_per_frame , cap , path)
                    # os.system("rm /media/ayush/Extra/The_Eternal_Dataset/var_img.jpeg")
                    writer.write(tf_example.SerializeToString())
                    break
            print("Video no. {} percentage {} , ".format(video_number,((frame_number/cap.get(7))*100)) , end ='\r')


        print("{} is done moving on to the next video".format(video_path))
        os.system("rm /home/uav/var_img.jpeg")

    end = time.time()
    print("Total time taken = {} minutes".format((end-start)/60))

if __name__ == '__main__':
    tf.app.run()
