from ldacomp.dataset import Dataset

def test_dataset_first_row():
    dataset = Dataset('data/mitchell-lapata.txt')
    first_row = next(iter(dataset))
    assert first_row.participant == 'participant1'
    assert first_row.instance_type == 'verbobjects'
    assert first_row.s1 == ['knowledge', 'use']
    assert first_row.s2 == ['influence', 'exercise']
    assert first_row.rating == 5
    
