
import re

# what we want:
#   `dAmn Viper [version] [state] - Build [build] ([stamp]) [series]
#   <[link]>`_
#
# The regex gives us:
#   0 = link
#   1 = link seg 1
#   2 = stamp
#   3 = series
#   4 = .zip
#   5 = dAmn Viper [version] [state] (Build [build])
#   6 = dAmn Viper [version] [state]
#   7 = Build [build]
#
# So we can create this:
#   `\\6 - \\7 (\\2) \\3
#   <\\0>`_
#
# Actual thing: '`\\6 - \\7 (\\2) \\3\n  <\\0>`_'
#

f=open('downloads.rst', 'r')
fd = f.read()
f.close()

data = re.sub('\[((.+)([0-9-]{15})__([^\.]+)(\S+)) (([^\(]+)\(([^\)]+)\))\]\.', "`\\7 - \\8 (\\3) \\4\n  <\\1>`_", fd)
print data
f=open('downloads.rst', 'w')
f.write(data)
f.close()
