---
title: "Advent of Code: Year 2020, Day 24"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---
Merry Christmas Eve! I had a lot more fun with today's challenge than the past few days. It is reminiscent of days [11](https://aaronreidsmith.github.io/blog/advent-of-code-year-2020-day-11/) and [17](https://aaronreidsmith.github.io/blog/advent-of-code-year-2020-day-17/), but with a fun twist. I also solved it using a different data structure due to that twist, so it felt fresh.

## The Problem

### Part 1

We _finally_ made it to the resort, but there is a problem -- they are renovating the lobby floor, and we can't make it to the check-in desk until they are done. Since we are in a rush, we offer to help.

The workers are trying to lay a pattern using hexagonal tiles. All the tiles are white on one side and black on the other; to start, the workers laid them all out in the "white" orientation. The foreman gives us a list that looks like the following:

```
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
```

From an arbitrary starting tile, this defines directions to the tiles that need to be flipped; one set of directions per line. From each tile, there are six directions we can move in: `e`, `se`, `sw`, `w`, `nw`, and `ne`. So the first line above would split into these directions:

```
se se nw ne ne ne w se e sw w sw sw w ne ne w se w sw
```

Once we follow the directions to the appropriate tile, we flip it. One note, some of these tiles may flip and then _flip back_. After all the instructions have been processed, how many tiles are flipped with their black side up?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-24.raku)

See below for explanation and any implementation-specific comments.

```
sub MAIN($file) {
    my $regex = /^(e|se|sw|w|nw|ne)+$/;
    my @instructions =
        $file.IO
        .lines
        .map(-> $line {
            $line.match($regex).map(*.Str).split(' ')
        });
    my $flipped = Set.new;
    for @instructions -> @instruction-set {
        my ($q, $r) = (0, 0);
        for @instruction-set -> $direction {
            given $direction {
                when 'e'  { $q += 1          }
                when 'se' { $r += 1          }
                when 'sw' { $q -= 1; $r += 1 }
                when 'w'  { $q -= 1          }
                when 'nw' { $r -= 1          }
                when 'ne' { $q += 1; $r -= 1 }
            }
        }
        my $tile-key = "$q:$r";    # [1]
        if $tile-key ∈ $flipped {
            $flipped ⊖= $tile-key; # [2]
        } else {
            $flipped ∪= $tile-key; # [3]
        }
    }
    say $flipped.elems;
}
```

This runs as such:

```
$ raku day-24.raku input.txt
459
```

#### Explanation

First things first, we need to split the input into a list of lists, where the inner list contains the individual directions we need to move. We do so by matching each line against a regex and converting that into a list. Next, since a hexagonal grid is kind of an unconventional data structure, I decided to go with a `Set` to store the flipped tiles rather than a `List` or some other traversable.

Now that we have the building blocks, how do we follow these directions? I found this great resource dedicated to [hexagonal grids](https://www.redblobgames.com/grids/hexagons) and how to traverse them. We use something called [axial coordinates](https://www.redblobgames.com/grids/hexagons/#coordinates-axial). Here is a good representation of what is happening:

![Axial Coordinates (credit: Red Blob Games)](https://raw.githubusercontent.com/aaronreidsmith/aaronreidsmith.github.io/master/assets/images/axial-coordinates.png)
<sub>Image credit: [Red Blob Games](https://www.redblobgames.com/grids/hexagons/#coordinates-axial)<sub>

Basically, we move east or west, we increment or decrement our `q` value. Similarly, if we move northwest or southeast, we increment or decrement our `r` value. If we move northeast or southwest, we increment one while decrementing the other. Now that we understand that, it is fairly easy to see what is happening in the `given` block. 

Once we reach our desired tile, we check if it is in our `$flipped` set. If so, we need to remove it (or "un-flip" it); otherwise, it goes _in_ to the `$flipped` set. Finally, we just count the flipped tiles (via `$flipped.elems`).

##### Specific Comments

1. Sets can only contain scalars in Raku (i.e., `Set.new((1, 2, 3))` yields `Set(1, 2, 3)`), so we can't just add the `q` and `r` values to the set as-is. My workaround is to convert them to a string with the format `q:r` so we are able to store them in a set, but still retrieve them easily later.
2. `⊖` is the [symmetric difference](https://en.wikipedia.org/wiki/Symmetric_difference) operator, which removes elements that are present in both sets. In conjunction with the `=` operator, it reassigns to `$flipped`.
3. `∪` is the [set union](https://en.wikipedia.org/wiki/Union_(set_theory)), which returns all the items in both sets cast to a new set. In conjunction with the `=` operator, it reassigns to `$flipped`.

### Part 2

Now we find out that the tiles in the lobby are meant to be a sort-of "living art exhibit." Every day the tiles are flipped according to the following rules:

- Any **black** tile with **zero** or **more than 2** black tiles immediately adjacent to it is flipped to **white**.
- Any **white** tile with **exactly 2** black tiles immediately adjacent to it is flipped to **black**.

The rules are applied simultaneously to every tile; put another way, it is first determined which tiles need to be flipped, then they are all flipped at the same time.

Starting with the layout _after_ part one, what how many tiles will be black after 100 days?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-24.raku)

See below for explanation and any implementation-specific comments.

```
sub adjacent($q, $r) {
    "{$q + 1}:$r",       # [1]
    "$q:{$r + 1}",
    "{$q - 1}:{$r + 1}",
    "{$q - 1}:$r",
    "$q:{$r - 1}",
    "{$q + 1}:{$r - 1}"  # [2]
}

sub MAIN($file, Bool :$p2 = False) {
    my $regex = /^(e|se|sw|w|nw|ne)+$/;
    my @instructions =
        $file.IO
        .lines
        .map(-> $line {
            $line.match($regex).map(*.Str).split(' ')
        });

    my $flipped = Set.new;
    for @instructions -> @instruction-set {
        my ($q, $r) = (0, 0);
        for @instruction-set -> $direction {
            given $direction {
                when 'e'  { $q += 1          }
                when 'se' { $r += 1          }
                when 'sw' { $q -= 1; $r += 1 }
                when 'w'  { $q -= 1          }
                when 'nw' { $r -= 1          }
                when 'ne' { $q += 1; $r -= 1 }
            }
        }
        my $tile = "$q:$r";
        if $tile ∈ $flipped {
            $flipped ⊖= $tile;
        } else {
            $flipped ∪= $tile;
        }
    }

    if $p2 {
        for (^100) {
            my $flipped-this-round = Set.new;
            my $unflipped-this-round = Set.new;
            my @q-range = $flipped.keys.map(*.split(':')[0].Int).minmax;
            my @r-range = $flipped.keys.map(*.split(':')[1].Int).minmax;
            for (@q-range.min - 1 .. @q-range.max + 1) -> $q {
                for (@r-range.min - 1 .. @r-range.max + 1) -> $r {
                    my $tile = "$q:$r";
                    my $adjacent-flipped = adjacent($q, $r).grep(* ∈ $flipped).elems;
                    if $tile ∈ $flipped {
                        if $adjacent-flipped == 0 || $adjacent-flipped > 2 {
                            $unflipped-this-round ∪= $tile;
                        }
                    } else {
                        if $adjacent-flipped == 2 {
                            $flipped-this-round ∪= $tile;
                        }
                    }
                }
            }
            $flipped ∪= $flipped-this-round;
            $flipped ⊖= $unflipped-this-round;
        }
    }
    say $flipped.elems;
}
```

This runs as such:

```
$ raku day-24.raku input.txt
459

$ raku day-24.raku --p2 input.txt
4150
```

#### Explanation

I had some initial difficulty here because I didn't have a good data structure to traverse, so how would this work? Turns out we don't need it, we just need the min and max black tile coordinates (from our arbitrary starting tile), and we can traverse that way! 

All that was added was the `if $p2 {...}` block, as well as a helper function (`adjacent`) to help find adjacent tiles. The logic here is fairly straightforward:

1. Once we have our layout for part 1, we kick off 100 iterations.
2. Within each iteration, to not affect `$flipped` state until the end, we create 2 new sets: `$flipped-this-round` and `$unflipped-this-round`.
3. We find the minimum and maximum `q` and `r` values and go one tile further (we need to account for the neighbors of those outer black tiles).
4. For each tile in our area we check if it is black (`$tile ∈ $flipped`).
    - If so, we check if it has either `0` or `>2` black neighbors. If so, it goes in the `$unflipped-this-round` set.
    - If it is a white tile, we check if it has exactly `2` black neighbors. If so, it goes in the `$flipped-this-round` set.
5. We update `$flipped` by unioning it with `$flipped-this-round` and removing the `$unflipped-this-round` elements via symmetric set difference.

After 100 round, just like part one, we count our black tiles via `$flipped.elems`!

##### Specific comments

1. Parentheses are optional when constructing a list in Raku. In this case, I felt it read better to not use them.
2. Additionally, semicolons are optional _for the last expression in a block_. You have seen this before (look at those `given/when` blocks, for example), but I have never called it out. Similarly, I felt it read better without it here.

## Final Thoughts

I had fun with this one! Maybe it helps that I am actually off for the holidays and don't have to rush through it before or after work. Looking forward to crossing the finish line tomorrow!
