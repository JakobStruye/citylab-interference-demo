#!/bin/bash


ssh jstruye@euterpe.idlab.uantwerpen.be 'date > timestamp_tmp'
rsync -av --progress --files-from=<(ssh jstruye@euterpe.idlab.uantwerpen.be 'find ~/cot -cnewer timestamp -type f -exec echo {} \;') jstruye@euterpe.idlab.uantwerpen.be:/ . 

ssh jstruye@euterpe.idlab.uantwerpen.be 'rm timestamp && mv timestamp_tmp timestamp'
