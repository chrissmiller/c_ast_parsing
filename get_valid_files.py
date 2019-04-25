import re
from os import system
# Takes a file with all filenames, produces file listing all binaries
# with correct c files related to engs20
filepath = "../archives/2019_filenames.txt"

with open(filepath, "r") as allfiles:
    filenames = set(allfiles.readlines())

destfiles = []
dest = "../archives/2019_binaries.txt"
with open(dest, "w") as dest_file:
    for filename in filenames:
        if "." not in filename[-21:] and "engs20" in filename and "2019" not in filename and filename[:-1] + '.c\n' in filenames:
            dest_file.write(filename[:-1] + '.c\n')
            destfiles.append(filename[:-1] + '.c\n')

generic_path = "../archives/2019_archive/"
for cfilename in destfiles:
    specific_path = generic_path + cfilename[:-1]
    cmd = "cp " + specific_path + " ../archives/to_process_2019/."
    system(cmd)

starting_points = set()
log = ""
for file in destfiles:
    matcher = re.match('[a-zA-Z0-9]{7}_(.*)_\d{4}-\d{2}-\d{2}', file)
    if matcher:
        starting_points.add(matcher.group(1))
    else:
        log += "No match, file " + file + "\n"

with open("../archives/filenames/startpts_2019.txt", "w") as startpts:
    for pt in starting_points:
        startpts.write(pt + "\n")

print("Log: " + log)
