# Notes for Day 11: Chronal Charge

My first solution used brute force.  It took 1 hour 13 minutes to run and give
the correct answer: x=232, y=251, size=12 (power=119).

My second solution used a dynamic programming approach where I used previously
computed sums to compute a new sum for a given square anchored at (x, y).
This required 5 minutes 20 seconds to give the correct answer.

My third solution used a data structure called a summed area table to compute
the power of a square anchored at (x, y) of size z.  This still required
looping over x, y, and size(z) but was much faster to compute the square's 
power.  It gave the correct answer in 19 seconds.

References on the summed area table:

1: https://blog.demofox.org/2018/04/16/prefix-sums-and-summed-area-tables/
2: https://www.geeksforgeeks.org/submatrix-sum-queries/
