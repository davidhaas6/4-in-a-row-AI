import pstats

# https://docs.python.org/2/library/profile.html
file_name = 'stats'

p = pstats.Stats(file_name)

metrics = ['tottime', 'cumulative']

for met in metrics:
    p.sort_stats(met).print_stats()
    print '------------'
