def to_seconds(time):
    hour, minute, second = map(int, time.split(":"))

    return 3600 * hour + 60 * minute + second


def to_hms(seconds):
    hour, rest = divmod(seconds, 3600)
    minute, second = divmod(rest, 60)

    return f"{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}"


def solution(play_time, adv_time, logs):
    play_seconds = to_seconds(play_time)
    adv_seconds = to_seconds(adv_time)
    play_counts = [0] * (play_seconds + 1)
    LOG_COUNT = len(logs)

    start_times = []
    end_times = []

    for log in logs:
        start_time, end_time = log.split("-")
        start_times.append(to_seconds(start_time))
        end_times.append(to_seconds(end_time))

    start_times.sort()
    end_times.sort()

    s_idx, e_idx = 0, 0

    for t in range(play_seconds + 1):
        while s_idx < LOG_COUNT and start_times[s_idx] == t:
            s_idx += 1
        while e_idx < LOG_COUNT and end_times[e_idx] == t:
            e_idx += 1
        play_counts[t] = s_idx - e_idx

    for idx in range(1, play_seconds + 1):
        play_counts[idx] += play_counts[idx - 1]

    max_accumulates = play_counts[adv_seconds - 1]
    adv_start_time = 0

    for s in range(1, play_seconds - adv_seconds + 1):
        cnt_accumulates = play_counts[s + adv_seconds - 1] - play_counts[s - 1]

        if cnt_accumulates > max_accumulates:
            max_accumulates = cnt_accumulates
            adv_start_time = s

    return to_hms(adv_start_time)



print(solution("02:03:55", "00:14:15", ["01:20:15-01:45:14", "00:40:31-01:00:00", "00:25:50-00:48:29", "01:30:59-01:53:29", "01:37:44-02:02:30"]))
print(solution("99:59:59", "25:00:00", ["69:59:59-89:59:59", "01:00:00-21:00:00", "79:59:59-99:59:59", "11:00:00-31:00:00"]))
print(solution("50:00:00", "50:00:00", ["15:36:51-38:21:49", "10:14:18-15:36:51", "38:21:49-42:51:45"]))
