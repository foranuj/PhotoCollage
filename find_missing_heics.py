import os
import shutil

rooms = ['Adventureland', 'Sunshine', 'Jungle', 'Ladybugs', 'Seaturtle']
basedir = '/Users/anshah/GoogleDrive/Monticello_Preschool_2021_2022_Original'
png_dir = '/Users/anshah/GoogleDrive/Monticello_Preschool_2021_2022'

with open('/Users/anshah/Desktop/HighResMissingHeics', 'r') as f:
    lines = f.readlines()
    missingCounter = 0
    for line in lines:
        event_name = os.path.dirname(line.strip()).split('/')[-1]
        file_name, ext = os.path.splitext(line.strip())
        base_file_name = os.path.basename(file_name)
        for room in rooms:
            room_event_path = os.path.join(basedir, room, event_name, base_file_name + ".heic")
            if os.path.exists(room_event_path):
                png_file_path = os.path.join(png_dir, room, event_name, base_file_name + ".png")
                print("Copy from %s to %s" % (png_file_path, line.strip()))
                #shutil.copyfile(room_event_path, line.strip())
                break
        else:
            missingCounter = missingCounter + 1
            print("Missing this file %s " % line.strip())

print("Missing %s files" % missingCounter)
