set terminal postscript color colortext
set xrange[0.8:1.2]
set yrange[0:1]
set key left notitle box 3
set xlabel "Ratio"
set ylabel "Cumulative probability"
set notitle
set grid
set output "plot_1024.ps"
plot "./output/152868_1024.dat" title "James Flavin",\
	 "./output/212581_1024.dat" title "Stuart Holmes",\
	 "./output/233082_1024.dat" title "James Earl Jones",\
	 "./output/372839_1024.dat" title "Lee Phelps",\
	 "./output/621468_1024.dat" title "Bess Flowers",\
	 "./output/209799_1024.dat" title "Adolf Hitler",\
	 "./output/22585_1024.dat" title "Irving Bacon",\
	 "./output/245158_1024.dat" title "Donald (I) Kerr",\
	 "./output/433904_1024.dat" title "Martin Sheen",\
	 "./output/74450_1024.dat" title "John Carradine";