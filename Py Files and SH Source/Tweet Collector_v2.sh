#!/bin/bash
#SBATCH -N 1
#SBATCH -c 4
#SBATCH --mem=4G
#SBATCH -p 'cpu'
#SBATCH --qos='long-cpu'
#SBATCH --job-name=TwiSearch
#SBATCH -t 14-00
#SBATCH -e /home2/hzhx55/Dissertation/erroutput_2.txt
#SBATCH -o /home2/hzhx55/Dissertation/output_2.txt
source /etc/profile
source /home2/hzhx55/Dissertation/env/bin/activate
python3 /home2/hzhx55/Dissertation/TwRes_model2.py