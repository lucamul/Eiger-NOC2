#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <new_value>"
  exit 1
fi

new_value="$1"
# replace ZIPFIAN_CONSTANT value in ScrambledZipfianGenerator.java file
sed -i "s/ZIPFIAN_CONSTANT=[0-9]*\.?[0-9]*/ZIPFIAN_CONSTANT=$new_value/" /home/ubuntu/kaiju/contrib/YCSB/core/src/main/java/com/yahoo/ycsb/generator/ZipfianGenerator.java

# replace USED_ZIPFIAN_CONSTANT value in ZipfianGenerator.java file
sed -i "s/USED_ZIPFIAN_CONSTANT=[0-9]*\.?[0-9]*/USED_ZIPFIAN_CONSTANT=$new_value/" /home/ubuntu/kaiju/contrib/YCSB/core/src/main/java/com/yahoo/ycsb/generator/ScrambledZipfianGenerator.java

echo "Constant values updated successfully!"
