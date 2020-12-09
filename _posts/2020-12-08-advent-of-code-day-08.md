---
title: "Advent of Code: Day 8"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Today tripped me up a bit in part 2 due to my lack of understanding around copying objects in Raku. Regardless, we made it through and are now over 30% of the way to the end!

## The Problem

### Part 1

We're still traveling to our destination (see the past few blogs of the [Advent of Code](https://www.adventofcode.com) itself for more backstory).

We are on another flight, and the kid in the seat next to us is having an issue with his Game Boy. We are able to isolate the boot code, and it looks like this:

```
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
```

Where each instruction means the following:

- `nop`: No operation, move to the next entry
- `jmp`: Jump to the entry specified by the number (+1 means next entry, -1 means previous entry, etc.)
- `acc`: Increment an accumulator the specified amount of times, then go to the next entry

The example instructions, as well as our input, create an infinite loop. Our task is to find the value of the accumulator immediately before any instruction is executed a second time.


#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/08/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub accumulate(@instructions is copy, $pointer = 0, $accumulator = 0) { # [1]
    if @instructions[$pointer]<visited> {
        $accumulator;
    } else {
        @instructions[$pointer]<visited> = True;
        given @instructions[$pointer]<operation> {
            when 'acc' {
                accumulate(
                    @instructions,
                    $pointer + 1,
                    $accumulator + @instructions[$pointer]<value>
                );
            }
            when 'jmp' {
                accumulate(
                    @instructions,
                    $pointer + @instructions[$pointer]<value>,
                    $accumulator
                );
            }
            when 'nop' {
                accumulate(@instructions, $pointer + 1, $accumulator);
            }
        }
    }
}


sub MAIN($file) {
    my @cells = $file.IO.lines.map(-> $line {
        my ($operation, $value) = $line.split(' ');
        { :$operation, value => $value.Int, :!visited } # [2]
    });
    say accumulate(@cells);
}
```

This runs as such:

```
$ raku main.raku input.txt
1600
```

#### Explanation

The logic here is fairly simple. First, we split our input into a list of `Hash` objects that look like this:

```
{ operation => 'jmp|acc|nop', value => <value>, visited => False }
```

We then recursively traverse this list of cells until we hit one that is `visited => True`, and we return the accumulator at that point.

##### Specific Comments

1. We mark the `@instructions` variable as a copy so that we can manipulate it in the `accumulate` subroutine without affecting the outer scope.
2. We use two shorthands on this line. The first being `:$operation`, which is shorthand for `operation => $operation`, and the second being `:!visited`, which is shorthand for `visited => False`. I don't really like mixing the paradigms, but IntelliJ was complaining about it, so what are you gonna do? 🤷🏻‍♂️ 


### Part 2

Now that we have a program to interpret the boot code, we find that there is a bug in the boot code itself. Either a `nop` was switched for a `jmp` or vice versa, in exactly one place in the code. Swapping the right code back to its original form will allow the boot code to terminate rather than running forever.

We need to find the value of the accumulator in the terminal solution.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/08/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub accumulate(@instructions is copy, $pointer = 0, $accumulator = 0, $part-two = False) {
    if $part-two && $pointer == @instructions.elems {
        ($accumulator, 'Terminal');
    } elsif @instructions[$pointer]<visited> {
        ($accumulator, 'Infinite');
    } else {
        @instructions[$pointer]<visited> = True;
        given @instructions[$pointer]<operation> {
            when 'acc' {
                accumulate(
                    @instructions,
                    $pointer + 1,
                    $accumulator + @instructions[$pointer]<value>,
                    $part-two
                );
            }
            when 'jmp' {
                accumulate(
                    @instructions,
                    $pointer + @instructions[$pointer]<value>,
                    $accumulator,
                    $part-two
                );
            }
            when 'nop' {
                accumulate(@instructions, $pointer + 1, $accumulator, $part-two);
            }
        }
    }
}


sub MAIN($file, Bool :$p2 = False) {
    my @cells = $file.IO.lines.map(-> $line {
        my ($operation, $value) = $line.split(' ');
        { :$operation, value => $value.Int, :!visited }
    });
    if $p2 {
        my @fixed-instructions = gather {
            for @cells.kv -> $index, %cell {
                given %cell<operation>.Str {
                    when /^[nop|jmp]$/ {                                               # [1]
                        my @cells-copy = @cells.deepmap(-> $entry is copy { $entry }); # [2]
                        my %cell-copy = %cell.deepmap(-> $entry is copy { $entry });
                        when 'nop' {
                            %cell-copy<operation> = 'jmp';
                            @cells-copy[$index] = %cell-copy;
                            take @cells-copy;
                        }
                        when 'jmp' {
                            %cell-copy<operation> = 'nop';
                            @cells-copy[$index] = %cell-copy;
                            take @cells-copy;
                        }
                    }
                }
            }
        };
        say @fixed-instructions
            .map(&accumulate.assuming(*, 0, 0, $p2))
            .grep(-> @pair { @pair[1] eq 'Terminal' })
            .head  # Gives us the first item in the above list
            .head; # Gives us the number in the pair returned from `accumulate`
    } else {
        say accumulate(@cells).head;
    }
}
```

This runs as such:

```
# Part 1
$ raku main.raku input.txt
1600

# Part 2
$ raku main.raku --p2 input.txt
1543
```

#### Explanation

The logic here is fairly straight forward (albeit brute force) as well. Basically, we find all combinations of our input with a single code point change (`@fixed-instructions`), find _all_ solutions to those codes (infinite and terminal), filter down to the terminal solution and print the output.

The hard part here was copying `@cells` multiple times into `@fixed-instructions`. I ran into an issue where all of `@fixed-instructions` was pointing to the same memory address, so after traversing `@fixed-instructions[0]`, the rest of the inputs were tainted. This issue was fixed by the (awkward) `.deepmaps`. See #2 below for additional details.


##### Specific Comments
1. Interestingly `when 'nop' || 'jmp'` does not work here. I suspect it has to do with the fact that `when` operates [very eagerly](https://docs.raku.org/language/control#index-entry-control_flow__given-given) and as soon as it finds a match, it skips the rest of the lines of input. Generally that happens in a code block, but I guess it can happen in the `when` statement itself.
2. I knew I needed a mutable copy of the original input here. Originally I tried `@cells-copy = @cells`, but that didn't work. Eventually I stumbled upon `.clone`, which it seems [_intentionally_ doesn't work](https://docs.raku.org/routine/clone) on `@`- or `%`-sigiled variables. Finally, I [stumbled upon](https://stackoverflow.com/a/38585401/10696164) this awkward `.deepcopy` syntax which is not only incredibly ugly, but also incredibly slow. For reference, part one runs in 0.48 seconds on my machine and part two runs in 28.7 seconds.


## Final Thoughts

Today's problem helped me get back on the functional Raku track after a [frustrating day 7](https://aaronreidsmith.github.io/blog/advent-of-code-day-07/). However, I am going to have to do more digging on copies of iterables in Raku, because a 60x performance decrease is not really acceptable for this kind of thing, especially when the input is relatively small (<1000 lines).