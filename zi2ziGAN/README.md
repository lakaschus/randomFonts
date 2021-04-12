# zi2zi for Python 3 

Forked from https://github.com/kaonashi-tyc/zi2zi

Here I did some small adjustments in order to run the generator using the pretrained model using Python 3 on Windows.

# Tutorial on how to use the pretrained model:

1) Download the pretrained model at https://github.com/kaonashi-tyc/zi2zi
2) This model is trained with training data in SIMSUN font. Therefore you should download the simsun font on the internet, just to comply with the source code.
3) Run

python font2img.py --src_font=SIMSUN.ttf --dst_font=MaShanZheng.ttf --charset=CN --sample_count=1 --sample_dir=hanzi_dir --label=0 --filter=0 --shuffle=0


This script converts text to images. The characters are defined in charset/cjk.json. If you want to use your own set of characters create a json analogous to cjk.json but with your characters and point to the new json by changing DEFAULT_CHARSET in **font2img.py**.
The dst_font is the same as src_font because we actually don't want to train the model but just using the pretrained model.

4) Run

python package.py --dir=hanzi_dir/ --save_dir=save_dir/ --split_ratio=0

5) Run

python infer.py --model_dir=datasets/font27 --batch_size=1 --source_obj=save_dir/train.obj --embedding_ids=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 --save_dir=output_dir --interpolate=0 --steps=1


Or alternatively run

python run.py

the number of embedding_ids runs from 1 to 27 

Options --interpolate=0 --steps=1 saves only the resulting figure