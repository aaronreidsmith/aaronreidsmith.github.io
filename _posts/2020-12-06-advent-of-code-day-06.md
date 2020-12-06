---
title: "Advent of Code: Day 6"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Well, our old pal [set theory](https://en.wikipedia.org/wiki/Set_theory) reared its ~~ugly~~ beautiful head again today. I'm very happy with the middle ground I found between conciseness and readability with this challenge; only about 11 lines overall for both parts 1 and 2!

## The Problem

### Part 1

On [day four](https://aaronreidsmith.github.io/blog/advent-of-code-day-04/) we helped out airport security with their passport scanner, and [yesterday](https://aaronreidsmith.github.io/blog/advent-of-code-day-05/) we wrote a program to find our seat on the airplane after losing our boarding pass. Today we are about to land, and it's time to fill out customs declaration form.

This form has 26 yes or no questions marked "A" through "Z." We fill ours out quickly and notice the family next to us having some issues with theirs; they ask us for help. Pretty soon we have offered to help everyone on the plane, and we end up with a file that looks like this:

```
abc

a
b
c

ab
ac

a
a
a
a

b
```

Where each family is distinguished by a blank space, and each person's answers are on their own line, and the presence of a letter means that person answered "yes." Additionally, we only count a "yes" once per family. So the above could be interpreted as follows:

- The first group contains one person who answered "yes" to 3 questions: a, b, and c
- The second group contains three people; combined, they answered "yes" to 3 questions: a, b, and c
- The third group contains two people; combined, they answered "yes" to 3 questions: a, b, and c
- The fourth group contains four people; combined, they answered "yes" to only 1 question, a
- The last group contains one person who answered "yes" to only 1 question, b

The sum of these counts is `3 + 3 + 3 + 1 + 1 = 11`.

Our job is to find the sum of distinct "yes" answers (one per question per family) for the entire plane.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/06/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub MAIN($file) {
    say [+] $file.IO
              .lines(:nl-in("\n\n"))                        # [1]
              .map(-> $group {
                (set $group.subst("\n", '', :g).comb).elems # [2]
              });
}
```

This runs as such:

```
$ raku main.raku input.txt
6809
```

#### Explanation

This one is short and sweet due to the tools Raku gives us. First, we read the file in and split it into families (`:nl-in("\n\n")`; see below for details). Then, for each family, we combine everyone's answers into one line, convert it to a list, then convert it to a set (which removes duplicates). We then count the number of elements in each set `.elems` and sum _all_ the sets using the `[+]` metaoperator.

##### Specific Comments

1. By default `.lines` will split the input file on the `\n` and `\r\n` newline characters. But Raku gives us the tools to tell it to split on whatever we want. In this case, we tell it to split on 2 newline characters, which delineate our families. Additionally, as opposed to `IO.slurp`, `IO.lines` is lazy, so it does not pull the whole file into memory; something to think about if we had a large file.
2. `subst` is Raku's string replacement method (not to be confused with `substr`, its substring method). What's important here is the `:g` flag we pass in, which say to replace all newlines in the string rather than just the first one.

### Part 2

As soon as we finished processing everyone's customs forms, we realize we misread the instructions! We don't want to count where _anyone_ answered yes, we want to count where _everyone_ answered yes. We need to tweak our solution quickly before we land!

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/06/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub part-one($group) {
    (set $group.subst("\n", '', :g).comb).elems;
}

sub part-two($group) {
    [∩] $group.split("\n").map(-> $entry { set $entry.comb }); # [1]
}

sub MAIN($file, Bool :$p2 = False) {
    say [+] $file.IO.lines(:nl-in("\n\n")).map($p2 ?? &part-two !! &part-one);
}
```

This runs as such:

```
# Part 1
$ raku main.raku input.txt
6809

# Part 2
$ raku main.raku --p2 input.txt
3394
```

#### Explanation

So the first obvious difference is we refactored our part one solution to its own subroutine, `part-one`, but the logic is the same. Then we added the `part-two` with the new logic.

In `part-two`, rather than combine the whole family's input, we split them into individual people `.split("\n")`, and then convert each person's answers to a set. Finally, we use reduction metaoperator (`[<operator>]`) to apply the [set intersection](https://en.wikipedia.org/wiki/Intersection_(set_theory)) operator to all the sets in the family.

##### Specific Comments

1. Once again, we use the Unicode operator (`∩`) as opposed to the ASCII operator (`(&)`). You may have seen me use the `[+]` or `[*]` metaoperators, but this is a new one. The actual operator here is the bracket pair. Basically, when Raku sees the bracket pair, it just applies the operator inside it to all items in the list. So, in this case, it does something like the following:

```
[∩] (Set(a b c), Set(b c d), Set(c d e)) == Set(a b c) ∩ Set(b c d) ∩ Set(c d e) == Set(c)
```


## Final Thoughts

Nothing much to add to this one today. A short and sweet question with a short and sweet answer!