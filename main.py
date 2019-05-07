import datetime

resources = []
cases = {}

not_relevant = ["Prepare implements",
                "Hand washing",
                "Get in sterile clothes",
                "Clean puncture area",
                "Drap puncture area",
                "Ultrasound configuration",
                "Gel in probe",
                "Cover probe",
                "Put sterile gel",
                "Position probe",
                "Position patient",
                "Anatomic identification",
                "Doppler identification",
                "Compression identification"]

very_relevant = ["Puncture",
                 "Remove syringe",
                 "Guidewire install",
                 "Remove trocar",
                 "Widen pathway",
                 "Advance cathether", 
                 "Remove guidewire"]


class Case:

    def __init__(self, resource):
        self.resource = resource
        self.trace = []

    def add_activity(self, activity):
        self.trace.append(activity)

    def __str__(self):
        return self.trace

    def get_only_activities(self):
        activities = []
        for a in self.trace:
            activities.append(a.activity)
        return activities

    def subsequence(self, subseq, seq):
        i, n, m = -1, len(seq), len(subseq)
        try:
            while True:
                i = seq.index(subseq[0], i + 1, n - m + 1)
                if subseq == seq[i:i + m]:
                    return True
        except ValueError:
            return False

    def is_in_trace(self, start, end):
        start_idx = 50
        end_idx = -1
        for i in range(len(self.trace)):
            if self.trace[i].activity == start and start_idx >= 50:
                start_idx = i
            elif self.trace[i].activity == end and end_idx < 0:
                end_idx = i

        return start_idx < end_idx

    def post_check(self):
        checks = ["Check wire in long axis", 
                 "Check wire in short axis"]
        for i in range(len(self.trace)):
            if self.trace[i].activity in checks:
                try:
                    check = self.trace[i].activity
                    post = self.trace[i +1 ].activity
                    print("{} -> {}".format(check, post))
                except:
                    pass

    def print_trace(self):
        for event in self.trace:
            print("{}, {}, {}".format(event.activity, event.start, event.end))

    def execution_order(self):
        apocalypse = ["Puncture",
                 "Remove syringe",
                 "Guidewire install",
                 "Remove trocar",
                 "Widen pathway",
                 "Advance catheter", 
                 "Remove guidewire"]
        permutations = [(0,1), (1,2), (2,3),
                        (3,4), (4,5), (5,6),
                        (0,0), (1,1), (2,2),
                        (3,3), (4,4), (5,5),
                        (6,6)]
        
        for p in permutations:
            order = self.subsequence([apocalypse[p[0]], apocalypse[p[1]]], self.get_only_activities())
            print("{} -> {}: {}".format(apocalypse[p[0]], apocalypse[p[1]], order))
        
    def execution_time(self):
        for event in self.trace:
            if event.activity in very_relevant:
                print("{} -> {} seconds".format(event.activity, event.get_execution_time()))


class Log:

    def __init__(self):
        self.cases = []

    def add_case(self, case):
        self.cases.append(case)

class Event:
    
    def __init__(self, activity, start, end):
        date_format = "%m/%d/%Y %H:%M:%S"
        self.activity = activity
        self.start = datetime.datetime.strptime(start, date_format)
        self.end = datetime.datetime.strptime(end, date_format)

    def get_execution_time(self):
        return (self.end - self.start).seconds

    def __repr__(self):
        return self.activity



with open("CCC19 - Log CSV.csv", "r") as logfile:
    first = True
    for line in logfile:
        if first:
            first = False
            continue
        data = line.strip().split(",")
        if data[0] not in cases.keys():
            cases[data[0]] = Case(data[1])
        if data[4] not in not_relevant:
            cases[data[0]].add_activity(Event(data[4], data[6], data[7]))


for key in cases.keys():
    print("Case: {}".format(key))
    cases[key].post_check()
    print("\n")