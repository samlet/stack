#!/bin/bash
#$ docker login --username=xiaofei.wu@gmail.com registry.cn-hangzhou.aliyuncs.com
# image=samlet/cabocha:0.1.4
# image=samlet/timeprocs:0.1
image=samlet/langprocs:0.1
docker tag $image registry.cn-hangzhou.aliyuncs.com/$image
docker push registry.cn-hangzhou.aliyuncs.com/$image
docker rmi registry.cn-hangzhou.aliyuncs.com/$image
