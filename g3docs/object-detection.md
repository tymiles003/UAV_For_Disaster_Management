# Object Detection

Base folder: Stanford_Drone_Dataset

## Exports

```
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```

## Create TF Records

```
python tf_records/create_sdd_tf-records.py --output_path /home/uav/data/train.record
```

TODO: change args
```
python tf_records/create_sdd_tf-records.py --output_path /home/uav/data/train.record
```

## Configs

At configs.

## Training

```
PIPELINE_CONFIG_PATH={$(pwd)/configs/ssd_inception_v2_coco.config}
MODEL_DIR={/home/uav/model}
NUM_TRAIN_STEPS=100000
SAMPLE_1_OF_N_EVAL_EXAMPLES=1
python object_detection/model_main.py \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --model_dir=${MODEL_DIR} \
    --num_train_steps=${NUM_TRAIN_STEPS} \
    --sample_1_of_n_eval_examples=$SAMPLE_1_OF_N_EVAL_EXAMPLES \
    --alsologtostderr
```

## Runnning Tensorboard

```
tensorboard --logdir /home/uav/model
```