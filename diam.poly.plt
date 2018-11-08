#
# graph - shortest path. G(117798, 108771). Diam: avg:9.85  eff:12.64  max:23 (Wed Nov  7 16:32:34 2018)
#

set title "graph - shortest path. G(117798, 108771). Diam: avg:9.85  eff:12.64  max:23"
set key bottom right
set logscale y 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Number of hops"
set ylabel "Number of shortest paths"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'diam.poly.png'
plot 	"diam.poly.tab" using 1:2 title "" with linespoints pt 6
