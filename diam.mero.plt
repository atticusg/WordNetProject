#
# graph - shortest path. G(117798, 101021). Diam: avg:10.72  eff:13.78  max:25 (Wed Nov  7 16:32:42 2018)
#

set title "graph - shortest path. G(117798, 101021). Diam: avg:10.72  eff:13.78  max:25"
set key bottom right
set logscale y 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Number of hops"
set ylabel "Number of shortest paths"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'diam.mero.png'
plot 	"diam.mero.tab" using 1:2 title "" with linespoints pt 6
