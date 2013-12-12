set terminal postscript color colortext
set xrange[0.8:1.2]
set yrange[0:1]
set key left notitle box 3
set xlabel "Ratio"
set ylabel "Cumulative probability"
set notitle
set grid
set output "plot_256.ps"
plot "./output1/152868_256.dat" title "James Flavin",\
	 "./output1/212581_256.dat" title "Stuart Holmes",\
	 "./output1/233082_256.dat" title "James Earl Jones",\
	 "./output1/372839_256.dat" title "Lee Phelps",\
	 "./output1/621468_256.dat" title "Bess Flowers",\
	 "./output1/209799_256.dat" title "Adolf Hitler",\
	 "./output1/22585_256.dat" title "Irving Bacon",\
	 "./output1/245158_256.dat" title "Donald (I) Kerr",\
	 "./output1/433904_256.dat" title "Martin Sheen",\
	 "./output1/74450_256.dat" title "John Carradine";

