from aveMinutes import main
import cProfile

p = cProfile.Profile()
p.runcall(main)
p.print_stats()
