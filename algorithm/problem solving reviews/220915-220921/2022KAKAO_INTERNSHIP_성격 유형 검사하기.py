def solution(survey, choices):
    total_points = {
        'R': 0, 'T': 0, 'C': 0, 'F': 0, 'J': 0, 'M': 0, 'A': 0, 'N': 0
    }

    for idx in range(len(choices)):
        if choices[idx] < 4:
            character_type = survey[idx][0]
            total_points[character_type] += (4 - choices[idx])
        elif choices[idx] > 4:
            character_type = survey[idx][1]
            total_points[character_type] += (choices[idx] - 4)

    result = ""

    for type1, type2 in [['R', 'T'], ['C', 'F'], ['J', 'M'], ['A', 'N']]:
        if total_points[type1] >= total_points[type2]:
            result += type1
        else:
            result += type2

    return result
