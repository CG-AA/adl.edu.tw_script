import subprocess
from tqdm import tqdm
import sys

# Prompt the user for input
count = int(input("Enter the number of times to loop: "))
delay = int(input("Enter the delay between each request(ms): "))

suc = 0
command = ""
with open('cURL.txt', 'r') as file:
    command = file.read()
    # sleep
    command += f" && sleep {delay/1000};"

# Loop the specified number of times
for i in tqdm(range(1, count + 1)):
    res = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip()
    # if message is {"msg":"\u7b54\u5c0d\u4e86\uff01"} add 1 to suc
    if res == '{"msg":"\\u7b54\\u5c0d\\u4e86\\uff01"}':
        suc += 1
        print(str(suc)+'success')
    else:
        print("\033[91mfailed, retrying\033[0m")
        print(res)
        i-=1