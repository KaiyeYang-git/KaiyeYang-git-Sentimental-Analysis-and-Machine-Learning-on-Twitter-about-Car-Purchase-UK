#!/bin/bash
#SBATCH -N 1
#SBATCH -c 4
#SBATCH --mem=4G
#SBATCH -p 'cpu'
#SBATCH --qos='long-cpu'
#SBATCH --job-name=TwiSearch1
#SBATCH -t 14-00
#SBATCH -e /home2/hzhx55/Dissertation/erroutput_1.txt
#SBATCH -o /home2/hzhx55/Dissertation/output_1.txt
source /etc/profile
source /home2/hzhx55/Dissertation/env/bin/activate
python3 /home2/hzhx55/Dissertation/TwRes_model1.py
