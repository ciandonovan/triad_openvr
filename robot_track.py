import triad_openvr
import time
import sys
import math
from pathlib import Path

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

controller = "controller_1"

if len(sys.argv) == 1:
    interval = 1/10
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False

def main():
    start = time.time()

    while ((curr_euler := v.devices[controller].get_pose_euler()) is None):
        print("\"" + controller + "\" lost")
        time.sleep(1)
    curr_pos = [curr_euler[0], curr_euler[2]]
    curr_yaw = curr_euler[4]
    dist = math.dist(start_pos, curr_pos)
    rel_pos = [curr_pos[0] - start_pos[0], curr_pos[1] - start_pos[1]]
    rel_yaw = curr_yaw - start_yaw

    row = [start - begin, curr_pos[0], curr_pos[1], curr_yaw, rel_pos[0], rel_pos[1], rel_yaw]
    print(f"{row[0]:<15.3f}{row[1]:<15.3f}{row[2]:<15.3f}{row[3]:<15.1f}{row[4]:<15.3f}{row[5]:<15.3f}{row[6]:<15.1f}")

    f.write(','.join(map(str, row)) + '\n')

    sleep_time = interval-(time.time()-start)
    if sleep_time>0:
        time.sleep(sleep_time)

if __name__ == '__main__':
    try:
        Path("data").mkdir(parents=True, exist_ok=True)

        filename = input('Filename: ')
        f = open("data/" + filename + ".csv", "w")

        begin = time.time()

        try:
            start_euler = v.devices[controller].get_pose_euler()
        except KeyError:
            print("No controllers found")
            f.close()
            sys.exit(1)

        try:
            start_pos = [start_euler[0], start_euler[2]]
            start_yaw = start_euler[4]
        except TypeError:
            print("\"" + controller + "\" not found")
            f.close()
            sys.exit(1)

        header = ['TIME (s)', 'ABS_X (m)', 'ABS_Y (m)', 'ABS_YAW (deg)', 'REL_X (m)', 'REL_Y (m)', 'REL_YAW (deg)']
        print(f"{header[0]:<15}{header[1]:<15}{header[2]:<15}{header[3]:<15}{header[4]:<15}{header[5]:<15}{header[6]:<15}")
        f.write(','.join(map(str, header)) + '\n')

        while(True):
            main()

    except KeyboardInterrupt:
        f.close()
        print()
