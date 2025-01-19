#!/bin/bash

curr_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${curr_dir}

cd ../
mkdir analytics
cd analytics/

wget https://downloads.metabase.com/v0.48.3/metabase.jar