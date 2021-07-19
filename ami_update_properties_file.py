import re
import sys
import os
import shutil
region_file = open("/home/cloud-user/ami-files/regions.txt", "r")
input_region_value_map = {}
for i in region_file.readlines():
    try:
        if (os.environ[i.rstrip("\n")] != None):
              input_region_value_map[(i.rstrip("\n")).replace("_","-")] = os.environ[i.rstrip("\n")]
        else:
              continue
    except:
        continue
ami_genearted = input_region_value_map
file_path = sys.argv[1] + "/EnvironmentJsonsV2/R37/properties/"
if (os.environ["Environment"] == "MREL-AWS"):
    file_path = file_path + "cdi-aws-mrel-pod1/cdi-pod-services.properties"
file_input = open(file_path, "r")
content = file_input.read()
for i in ami_genearted.keys():
    pattern = i + "=(ami-.*?)[;|\"]"
    reg_pattern = re.compile(pattern)
    old_ami = re.search(reg_pattern,content)
    if ((old_ami == None) and (i + "=" in content)):
        new_region_pattern = i + "=" + "[\s]*"
        new_reg_pattern = re.compile(new_region_pattern)
        new_ami_region = i + "=" + ami_genearted[i]
        content = re.sub(new_reg_pattern,new_ami_region,content)
    elif ((old_ami == None) and ((i + "=") not in content)):
        new_region_pattern = "\$serverless_agent_image=\"(.*)\""
        new_reg_pattern = re.compile(new_region_pattern)
        old_ami_entry = (re.search(new_reg_pattern,content).group(0)).rstrip("\"")
        new_ami_region = i + "=" + ami_genearted[i]
        new_ami_entry = old_ami_entry + ";" + new_ami_region + "\""
        content = re.sub(new_reg_pattern,new_ami_entry,content)
    else:
        content  = re.sub(old_ami.group(1),ami_genearted[i],content)
file_output = open(file_path, "r+")
file_output.write(content)
file_output.truncate()

