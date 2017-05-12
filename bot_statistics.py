import pstats

# https://docs.python.org/2/library/profile.html
file_name = 'seq_each'

p = pstats.Stats(file_name)

metrics = ['tottime']

for met in metrics:
    p.sort_stats(met).print_stats()
    print '------------'
