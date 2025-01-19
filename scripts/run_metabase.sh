#!/bin/bash

curr_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${curr_dir}

cd ../analytics
java -jar -Dlog4j2.formatMsgNoLookups=true metabase.jar