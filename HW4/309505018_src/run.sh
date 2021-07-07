#!/bin/bash

set -e

if [ "$1" = "" ];then
	echo "Command Error, no argv 1"
	exit 1
fi

python3 gan.py --mode=process_data --data_path=$1
python3 gan.py --mode=train
python3 gan.py --mode=inference --model_path=result/models/99600/
# python3 eval/fid_score.py result/images_inference/ dataset/images_ref/
