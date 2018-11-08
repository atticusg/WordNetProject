#
# graph - shortest path. G(117798, 300890). Diam: avg:6.22  eff:7.42  max:16 (Wed Nov  7 16:32:33 2018)
#

set title "graph - shortest path. G(117798, 300890). Diam: avg:6.22  eff:7.42  max:16"
set key bottom right
set logscale y 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Number of hops"
set ylabel "Number of shortest paths"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'diam.hyp.png'
plot 	"diam.hyp.tab" using 1:2 title "" with linespoints pt 6
