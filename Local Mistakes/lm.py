'''
Load the entire log into memory
'''


def log_reader(path):
    cases = []
    events = {}
    with open(path, "r") as file:
        next(file)
        '''
        case is CASEID
        res is RESOURCE
        rd is ROUND
        ev_id is EVENTID
        act is ACTITY
        stg is STAGE
        start is START
        end is END
        v_start is VIDEOSTART
        v_end is VIDEOEND
        '''
        for line in file:
            # case, res, rd, ev_id, act, stg, start, end, v_start, v_end = line.strip().split(",")
            # For this code there aren't necessary all the fields
            case, _, _, _, act, _, _, _, _, _ = line.strip().split(",")
            if case not in cases:
                cases.append(case)
                events[case] = []
            events[case].append(act)
    return cases, events


'''
Load a activity filter from a file
'''


def load_filter_activities(path):
    activities = []
    with open(path, "r") as file:
        for line in file:
            activities.append(line.strip())
    return activities


'''
Given a trace, return a list of activities
that aren't in the activities list
'''


def filter_irrelevants(trace, activities):
    return list(filter(lambda x: x not in activities, trace))


'''
Given a log, return the same log but
applying the filter_irrelevants function
on every trace
'''


def filter_log(cases, events, actitivies):
    filtered_events = {}
    for case in cases:
        filtered_events[case] = filter_irrelevants(events[case], actitivies)
    return filtered_events


'''
Generates a csv file with the case id and the count 
of every activity for it
'''


def activity_rework_count(cases, events):
    with open("activity_rework_count.csv", "w") as file:
        file.write("CASEID,ACTIVITY,COUNT\n")
        for case in cases:
            case_freq = dict((x, events[case].count(x))
                             for x in set(events[case]))
            for k in case_freq.keys():
                line = "{},{},{}\n".format(case, k, case_freq[k])
                file.write(line)


'''
Generates a csv file with the case id, a start
activity, an end activity and the frequency of 
this sequence
'''


def activity_rework(cases, events):
    with open("activity_rework.csv", "w") as file:
        file.write("CASEID,START,END,FREQUENCY\n")
        for case in cases:
            pairs = list(zip(events[case], events[case][1:]))
            edge_freq = [[x, pairs.count(x)] for x in set(pairs)]
            for edge in edge_freq:
                line = "{},{},{},{}\n".format(
                    case, edge[0][0], edge[0][1], edge[1])
                file.write(line)


'''
Given a list of checks, generates a csv file 
with a case id, a start and an end activity,
a check realized between this two activities 
and the frequency, if it occurs.

The trace must contain the checks provided
in the list checks or it will write 
an empty of incomplete csv.
'''


def check_frequency(cases, events, checks):
    with open("check_frequency.csv", "w") as file:
        file.write("EVENTID,START,END,CHECK,FREQUENCY\n")
        for case in cases:
            for check in checks:
                check_idx = [i for i, x in enumerate(
                    events[case]) if x == check]
                if len(check_idx) == 0:
                    continue
                sequences = []
                for i in check_idx:
                    seq = (find_prev_activity(events[case], i, checks),
                           events[case][i], find_next_activity(
                        events[case], i, checks))
                    sequences.append(seq)
                seq_count = [[x, sequences.count(x)] for x in set(sequences)]
                for pair in seq_count:
                    file.write("{},{},{},{},{}\n".format(
                        case, pair[0][0], pair[0][2],
                        pair[0][1], pair[1]))


'''
Given an index, find the next activity that
doesn't belongs to the avoided ones.

Ex: 
trace: ["a", "b", "b", "b", "c"]
index: 2
avoid ["b"]

return: "c"
'''


def find_next_activity(trace, index, avoid):
    for i in range(index, len(trace)):
        if trace[i] not in avoid:
            return trace[i]


'''
Given an index, find the previous activity that
doesn't belongs to the avoided ones.

Ex: 
trace: ["a", "b", "b", "b", "c"]
index: 2
avoid ["b"]

return: "a"
'''


def find_prev_activity(trace, index, avoid):
    for i in range(index-1, -1, -1):
        if trace[i] not in avoid:
            return trace[i]


if __name__ == "__main__":
    # Loading the log into memory
    cases, events = log_reader('CCC19 - Log CSV.csv')

    # Get the list to activities to filter in the log
    knights_activities = load_filter_activities('just_knights.txt')

    # Get only the events that aren't in the activity filter
    filtered_events = filter_log(cases, events, knights_activities)

    # Generate activity_rework_cound.csv
    activity_rework_count(cases, filtered_events)

    # Generate activity_rework.csv
    activity_rework(cases, filtered_events)

    # Generate check_frequency.csv
    check_frequency(cases, filtered_events, [
                    "Check wire in long axis", "Check wire in short axis"])

    # check_frequency(cases, filtered_events, ["Prepare implements",
    # "Hand washing",
    # "Get in sterile clothes",
    # "Clean puncture area",
    # "Drap puncture area"])
