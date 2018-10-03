sudo apt-get install -y protobuf-compiler python-pil python-lxml python-tk
pip install Cython
pip install matplotlib

# COCO API Metrics
git clone https://github.com/cocodataset/cocoapi.git
cd cocoapi/PythonAPI
make
cp -r pycocotools <path_to_tensorflow>/models/research/

# From root folder
protoc object_detection/protos/*.proto --python_out=.