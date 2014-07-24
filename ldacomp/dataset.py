# Bismillahi-r-Rahmani-r-Rahim
"""
Class to encapsulate the Mitchell and Lapata dataset.
"""


class DatasetInstance(object):
    def __init__(self, participant, instance_type, version,
                 s1lemma1, s1lemma2, s2lemma1, s2lemma2, rating):
        self.participant = participant
        self.instance_type = instance_type
        self.version = version
        self.s1 = [s1lemma1, s1lemma2]
        self.s2 = [s2lemma1, s2lemma2]
        self.rating = int(rating)

class Dataset(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with open(self.filename) as open_file:
            # Skip the header
            next(open_file)
            for row in open_file:
                yield DatasetInstance(*row.split())
    
        
    def all_lemmas(self):
        lemmas = set()
        for instance in self:
            lemmas |= set(instance.s1 + instance.s2)
        return lemmas
