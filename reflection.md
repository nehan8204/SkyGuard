# Automation ROI Reflection (SkyGuard)

Automating the 8 selected cases took about 55 minutes (setup ~15 min, writing parametrized
tests ~25 min, CI config ~15 min). Running the same 8 cases by hand takes about 6 minutes per
pass (type coordinates and sensor states, read the result, log it), so ten manual passes cost
about 60 minutes and each pass risks typing mistakes, especially with decimal values such as 120.1
and 14.9. The automated suite finishes in well under a second on every push.

Break-even came at roughly 9-10 runs. For a flight-control feature that is re-tested after every
change, that is reached quickly. The hardest case to automate was F2 (battery exactly 15%) because
the oracle must pin the boundary precisely; a loose check like "not CONTINUE" would let the
off-by-one bug through. False passes could come from importing the wrong build, from expected
values copied from program output, or from missing boundary cases. I validated the oracle with a
deliberately broken build, which failed 4 of 8 tests as intended.

(Replace the minutes with your own measured times.)
