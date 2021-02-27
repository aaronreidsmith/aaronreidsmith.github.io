---
title: "Perl Weekly Challenge 101"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

This week was pretty fun -- solution one ends up re-using some code from [my first post](https://aaronreidsmith.github.io/blog/perl-weekly-challenge-088/) (Challenge 88), and solution two explores [Barycentric coordinates](https://en.wikipedia.org/wiki/Barycentric_coordinate_system)! No ugly one-liners this week. 🙂

## Task 1: Pack a Spiral

You are given an array `@A` of items (integers say, but they can be anything).

Your task is to pack that array into an `MxN` matrix spirally **counterclockwise**, as tightly as possible. "Tightly" means the absolute value of the difference between `M` and `N` (`|M-N|`) has to be as small as possible.

### Example 1
```
Input: @A = (1,2,3,4)

Output:

    4 3
    1 2

Since the given array is already a 1x4 matrix on its own, but that's not as tight as possible. Instead, you'd spiral it counterclockwise into

    4 3
    1 2
```

### Example 2

```
Input: @A = (1,2,3,4,5,6)

Output:

    6 5 4
    1 2 3

or

    5 4
    6 3
    1 2

Either will do as an answer, because they're equally tight.
```

### Example 3

```
Input: @A = (1,2,3,4,5,6,7,8,9,10,11,12)

Output:

       9  8  7 6
      10 11 12 5
       1  2  3 4

or

       8  7 6
       9 12 5
      10 11 4
       1  2 3
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-101/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
# Finds all factor pairs of a given numbers
sub factors(Int $n) returns Positional {
    my $max = $n.sqrt.floor;
    my $number = 1;
    my @factors;
    while $number <= $max {
        my $potential-factor = $n / $number;
        if $potential-factor == $potential-factor.Int {
            @factors.push(($number.clone, $potential-factor)); # [1]
        }
        $number++;
    }
    @factors;
}

# Formats a 2D array into a multi-line string
sub format(@two-d) returns Str {
    my $width = @two-d[*;*].max(*.chars).chars;                                # [2]
    my @formatted = gather {
        for @two-d -> @row {
            take @row.map(-> $num { sprintf('%*s', $width, $num) }).join(' '); # [3]
        }
    }
    @formatted.join("\n");
}

sub challenge(@A) returns Str {
    enum Direction <NORTH EAST SOUTH WEST>;

    my @factors = factors(@A.elems);
    my ($m, $n) = @factors.min(-> ($a, $b) { abs($a - $b) });
    my (@matrix, @output);
    for ^$m {
        my (@matrix-row, @output-row);
        for ^$n {
            @matrix-row.push({ :!visited });
            @output-row.push(Nil)
        }
        @matrix.push(@matrix-row);
        @output.push(@output-row);
    }

    sub visit-cell($i, $j, $element) { # [4]
        my %cell = @matrix[$i][$j];
        if !%cell<visited> {
            @output[$i][$j] = $element;
        }
        @matrix[$i][$j]<visited> = True;
    }

    my ($min-row, $min-col) = 0, 0;
    my ($max-row, $max-col) = @matrix.elems - 1, @matrix.tail.elems - 1;
    my ($current-row, $current-col, $current-direction) = $min-row, $min-col, EAST;

    for @A -> $element {
        visit-cell($current-row, $current-col, $element);
        given $current-direction {
            when EAST {
                if $current-col == $max-col || @matrix[$current-row][$current-col+1]<visited> {
                    $current-direction = SOUTH;
                    $current-row += 1;
                } else {
                    $current-col += 1;
                }
            }
            when SOUTH {
                if ($current-row == $max-row && $current-col == $max-col) || @matrix[$current-row+1][$current-col]<visited> {
                    $current-direction = WEST;
                    $current-col -= 1;
                } else {
                    $current-row += 1;
                }
            }
            when WEST {
                if $current-col == $min-col || @matrix[$current-row][$current-col-1]<visited> {
                    $current-direction = NORTH;
                    $current-row -= 1;
                } else {
                    $current-col -= 1;
                }
            }
            when NORTH {
                # No need to check for special case here, because we always start in the top left
                if @matrix[$current-row-1][$current-col]<visited> {
                    $current-direction = EAST;
                    $current-col += 1;
                } else {
                    $current-row -= 1;
                }
            }
        }
    }

    format(@output.reverse);
}

sub MAIN(*@A) {
    say challenge(@A);
}
```

This program runs as such:

```
$ raku ch-1.raku 1 2 3 4
4 3
2 1

$ raku ch-1.raku 1 2 3 4 5 6
6 5 4
1 2 3
```

### Explanation

The problem says to wrap the spiral counterclockwise (i.e., start at the bottom left, and fill-in counterclockwise), this is pretty hard to do, given a dynamic-sized array. What I did instead was start at the top left, fill in clockwise, then reverse (mirror) the outer array, so the spiral started at the bottom left.

Here is the basic logic:

1. Find all the factors of the length of the input array.
2. Find the pair of `M` and `N` such that `|M-N|` is minimized  
  - Because of the way we find the factors, `M` will always be `<= N`, so we will have horizontal output as opposed to the vertical output.
3. Define the 2D array with empty cells (`@output`), as well as a separate companion array (`@matrix`) that keeps track of visited cells.
4. Traverse through the input array, keeping track of visited cells in `@matrix`, and filling in `@output`.
5. Once `@output` has been filled in, reverse it, and format it into the expected output string.

#### Specific comments

1. I found it interesting that I had to use `$number.clone` here, but if I just used `$number`, all the pairs in the output ended up with the same `M` value.
2. `[*;*]` is the way to flatten a 2D array. If it were a 3D array you would use `[*;*;*]` and the pattern continues for more-nested arrays. An interesting quirk of Raku.
3. Normally in `sprintf` we would do something like `%2s` to say we want to pad something to two characters. However, since the width is variable, we are able to use `%*s` and pass the width in as an argument.
4. The `visit-cell` subroutine needs to be defined within `challenge` because it is a [closure](https://stackoverflow.com/a/7464475/10696164), meaning it has access to the variables defined within `challenge`, but outside `visit-cell`. In this case, it is accessing `@output` and `@matrix`.
  
## Task 2: Origin-containing Triangle

You are given three points in the plane, as a list of six coordinates: `A=(x1,y1)`, `B=(x2,y2)` and `C=(x3,y3)`.

Write a script to find out if the triangle formed by the given three coordinates contain origin `(0,0)`.

Print `1` if found otherwise `0`.

### Example 1

```
Input: A=(0,1), B=(1,0) and C=(2,2)

Output: 0 because that triangle does not contain (0,0).
```

### Example 2

```
Input: A=(1,1), B=(-1,1) and C=(0,-3)

Output: 1 because that triangle contains (0,0) in its interior.
```

### Example 3

```
Input: A=(0,1), B=(2,0) and C=(-6,0)

Output: 1 because (0,0) is on the edge connecting B and C.
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-101/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
class Point {
    has Int $.x;
    has Int $.y;

    multi method new($x, $y) { # [1]
        self.bless(:$x, :$y);
    }
}

sub challenge(Point $A, Point $B, Point $C, Point $target = Point.new(0, 0)) returns Int {
    my $area = 0.5 * (-$B.y * $C.x + $A.y * (-$B.x + $C.x) + $A.x * ($B.y - $C.y) + $B.x * $C.y);
    my $s = 1 / (2 * $area) * ($A.y * $C.x - $A.x * $C.y + ($C.y - $A.y) * $target.x + ($A.x - $C.x) * $target.y);
    my $t = 1 / (2 * $area) * ($A.x * $B.y - $A.y * $B.x + ($A.y - $B.y) * $target.x + ($B.x - $A.x) * $target.y);
    (0 <= $s <= 1 && 0 <= $t <= 1 && $s + $t <= 1).Int;
}

sub MAIN(Int $x1, Int $y1, Int $x2, Int $y2, Int $x3, Int $y3) {
    say challenge(
        Point.new($x1, $y1),
        Point.new($x2, $y2),
        Point.new($x3, $y3)
    );
}
```

This program runs as such:

```
$ raku ch-2.raku 0 1 1 0 2 2
0

$ raku ch-2.raku 1 1 -1 1 0 -3
1
```

### Explanation

This solution is essentially [this StackOverflow answer](https://stackoverflow.com/a/14382692/10696164) combined with [this StackOverflow answer](https://stackoverflow.com/a/2049712/10696164) with classes instead of individual points. I won't pretend I understand [Barycentric coordinates](https://en.wikipedia.org/wiki/Barycentric_coordinate_system), but it was easy enough to translate the solution into Raku. We do the following:

1. Turn our six integers into `Point` objects, so we can reference them via `$point.x` and `$point.y`.
2. Find the area of the triangle defined by the three points.
3. Use the area to find the Barycentric values `s` and `t`.
4. If `0 <= s <= 1` and `0 <= t <= 1` and `s + t <= 1`, then the target point (`(0,0)` by default, but can be anything) is in the triangle, otherwise it is not.
5. Cast the above boolean to an integer, because that is what is requested in the challenge.

#### Specific Comments

I think the linked StackOverflow questions do a better job of describing Barycentric coordinates than I can, so I just have one implementation comment.

1. It's much easier to deal with this problem with the `Point` object. However, defining instances of classes in Raku is quite verbose; by default, it would be like this: `Point.new(x => $x1, y => $y1)`. We define our own `new` method that just takes positional arguments and internally calls the named arguments via `bless`. `self.bless(:$x, :$y)` is shorthand for `self.bless(x => $x, y => $y)`. In fact, this `Point` implementation is actually [the example](https://docs.raku.org/routine/bless) for the `bless` method.

## Final Thoughts

Nothing much to add this week. See y'all next week!