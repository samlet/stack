#!/bin/bash
# $ bash /pi/stack/scripts/download_snips_models.sh 
array=( de en es fr it ja ko pt_br pt_pt )
for i in "${array[@]}"
do
    echo "$i ..."
    python -m snips_nlu download ${i}
done

echo 'done.'
