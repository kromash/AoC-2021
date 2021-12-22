import math
from collections import defaultdict


def shot_one(x_start, x_end, y_start, y_end):
    y_max = max(abs(y_end), abs(y_start))
    print(int((y_max) / 2 * (y_max - 1)))


def shot_two(x_start, x_end, y_start, y_end):
    x_frames = defaultdict(list)
    y_frames = defaultdict(list)
    x_stopped_in_area = defaultdict(list)
    min_x = int(x_start / math.sqrt(2))
    max_y = abs(y_start)

    for start_velocity in range(0, x_end+1):
        dist = 0
        step = 0
        for x_velocity in range(start_velocity+1, 0, -1):
            dist += x_velocity
            step += 1
            if x_start <= dist <= x_end:
                if start_velocity == 6:
                    print(f'start 6: {step}')
                x_frames[step].append(start_velocity)

        if x_start <= dist <= x_end:
            x_stopped_in_area[step].append(start_velocity)

    for start_velocity in range(-max_y, max_y + 1):
        # print(start_velocity)
        y_dist = 0
        step = 0
        curr_velocity = start_velocity
        while y_dist >= y_start:
            y_dist += curr_velocity
            step += 1
            curr_velocity -= 1
            if y_start <= y_dist <= y_end:

                y_frames[step].append(start_velocity)

    count = 0
    aims = set()
    for step, l in x_frames.items():
        for x in l:
            for y in y_frames[step]:
                aims.add(f'x{x}y{y}')
                count += 1
    for step, l in y_frames.items():
        for y in l:
            for stopped_step, x_items in x_stopped_in_area.items():
                if step >= stopped_step:
                    for x in x_items:
                        aims.add(f'x{x}y{y}')
    print(len(aims))


if __name__ == '__main__':
    shot_input = (265, 287, -103, -58)
    shot_one(*shot_input)
    shot_two(*shot_input)
