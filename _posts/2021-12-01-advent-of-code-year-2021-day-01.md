---
title: "Advent of Code: Year 2021, Day 1"
categories:
  - Blog
tags:
  - Advent of Code
  - Scala
---

I am back after not blogging for 6 months. Who knows if I will blog every day, but I am excited for Advent of Code regardless!

This year I am planning on doing everything in Scala, and I am going to focus more on the problem than the prose when/if I blog my solution.

## The Problem

### Part 1

Given a list of integers that looks like the below, count the number of entries that are greater than the previous entry.

```
199
200
208
210
200
207
240
269
260
263
```

So for this example, it would look like this, for an answer of **7**.

```
199 (N/A - no previous measurement)
200 (increased)
208 (increased)
210 (increased)
200 
207 (increased)
240 (increased)
269 (increased)
260 
263 (increased)
```

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/scala/io/github/aaronreidsmith/year2021/Day01.scala)

```scala
object Day01 {
  def main(args: Array[String]): Unit = {
    val input = Using.resource(Source.fromResource("2021/day01.txt"))(_.getLines().map(_.toInt).toSeq)

    val part1 = input.sliding(2).count { case Seq(a, b) => b > a }
    println(s"Part 1: $part1")
  }
}
```

#### Explanation

This solution uses Scala's `sliding` function to group our input into pairs and then counts the number where the second entry is larger than the first.

### Part 2

The problem has changed so that we need to look at sliding windows of size 3 and count the number of windows where the sum of the latter window is larger than the sum of the previous window.

To visualize this, here are the sliding windows with the data from above:

```
199  A      
200  A B    
208  A B C  
210    B C D
200  E   C D
207  E F   D
240  E F G  
269    F G H
260      G H
263        H
```

The sums of those windows are:

```
A: 607 (N/A - no previous sum)
B: 618 (increased)
C: 618 
D: 617 
E: 647 (increased)
F: 716 (increased)
G: 769 (increased)
H: 792 (increased)
```

So the answer to part 2 with the example data is **5**

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/scala/io/github/aaronreidsmith/year2021/Day01.scala)

```scala
object Day01 {
  def main(args: Array[String]): Unit = {
    val input = Using.resource(Source.fromResource("2021/day01.txt"))(_.getLines().map(_.toInt).toSeq)

    val part1 = input.sliding(2).count { case Seq(a, b) => b > a }
    println(s"Part 1: $part1")

    val part2 = input.sliding(4).count { case Seq(a, _, _, d) => d > a }
    println(s"Part 2: $part2")
  }
}
```

#### Explanation

The naive answer would be something like this:

```scala
input.sliding(3).sliding(2).count { case Seq(a, b) => b.sum > a.sum }
```

However, the overlapping members don't matter, so we can save some cycles by only comparing every 4th item. Here is how it looks using windows `A` and `B` from above:

```
B - A = (210 + 208 + 200) - (208 + 200 + 199) = 210 + 208 + 200 - 208 - 200 - 199 = 210 - 199 = 11
```

## Final Thoughts

A good little puzzle to dip our toes in the water this year. Looking forward to the rest of the year! Happy Advent of Code!
