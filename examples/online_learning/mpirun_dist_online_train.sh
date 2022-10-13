#!/bin/bash
# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

# bash mpirun_dist_online_train.sh RANK_SIZE LOCAL_HOST_IP
self_path=$(cd "$(dirname "$0")" || exit; pwd)
RANK_SIZE=$1
LOCAL_HOST_IP=$2

mpirun --allow-run-as-root -n $RANK_SIZE --output-filename log_output --merge-stderr-to-stdout \
    python -s ${self_path}/dist_online_train.py --address=$LOCAL_HOST_IP  \
    --device_target="GPU"  > log.txt 2>&1 &
