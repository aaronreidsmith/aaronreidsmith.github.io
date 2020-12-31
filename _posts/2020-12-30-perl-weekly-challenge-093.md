---
title: "Perl Weekly Challenge 93"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

I was _going_ to stop adding my test cases (to the blog, not the code) this week, but after writing a solution that passed the provided test cases for part one, I wrote a new test that it failed and had to rewrite the whole thing. Because of that, today's solutions still have the tests included. Additionally, in part one, I will go through both the failing solution and the corrected one.

## Task 1: Max Points

You are given set of co-ordinates `@N`.

Write a script to count maximum points on a straight line when given co-ordinates plotted on 2-d plane.

### Example 1

```
|
|     x
|   x
| x
+ _ _ _ _

Input: (1,1), (2,2), (3,3)
Output: 3
```

### Example 2

```
|
|
| x       x
|   x
| x   x
+ _ _ _ _ _

Input: (1,1), (2,2), (3,1), (1,3), (5,3)
Output: 3
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-093/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

#### First Attempt

```
sub challenge(@pairs) {
    my %lines;
    my $already-compared = Set.new;

    for @pairs -> @pair {
        my @pairs-to-compare = @pairs.grep(* ne @pair);

        for @pairs-to-compare -> @other-pair {
            my ($x1, $y1) = @pair;
            my ($x2, $y2) = @other-pair;

            next if "$x1,$y1:$x2,$y2" ∈ $already-compared || "$x2,$y2:$x1,$y1" ∈ $already-compared; # [1]

            my $numerator = $y2 - $y1;
            my $denominator = $x2 - $x1;

            # Find the slope
            my $m = $denominator == 0 ?? 'undefined' !! $numerator / $denominator;

            # If it is a vertical line, use the x-intercept for uniqueness
            my $b = $m eq 'undefined' ?? @pair[1] !! @pair[1] - ($m * @pair[0]);

            # Slope and y-intercept (or x-intercept) are unique, so this is all we need
            %lines{"$m:$b"}++;                                                           # [2]

            $already-compared ∪= "$x1,$y1:$x2,$y2";
        }
    }
    %lines.max(-> $entry { $entry.value }).value;
}

multi sub MAIN(*@N where all(@N) ~~ Int && @N.elems %% 2) { # [3]
    my @pairs = @N.map(-> $x, $y { ($x, $y) });
    say challenge(@pairs);
}

multi sub MAIN(Bool :$test) {
    use Test;

    my @tests = (
        (((1, 1), (2, 2), (3, 3)), 3),
        (((1, 1), (2, 2), (3, 1), (1, 3), (5, 3)), 3),
        (((1, 1), (2, 1), (3, 1), (4, 1)), 4)
    );

    for @tests -> (@pairs, $expected) {
        is(challenge(@pairs), $expected);
    }

    done-testing;
}
```

This program runs as such:

```
$ raku ch-1.raku 1 1 2 2 3 3
3

$ raku ch-1.raku --test
ok 1 - 
ok 2 - 
not ok 3 - 
1..3
# Failed test at /home/asmith/perlweeklychallenge-club/challenge-093/aaronreidsmith/raku/ch-1.raku line 47
# expected: '4'
#      got: '6'
# You failed 1 test of 3
```

#### Corrected Solution

As you can see, the above solution fails for my added test case. We will explore this below, but here is the corrected version (with an additional test case):

```
class Point {
    has $.x;
    has $.y;

    multi method new($x, $y) { # [4]
        self.bless(:$x, :$y);
    }
}

class Line {
    has $.slope;
    has $.x-intercept;
    has $.y-intercept;
    has Set $.points is rw;
}

sub challenge(@points) {
    my %lines;
    for @points.kv -> $index, $point {
        for @points[$index+1..*] -> $other-point {
            my $numerator = $other-point.y - $point.y;
            my $denominator = $other-point.x - $point.x;

            my $slope = $denominator == 0 ?? 'undefined' !! $numerator / $denominator;

            my $y-intercept;
            if $slope eq 'undefined' {
                $y-intercept = $point.y == 0 ?? 0 !! 'undefined';
            } else {
                $y-intercept = $point.y - ($slope * $point.x);
            }

            my $x-intercept;
            if $slope eq 'undefined' {
                $x-intercept = $point.x;
            } elsif $slope == 0 {
                $x-intercept = 'undefined'
            } else {
                $x-intercept = -$y-intercept / $slope;
            }

            my $points = Set.new("{$point.x},{$point.y}", "{$other-point.x},{$other-point.y}");

            my $key = "$slope,$x-intercept,$y-intercept"; # [5]
            
            if %lines{$key}:exists {
                %lines{$key}.points ∪= $points;
            } else {
                %lines{$key} = Line.new(:$slope, :$x-intercept, :$y-intercept, :$points);
            }
        }
    }
    %lines.max({ $_.value.points.elems }).value.points.elems;
}

multi sub MAIN(*@N where all(@N) ~~ Int && @N.elems %% 2) {
    my @pairs = @N.map(-> $x, $y { Point.new($x, $y) });
    say challenge(@pairs);
}

multi sub MAIN(Bool :$test) {
    use Test;

    my @tests = (
        ((Point.new(1, 1), Point.new(2, 2), Point.new(3, 3)), 3),
        ((Point.new(1, 1), Point.new(2, 2), Point.new(3, 1), Point.new(1, 3), Point.new(5, 3)), 3),
        ((Point.new(1, 1), Point.new(2, 1), Point.new(3, 1), Point.new(4, 1)), 4),
        ((Point.new(1, 1), Point.new(1, 2), Point.new(2, 1), Point.new(3, 1), Point.new(4, 1)), 4)
    );

    for @tests -> (@points, $expected) {
        is(challenge(@points), $expected);
    }

    done-testing;
}
```

This program runs as such:

```
$ raku ch-1.raku 1 1 2 2 3 3
3

$ raku ch-1.raku --test
ok 1 - 
ok 2 - 
ok 3 - 
ok 4 -
1..4
```

### Explanation

For both of these there is some logic in `MAIN` that I will explain once. Basically, we expect the user to pass us one or more integers, and they have to pass us an _even_ number of integers so that we can split it into pairs. We then pass this to the `challenge` subroutine.

**First Attempt**

The logic here is as follows:

1. For each point, compare it to each other point.
2. During the comparison calculate both the slope and (`$m`) and the y-intercept (`$b`)
3. Store the slope/y-intercept combo in a Hash called `%lines`.
    - Increment if it exists, otherwise, set to `1`.
4. Comparing `(1, 1) <-> (2, 2)` and `(2, 2) <-> (1, 1)` is the same thing, so we store that in a `Set` to save ourselves a few cycles.
5. Finally, find the maximum entry by value and return it.

This logic breaks down in the case of a horizontal line (see test number 3). The reason it breaks down is because the pairs are evaluated like this:

1. `(1, 1)` and `(2, 1)` -- m = 0, b = 1. New line -- set to 1
2. `(1, 1)` and `(3, 1)` -- m = 0, b = 1. Existing line -- increment to 2
3. `(1, 1)` and `(4, 1)` -- m = 0, b = 1. Existing line -- increment to 3
4. `(2, 1)` and `(1, 1)` -- Same as number 1 -- skip
5. `(2, 1)` and `(3, 1)` -- m = 0, b = 1. Existing line -- increment to 4
6. `(2, 1)` and `(4, 1)` -- m = 0, b = 1. Existing line -- increment to 5
7. `(3, 1)` and `(1, 1)` -- Same as number 2 -- skip
8. `(3, 1)` and `(2, 1)` -- Same as number 5 -- skip
9. `(3, 1)` and `(4, 1)` -- m - 0, b = 1. Existing line -- increment to 6

As you can see, even with four points, we generate an answer of six. My first though was to just take the minimum of the number of points and the longest run we found, which would yield four. However, if we had any points _not_ on the line (look at test 4 the corrected solution), then it would yield the wrong answer as well.

**Corrected Solution**

The logic here is similar, but accounts for the above situation. First, you will notice I added a `Point` and `Line` class, to make things a little easier. The `Line` class also contains a set of points along that line that we can use to de-duplicate if necessary. Once those are defined, the logic is as follows:

1. Compare each point to each _subsequent_ point.
    - There is no need to look at past points, as it results in the "skips" shown above
2. During each comparison we calculate the slope, x-intercept and y-intercept.
    - The reason for this is because if we have an undefined slope (vertical line), we need to know where along the x-axis it falls.
3. Once we have the above calculated, we create a joint key of all 3 to use in a Hash.
4. Using the above key, we look up our string in the `%lines` Hash. If it exists, we add the points used to find it to the points contained in the `Line` object (since it is a set, it will de-duplicate itself automatically). Otherwise, we create a new `Line` object and store it with the key from #3.
5. Finally, we find the `Line` with the most `Point`s and return the number of `Point`s.


#### Specific Comments
 
1. We need to use a string here or else the `Set` will erroneously combine some of our points. Sets flatten their arguments in Raku, which makes it tricky to store nested items. This has been my go-to solution.
2. `Hash` objects behave kind of like default dicts in Python in that if you use `++` on a key that does not exist, it will create the key and increment it to `1`.
3. Raku has an operator specifically for "divisible by." In other languages, you might see `x % 2 == 0` to check if something is divisible by 2, but in Raku you can say `$x %% 2`.
4. Raku, like some other languages, allows us to define multiple constructors. The default one is created for us and takes named arguments. This one takes positional arguments and passes them to the default constructor via `self.bless`.
5. Similar to #1, `Hash` objects always use string keys. So if we need some kind of compound key, we need to cast it to a string as seen here.
  
## Task 2: Sum Path

You are given binary tree containing numbers `0-9` only.

Write a script to sum all possible paths from root to leaf.

### Example 1

```
Input:
     1
    /
   2
  / \
 3   4

Output: 13
as sum two paths (1->2->3) and (1->2->4)
```

### Example 2

```
Input:
     1
    / \
   2   3
  /   / \
 4   5   6

Output: 26
as sum three paths (1->2->4), (1->3->5) and (1->3->6)
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-093/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
subset NodeValue of Str where { $_ ~~ /^<digit>$/ || $_ eq 'Nil' } # [1]

class Node {
    has Node $.left  is rw = Nil; # [2]
    has Node $.right is rw = Nil;
    has Int $.value        = 0;
}

sub build-tree(@array, $root is copy = Nil, Int $i = 0) {
    if $i < @array.elems && @array[$i] ne 'Nil' {
        $root       = Node.new(value => @array[$i].Int);
        $root.left  = build-tree(@array, $root.left, 2 * $i + 1);
        $root.right = build-tree(@array, $root.right, 2 * $i + 2);
    }
    $root;
}

sub challenge(Node $root, @path is copy = ()) {
    my $path-sum = 0;
    with $root {
        @path.push($root.value);

        if !$root.left.defined && !$root.right.defined {
            $path-sum = @path.sum;
        } else {
            $path-sum += challenge($root.left, @path);
            $path-sum += challenge($root.right, @path);
        }
    }
    $path-sum;
}

multi sub MAIN(*@N where all(@N) ~~ NodeValue) {
    my $root = build-tree(@N);
    say challenge($root);
}

multi sub MAIN(Bool :$test) {
    use Test;

    my @tests = (
        (build-tree(('1', '2', 'Nil', '3', '4')), 13),
        (build-tree(('1', '2', '3', '4', 'Nil', '5', '6')), 26),
        (build-tree(('2', '7', '5', '2', '6', 'Nil', '9', 'Nil', '5', '11', '4', 'Nil')), 77)
    );

    for @tests -> ($tree, $expected) {
        is(challenge($tree), $expected);
    }

    done-testing;
}
```

This program runs as such:

```
$ raku ch-2.raku 1 2 Nil 3 4
13

$ raku ch-2.raku 1 2 3 4 Nil 5 6
26

$ raku ch-2.raku --test
ok 1 - 
ok 2 - 
ok 3 - 
1..3
```

### Explanation

The hardest part of this, for me, was giving the user some kind of command line interface to be able to define their own trees (something that wasn't explicitly part of the problem). We basically just use the [array implementation](https://www.geeksforgeeks.org/binary-tree-array-implementation/) of a binary tree where `@array[0]` is the root, `@array[1]` and `@array[2]` are the second row, etc. Anything that is `Nil` is recognized as an empty node (i.e., an [unbalanced tree](http://www.opendatastructures.org/versions/edition-0.1d/ods-java/node37.html)). So, for example, `1 2 Nil 3 4` represents the first example shown above.

`MAIN` does some validation to make sure everything is either a number or `Nil` and then let's `build-tree` convert the array into an actual tree (by creating `Node` objects). Once we have a tree, we give it to `challenge` which implements the following logic:

1. If the node is `Nil` return 0.
    - Technically unnecessary since we check if we are at a terminal node before recursing, but doesn't hurt to have.
2. Push the current node's value into our `@path` list.
3. If we are at a leaf node (no `left` or `right`), then calculate the sum of the path and return.
4. Otherwise, recurse both left and right ith the existing path and add it to the `$path-sum` variable.

#### Specific Comments

1. This line ensures that, even though we are expecting `Str` types, that all of them are either digits or `'Nil'`.
2. By default, class attributes are read only, so by defining them as `is rw` (read/write), we say that they are mutable. Additionally, we assign these attributes default values.

## Final Thoughts

This challenge is a good case study in test-driven development! Be sure to write edge-case tests to make sure everything is behaving as expected. In the case of part one, it was _not_ behaving as expected and required a re-write.