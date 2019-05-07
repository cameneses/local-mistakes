def load_log(filename, exclussion):
    resources = []
    cases = {}

    with open(filename, "r") as logfile:
        first = True
        for line in logfile:
            if first:
                first = False
                continue
            data = line.strip().split(",")
            if data[0] not in cases.keys():
                cases[data[0]] = []
            if data[4] not in exclussion:
                cases[data[0]].append(data[4])

    return cases

def load_exclussions(filename):
    exclussions = []
    with open(filename, "r") as file:
        for line in file:
            exclussions.append(line.strip())
    return exclussions