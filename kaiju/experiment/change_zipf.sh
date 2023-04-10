#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <new_value>"
  exit 1
fi

new_value="$1"
files=("/home/ubuntu/kaiju/contrib/YCSB/core/src/main/java/com/yahoo/ycsb/generator/ScrambledZipfianGenerator.java" "/home/ubuntu/kaiju/contrib/YCSB/core/src/main/java/com/yahoo/ycsb/generator/ZipfianGenerator.java")

for file in "${files[@]}"
do
  if grep -q "public static final double ZIPFIAN_CONSTANT=0.8;" "$file"; then
    sed -i "s/public static final double ZIPFIAN_CONSTANT=0.8;/public static final double ZIPFIAN_CONSTANT=$new_value;/" "$file"
    echo "Changed ZIPFIAN_CONSTANT value in $file to $new_value"
  else
    echo "Could not find ZIPFIAN_CONSTANT in $file"
  fi
done
