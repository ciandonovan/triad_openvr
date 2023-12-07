import triad_openvr
import time
import sys
import math
from pathlib import Path

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

controller = "controller_1"

if len(sys.argv) == 1:
    interval = 1/25
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False

def main():
    start = time.time()

    curr_euler = v.devices[controller].get_pose_euler()
    curr_pos = [curr_euler[0], curr_euler[2]]
    curr_yaw = curr_euler[4]
    dist = math.dist(start_pos, curr_pos)
    rel_pos = [curr_pos[0] - start_pos[0], curr_pos[1] - start_pos[1]]
    rel_yaw = curr_yaw - start_yaw

    row = [start - begin, curr_pos[0], curr_pos[1], curr_yaw, rel_pos[0], rel_pos[1], rel_yaw]
    print('{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}'.format(*row))

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

        start_euler = v.devices[controller].get_pose_euler()
        start_pos = [start_euler[0], start_euler[2]]
        start_yaw = start_euler[4]

        header = ['TIME (s)', 'ABS_X (m)', 'ABS_Y (m)', 'ABS_YAW (deg)', 'REL_X (m)', 'REL_Y (m)', 'REL_YAW (deg)']
        print('{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}'.format(*header))
        f.write(','.join(map(str, header)) + '\n')

        while(True):
            main()

    except KeyboardInterrupt:
        f.close()
        print()
