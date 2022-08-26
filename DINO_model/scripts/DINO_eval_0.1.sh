coco_path=$1
checkpoint=$2
python main.py \
  --output_dir logs/DINO/R50-MS4-01-%j \
	-c config/DINO/DINO_4scale_0.1.py --coco_path $coco_path  \
	--eval --resume $checkpoint \
	--options dn_scalar=100 embed_init_tgt=TRUE \
	dn_label_coef=1.0 dn_bbox_coef=1.0 use_ema=False \
	dn_box_noise_scale=1.0
