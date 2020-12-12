---
title: "Advent of Code: Day 12"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Today was the first day where I didn't use the same code for parts one and two -- they were just too different! Other than that, this is a classic recursive solution with a hint of middle school algebra.

## The Problem

### Part 1

We finally got on the ferry to our vacation destination after the [day 11](https://aaronreidsmith.github.io/blog/advent-of-code-day-11/) nonsense. However, we hit a patch of bad weather that knocked the navigation computer out. Luckily, as it was dying, it printed out its final instructions, and the captain needs help interpreting what it produced.

The instructions (our input) consist of single-character actions followed by values. Here is an example followed by our interpretation for the captain:

```
F10
N3
F7
R90
F11
```

- Action `N` means to move north by the given value.
- Action `S` means to move south by the given value.
- Action `E` means to move east by the given value.
- Action `W` means to move west by the given value.
- Action `L` means to turn left the given number of degrees.
- Action `R` means to turn right the given number of degrees.
- Action `F` means to move forward by the given value in the direction the ship is currently facing.

Our ship is fairly sophisticated, so it does not need to face the direction it is moving. If we are currently facing east, what is the [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry) from where we started after we execute the instructions?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/12/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub turn-ship($facing-direction, $turning-direction, $degrees) {
    my %turns = (
        N => { L => 'W', R => 'E' },  # [1][2]
        E => { L => 'N', R => 'S' },
        S => { L => 'E', R => 'W' },
        W => { L => 'S', R => 'N' }
    );

    if $degrees == 0 {
        $facing-direction;
    } else {
        my $new-degrees = $degrees - 90;
        my $new-direction = %turns{$facing-direction}{$turning-direction};
        turn-ship($new-direction, $turning-direction, $new-degrees);
    }
}

sub traverse(
    @directions,
    $pointer = 0,
    $current-direction = 'E',
    @current-position = (0, 0)
) {
    if $pointer == @directions.elems {
        @current-position.map(*.abs).sum;
    } else {
        my ($i, $j) = @current-position;
        my $new-pointer = $pointer + 1;
        my $direction = @directions[$pointer].subst('F', $current-direction); # [3]
        given $direction {
            # Traversal directions
            when /(N|E|S|W)(<digit>+)/ {
                my @new-position = do given $/[0].Str {                       # [4]
                    when 'N' { ($i - $/[1].Int, $j) }
                    when 'E' { ($i, $j + $/[1].Int) }
                    when 'S' { ($i + $/[1].Int, $j) }
                    when 'W' { ($i, $j - $/[1].Int) }
                };
                traverse(
                    @directions,
                    $new-pointer,
                    $current-direction,
                    @new-position
                );
            }
            # Turning directions
            when /(L|R)(<digit>+)/ {
                traverse(
                    @directions,
                    $new-pointer,
                    turn-ship($current-direction, $/[0].Str, $/[1].Int),
                    ($i, $j)
                );
            }
        }
    }
}

sub MAIN($file) {
    say traverse($file.IO.lines);
}
```

This runs as such:

```
$ raku main.raku input.txt
1186
```

#### Explanation

`MAIN` only has one line; most of the logic happens in `traverse`. `traverse` is a recursive subroutine that requires: the directions, a pointer to which step we are on, the direction we are currently facing, and an ordered pair describing our current position.

The logic in `traverse` is pretty simple:

- If we are at the end of the list of directions, return the sum of the absolute values of our position (aka the Manhattan distance); otherwise, we will read the next instruction.
- If the next instruction is `N|E|S|W|F`, we simply move our position in the desired direction and go to the next instruction.
- If the next instruction is `L` or `F`, we call the `turn-ship` subroutine that will recursively turn the ship 90° at a time, then go to the next instruction.

##### Specific Comments

1. Keys in hashes are strings by default, so you will notice we only put quotes around the values.
2. `{...}` is the anonymous `Hash` constructor, so it can be used to create a nested hash. You will notice we don't use it for the outer `Hash`; the reason for this is the `%` sigil already denotes that the right-hand-side of the expression is a `Hash`, so it is redundant. In fact, the parentheses are unnecessary as well, but they make it more readable.
3. Whenever we encounter an `F` it just means "go in the direction we are already facing." Rather than have a special `when` block for it, we just replace it with the direction we are already facing.
4. You might have seen me do something like this in the past: 

    ```
    my $y = gather {
        given $y {
            when * { take <value> }
        }
    }.head;
    ```
    
    This is because I am used to the Scala paradigm of something like this:
    
    ```scala
    val y = x match {
      case _ => value
    }
    ```
    
    The problem is `gather/take` returns a list when I just need one value (hence the `.head`). Well, it turns out that there is a subroutine called [`do`](https://docs.raku.org/routine/do) that can prefix any [`Supply`](https://docs.raku.org/type/Supply), which allows the values in the block to be returned/assigned to a variable rather than having to use the `gather/take` trick. It's not the prettiest, but it works!

### Part 2

After all that, it turns out that the instructions had come with interpretation instructions printed on the back. 🤦🏻 Almost all instructions refer to the manipulation of some waypoint relative to the ship. Here is the _real_ interpretation:

- Action `N` means to move the waypoint north by the given value.
- Action `S` means to move the waypoint south by the given value.
- Action `E` means to move the waypoint east by the given value.
- Action `W` means to move the waypoint west by the given value.
- Action `L` means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
- Action `R` means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
- Action `F` means to move forward to the waypoint a number of times equal to the given value.

If we start with a waypoint 1 unit north and 10 units east, what is our final Manhattan distance from our starting position?

#### Solution

For brevity on this one, since the two solutions do not overlap, I did not copy the part one code from above. If you would like to see it, see the link below.

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/12/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
# Part 1 code here
# ...

sub rotate-waypoint(@waypoint, $direction, $degrees) {
    if $degrees == 0 {
        @waypoint;
    } else {
        my ($i, $j) = @waypoint;
        my $new-degrees = $degrees - 90;
        given $direction {
            when 'L' { rotate-waypoint((-$j, $i), $direction, $new-degrees) } # [1]
            when 'R' { rotate-waypoint(($j, -$i), $direction, $new-degrees) }
        }
    }
}

sub traverse-part2(
    @directions,
    $pointer = 0,
    @current-position = (0, 0),
    @waypoint = (-1, 10)        # [2]
) {
    if $pointer == @directions.elems {
        @current-position.map(*.abs).sum;
    } else {
        my ($waypoint-i, $waypoint-j) = @waypoint;
        my $new-pointer = $pointer + 1;
        given @directions[$pointer] {
            # Waypoint translation directions
            when /(N|E|S|W)(<digit>)/ {
                my @new-waypoint = do given $/[0].Str {
                    when 'N' { ($waypoint-i - $/[1].Int, $waypoint-j) }
                    when 'E' { ($waypoint-i, $waypoint-j + $/[1].Int) }
                    when 'S' { ($waypoint-i + $/[1].Int, $waypoint-j) }
                    when 'W' { ($waypoint-i, $waypoint-j - $/[1].Int) }
                };
                traverse-part2(
                    @directions,
                    $new-pointer,
                    @current-position,
                    @new-waypoint
                );
            }
            # Waypoint rotation directions
            when /(L|R)(<digit>+)/ {
                traverse-part2(
                    @directions,
                    $new-pointer,
                    @current-position,
                    rotate-waypoint(@waypoint, $/[0].Str, $/[1].Int)
                );
            }
            # Ship-moving direction
            when /F(<digit>+)/ {
                my $number-of-moves = $/[0].Int;
                my ($i, $j) = @current-position;
                my $new-i = $i + ($number-of-moves * $waypoint-i);
                my $new-j = $j + ($number-of-moves * $waypoint-j);
                traverse-part2(
                    @directions,
                    $new-pointer,
                    ($new-i, $new-j),
                    @waypoint
                );
            }
        }
    }
}

sub MAIN($file, Bool :$p2 = False) {
    my @directions = $file.IO.lines;
    say $p2 ?? traverse-part2(@directions) !! traverse-part1(@directions);
}
```

This runs as such:

```
# Part 1
$ raku main.raku input.txt
1186

# Part 2
$ raku main.raku --p2 input.txt
47806
```

#### Explanation

The logic here is familiar, but just different enough to warrant its own subroutine. The only editing from the original function was to rename `traverse` to `traverse-part1`.

Basically, instead of storing our current direction, we store our waypoint position. When a `N|E|S|W` instruction comes in, we move it accordingly. When a `L|R` instruction comes in, we use a little [middle school algebra](https://calcworkshop.com/transformations/rotation-rules/) to rotate the waypoint (via the `rotate-waypoint` subroutine). And finally, when an `F` instruction comes in, we move towards the way point `N` times, where `N` is the value supplied with the `F` instruction.

##### Specific Comments

1. We were able to exploit the fact that all of our degrees were increments of 90. When we rotate the point `(x, y)` point counter clockwise it becomes `(-y, x)`, and, when we rotate the same point clockwise it becomes `(y, -x)`.
2. Since we are treating the grid as a grid from the top left and growing downward, `(-1, 10)` indicates 1 unit north and 10 units east.

## Final Thoughts

This was a fun little weekend exercise. Almost halfway to the end; see y'all tomorrow!

