#!/bin/bash
# 1. add white border
# 2. starting from left top, floodfill all pixels with same color
# 3. replace red with transparency
# 4. trim again to remove 1px border
convert -density 300 quantum-mobile-v3.svg\
     -bordercolor white -border 1x1 \
     -floodfill +0+0 red \
     -transparent red \
     -trim \
     quantum-mobile-v3.png
