def lanternfish(l, days):
    counts = [0] * 9
    for i in l:
        counts[i] += 1
    for day in range(0, days):
        births = counts[0]
        counts = counts[1:] + [0]
        counts[8] = births
        counts[6] += births
    print(sum(counts))


if __name__ == '__main__':
    example = [3, 4, 3, 1, 2]
    d6 = [2, 3, 1, 3, 4, 4, 1, 5, 2, 3, 1, 1, 4, 5, 5, 3, 5, 5, 4, 1, 2, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 4, 1, 3, 1, 4, 1, 1,
          4, 1, 3, 4, 5, 1, 1, 5, 3, 4, 3, 4, 1, 5, 1, 3, 1, 1, 1, 3, 5, 3, 2, 3, 1, 5, 2, 2, 1, 1, 4, 1, 1, 2, 2, 2, 2, 3,
          2, 1, 2, 5, 4, 1, 1, 1, 5, 5, 3, 1, 3, 2, 2, 2, 5, 1, 5, 2, 4, 1, 1, 3, 3, 5, 2, 3, 1, 2, 1, 5, 1, 4, 3, 5, 2, 1,
          5, 3, 4, 4, 5, 3, 1, 2, 4, 3, 4, 1, 3, 1, 1, 2, 5, 4, 3, 5, 3, 2, 1, 4, 1, 4, 4, 2, 3, 1, 1, 2, 1, 1, 3, 3, 3, 1,
          1, 2, 2, 1, 1, 1, 5, 1, 5, 1, 4, 5, 1, 5, 2, 4, 3, 1, 1, 3, 2, 2, 1, 4, 3, 1, 1, 1, 3, 3, 3, 4, 5, 2, 3, 3, 1, 3,
          1, 4, 1, 1, 1, 2, 5, 1, 4, 1, 2, 4, 5, 4, 1, 5, 1, 5, 5, 1, 5, 5, 2, 5, 5, 1, 4, 5, 1, 1, 3, 2, 5, 5, 5, 4, 3, 2,
          5, 4, 1, 1, 2, 4, 4, 1, 1, 1, 3, 2, 1, 1, 2, 1, 2, 2, 3, 4, 5, 4, 1, 4, 5, 1, 1, 5, 5, 1, 4, 1, 4, 4, 1, 5, 3, 1,
          4, 3, 5, 3, 1, 3, 1, 4, 2, 4, 5, 1, 4, 1, 2, 4, 1, 2, 5, 1, 1, 5, 1, 1, 3, 1, 1, 2, 3, 4, 2, 4, 3, 1]
    lanternfish(d6, 256)
