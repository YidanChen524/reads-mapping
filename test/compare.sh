#!/bin/bash

python3 $1 $3 $4 | sort > output-1.txt
python3 $2 $3 $4 | sort > output-2.txt
diff output-1.txt output-2.txt
rm output-1.txt output-2.txt
