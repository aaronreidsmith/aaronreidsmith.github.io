---
title: "Perl Weekly Challenge 88"
last_modified_at: 2020-12-01T08:40:30-05:00
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

I have always been a fan of Perl (and its younger brother Raku), but, since leaving the Bioinformatics world, have not found any real-world scenarios to flex those muscles.

I recently stumbled upon the [Perl Weekly Challenge](https://perlweeklychallenge.org/) and decided it would be a great way to keep up-to-date with the community. I participated for the first time this week and thought it would be fun to do a write-up of how I approached the problems. In the future, I will start publishing my blogs earlier in the week so that I can include a link to it in my PR.

So, without further ado, let's dive in.

## Task 1: Array of Product

You are given an array of positive integers `@N`.

Write a script to return an array `@M` where `$M[i]` is the product of all elements of `@N` except the index `$N[i]`.

### Example 1

```
Input:
    @N = (5, 2, 1, 4, 3)
Output:
    @M = (24, 60, 120, 30, 40)

    $M[0] = 2 x 1 x 4 x 3 = 24
    $M[1] = 5 x 1 x 4 x 3 = 60
    $M[2] = 5 x 2 x 4 x 3 = 120
    $M[3] = 5 x 2 x 1 x 3 = 30
    $M[4] = 5 x 2 x 1 x 4 = 40
```

### Example 2

```
Input:
    @N = (2, 1, 4, 3)
Output:
    @M = (12, 24, 6, 8)

    $M[0] = 1 x 4 x 3 = 12
    $M[1] = 2 x 4 x 3 = 24
    $M[2] = 2 x 1 x 3 = 6
    $M[3] = 2 x 1 x 4 = 8
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-088/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any specific implementation comments.

```
subset PositiveInt of Int where { $_ ~~ Int && $_ > 0 } # [1]

sub MAIN(*@N where all(@N) ~~ PositiveInt && @N.elems > 0) {
    my $product = [*] @N;         # [2]
    my @M = @N.map: $product / *; # [3]
    say @M;
}
```

This program runs as such:

```
$ raku ch-1.raku 5 2 1 4 3
[24 60 120 30 40]

$ raku ch-1.raku 2 1 4 3
[12 24 6 8]
```

### Explanation

My day job is 100% Scala, so I try to approach everything with an immutable and functional approach, ideally with only one pass through the input list.

The approach I took reminded me of multiplying fractions by the unit fraction to remove the denominator. For example `1/4 x 4/4 = 1`.

Here is the approach applied to example 1 above:

```
$M[0] = (5 x 2 x 1 x 4 x 3) / 5 = 24
$M[1] = (5 x 2 x 1 x 4 x 3) / 2 = 60
$M[2] = (5 x 2 x 1 x 4 x 3) / 1 = 120
$M[3] = (5 x 2 x 1 x 4 x 3) / 4 = 30
$M[4] = (5 x 2 x 1 x 4 x 3) / 3 = 40
```

#### Specific comments

1. The problem states we are given an array of positive integers, but it never hurts to validate. Raku gives us the `subset` keyword to easily define subsets of other types. In this case, the element has to be an integer and must be greater than 0. We then use this subset in the `MAIN` subroutine's signature.

2. As we can see from the modifications to example 1 above, we will always have the product of all items in the numerator and current item in the denominator. We just want to calculate that once, and Raku gives us a simple way of doing that through it's `[*]` operator.

3. This line shows my functional programming background bubbling up. Basically, for each item in the list, we want `$product / $item`, and we want the output collected into a list. This is a _textbook_ case for a map function, so you can see that is what I went with.
  - To a non-Raku user, this may be a little confusing because `*` in a map _literally_ means [`whatever`](https://docs.raku.org/type/Whatever) (more specifically, "whatever input I received") and _not_ `multiply`. The Scala equivalent would be `N.map(item => product / item)`.

  
## Task 2: Spiral Matrix

You are given `m x n` matrix of positive integers.

Write a script to print spiral matrix as list.

### Example 1

```
Input:
    [ 1, 2, 3 ]
    [ 4, 5, 6 ]
    [ 7, 8, 9 ]
Ouput:
    [ 1, 2, 3, 6, 9, 8, 7, 4, 5 ]
```

### Example 2

```
Input:
    [  1,  2,  3,  4 ]
    [  5,  6,  7,  8 ]
    [  9, 10, 11, 12 ]
    [ 13, 14, 15, 16 ]
Output:
    [ 1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10 ]
``` 

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-088/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any specific implementation comments.

```
subset PositiveInt of Int where { $_ ~~ Int && $_ > 0 }

enum Direction <NORTH EAST SOUTH WEST>;

sub MAIN(*@input where all(@input) ~~ PositiveInt && @input.elems > 0) {
    # Ensure our input is exactly square
    my $side-length = @input.elems.sqrt;
    $side-length.Int == $side-length or die "Must be a square matrix";

    # Turn our CLI input into a list of lists (containing both the value and a flag for if we have visted it)
    my @matrix = gather {
        loop (my $i = 0; $i < @input.elems; $i += $side-length) {
            my @row = @input[$i..^$i + $side-length].map({ Hash.new('value', $_, 'visited', False) });
            take @row;
        }
    }

    # Output list and helper function for adding to it
    my @output;
    sub visit-cell($i, $j) {
        my %cell = @matrix[$i][$j];
        if !%cell{'visited'} {
            @output.push(%cell{'value'});
        }
        @matrix[$i][$j]{'visited'} = True;
    }

    # Control vars used below
    my ($min-row, $min-col) = 0, 0;
    my ($max-row, $max-col) = @matrix.elems - 1, @matrix.tail.elems - 1;
    my ($current-row, $current-col, $current-direction) = $min-row, $min-col, EAST;

    # Iterate through matrix in the given directions. Check if we are in a corner or if we have already
    # visited the next cell to determine if we should turn
    while @output.elems != @input.elems {
        visit-cell($current-row, $current-col);
        given $current-direction {
            when EAST {
                if $current-col == $max-col || @matrix[$current-row][$current-col+1]{'visited'} {
                    $current-direction = SOUTH;
                    $current-row += 1;
                } else {
                    $current-col += 1;
                }
            }
            when SOUTH {
                if ($current-row == $max-row && $current-col == $max-col) || @matrix[$current-row+1][$current-col]{'visited'} {
                    $current-direction = WEST;
                    $current-col -= 1;
                } else {
                    $current-row += 1;
                }
            }
            when WEST {
                if $current-col == $min-col || @matrix[$current-row][$current-col-1]{'visited'} {
                    $current-direction = NORTH;
                    $current-row -= 1;
                } else {
                    $current-col -= 1;
                }
            }
            when NORTH {
                # No need to check for special case here, because we always start in the top left
                if @matrix[$current-row-1][$current-col]{'visited'} {
                    $current-direction = EAST;
                    $current-col += 1;
                } else {
                    $current-row -= 1;
                }
            }
        }
    }
    say @output;
}
```

This program runs as such:

```
$ raku ch-2.raku 1 2 3 4 5 6 7 8 9
[1 2 3 6 9 8 7 4 5]

$ raku ch-2.raku 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
[1 2 3 4 8 12 16 15 14 13 9 5 6 7 11 10]
```

### Explanation

I _tried_ to do this one functionally, but I just couldn't find a way to do it.

The basics of the above program are as follows:

1. We take some input and make sure it is square
  - Couldn't find a better way to do this, but I am all ears if anyone knows. Scala has an `isWhole` function on its number classes, so I basically did that check myself:

    ```
    my $side-length = @input.elems.sqrt;
    $side-length.Int == $side-length or die "Must be a square matrix";
    ```

2. Convert that into an actual matrix that looks like this (using example 1):

	```
	[
		[{value: 1, visited: False}, {value: 2, visited: False}, {value: 3, visited: False}],
		[{value: 4, visited: False}, {value: 5, visited: False}, {value: 6, visited: False}],
		[{value: 7, visited: False}, {value: 8, visited: False}, {value: 9, visited: False}],
	]
	```
	
3. 	Starting in the top left corner, walk to the right (`EAST`) with the following logic: if we hit the edge or a visited cell, turn right, else keep going.
  - We always "visit" the current cell by marking it visited and adding it to the output

**That's it!**

What I like about this solution is that it is pretty simple. In fact, steps one and two could be drastically simplified if this program trusted that it would always get a square matrix rather than a 1D matrix from the command line. Additionally, as a fan of pattern matching, I am glad I got to use a `given/when` clause here.

What I dislike about this solution is the mutability (`@output.push()`) and the fragility of it. For example, if the problem were tweaked to walk counter clockwise, I would basically have to re-write the actual "business logic" of this solution.

## Final Thoughts

This was a fun dive back into the world of Perl, and I am looking forward to more of these challenges and blogs going forward.

I am hoping someone can prove me wrong and solve the second problem functionally. Looking forward to seeing everyone's solutions and interacting more with the community! 

#### PS

It seems the theme I am using for my blog does not support `raku` code highlighting yet. I am using Jekyll; any plugin I can use to circumvent this?
