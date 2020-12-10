---
title: "Advent of Code: Day 9"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Today we have a classic [sliding window](https://www.geeksforgeeks.org/window-sliding-technique/) problem. But, instead of the traditional iterative approach, we take a recursive approach.

## The Problem

### Part 1

After helping our seatmate fix his Game Boy [yesterday](https://aaronreidsmith.github.io/blog/advent-of-code-day-08/), we find ourselves bored on the plane. Why not pass the time with a little mid-air hacking?

We hook our computer up to the seat-back entertainment center, but it is protected by the e**X**change-**M**asking **A**ddition **S**ystem (XMAS), which is a cipher with a documented weakness.

XMAS starts by sending us 25 numbers (a "preamble"). The 26th number should be the sum of two numbers in the preamble. The 27th number should be the sum of its previous 25 numbers, and so on. Here is an example with a preamble of size 5:

```
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
```

We can see how the pattern works here:

- 40 is the sum of 15 and 25
- 62 is the sum of 15 and 47
- 55 is the sum of 15 and 40
- etc.

The first step in attacking the weakness of the cipher is that exactly one number doesn't follow the pattern. In this case 127 is not the sum of any numbers in the previous 5 (95, 102, 117, 150, 182). Our job is to find the invalid number in the XMAS cipher.


#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/09/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub find-invalid(@list, $window-start = 0, $window-size = 25) {                               # [1]
    my $window-end = $window-start + $window-size - 1;
    my $target-number = @list[$window-end + 1];
    my @preamble-combinations = @list[$window-start..$window-end].combinations(2).map(*.sum); # [2]
    if $target-number ∈ @preamble-combinations {
        find-invalid(@list, $window-start + 1);
    } else {
        $target-number;
    }
}

sub MAIN($file) {
    say find-invalid($file.IO.lines.map(*.Int));
}
```

This runs as such:

```
$ raku main.raku input.txt
31161678
```

#### Explanation

First, we pull all of our numbers into a list and turn them into integers. Once we've done that, we pass the list to `find-invalid`, which will find the sliding window and target value we are looking for (`@list[0..24]` and `@list[25]` in the first iteration). We then find all possible combinations in that 25-item list (via `.combinations(2)`) and sum each pair (vis `.map(*.sum`). If the target _is_ in the list of sums, it is valid, and we go to the next sliding window. If it is _not_, we found our invalid term and return.

##### Specific Comments

1. I added a parameter for `$window-size` here because I had a feeling it would change in part two. It did not, but I left it in here to give an idea of my thought process.
2. I am trying to get more consistent in using dot operators (like `.sum`) rather than mixing paradigms. With that being said, `.map([+] *)` didn't work here to begin with; it wanted me to do something like `.map(-> @pair { [+] @pair })`. I think it was interpreting the `*` as a multiplication operator instead of a `Whatever` star, so it was getting confused. All the more reason to use dot operators, I guess!


### Part 2

The second step of finding the weakness relies on the invalid number found above.

We need to find a contiguous set of numbers (size two or greater) in the input that add up to our invalid input. Once we have found that contiguous range, we need to add the minimum and maximum numbers in the range; that is our encryption weakness.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/09/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub find-invalid(@list, $window-start = 0, $window-size = 25) {
    my $window-end = $window-start + $window-size - 1;
    my $target-number = @list[$window-end + 1];
    my @preamble-combinations = @list[$window-start..$window-end].combinations(2).map(*.sum);
    if $target-number ∈ @preamble-combinations {
        find-invalid(@list, $window-start + 1);
    } else {
        $target-number;
    }
}

sub find-contiguous-range(@list, $target, $start = 0, $end = 1) {
    my @range = @list[$start..$end];
    given @range.sum {
        when * < $target  { find-contiguous-range(@list, $target, $start, $end + 1) }       # [1][2]
        when * == $target { @range }
        when * > $target  { find-contiguous-range(@list, $target, $start + 1, $start + 2) }
    }
}

sub MAIN($file, Bool :$p2 = False) {
    my @input = $file.IO.lines.map(*.Int);
    my $invalid = find-invalid(@input);
    if $p2 {
        my @contiguous-range = find-contiguous-range(@input.reverse, $invalid); # [3]
        say @contiguous-range.min + @contiguous-range.max;
    } else {
        say $invalid;
    }
}
```

This runs as such:

```
# Part 1
$ raku main.raku input.txt
31161678

# Part 2
$ raku main.raku --p2 input.txt
5453868
```

#### Explanation

our `find-invalid` subroutine stays the same, but we now assign the output of it to a variable. If the user is running part one, we print and exit. If the user is running part two, we recursively search the list for a range that adds up to the invalid number. We use the following criteria:

1. Start with window size two
2. If the sum of the window is less than the target, increase it by one and try again
3. If the sum of the window is the target, return the range
4. If the sum of the window is greater than the target, move the start of the window by one, resize to a window of size two and start again


##### Specific Comments
1. This is an annoying trap that I almost fell into: since Raku treats `<foo>` the same as `('foo')`, I was unable to just write `when < $target`. It's annoying to me because I _can_ write `when $target` instead of `when * == $target`, but I left all three with the same pattern for consistency.
2. Either `*` or `$_` can be used here. Since I am using `*` in other places, I used it for consistency.
3. We exploit the fact that our input is _kind of_ in order. When I say _kind of_ I mean all the two-digit numbers are before all the three-digit numbers, etc. Because our invalid number is so large, I started our `contiguous-range` check from the end of the list. This paid off, as the solution did not even finish when starting from the beginning, but finished fairly quickly starting from the end.


## Final Thoughts

I'm realizing how _slow_ Raku is (both to write and to run). It's disappointing because Perl (Raku's older brother) is slow to write, but at least it is fast to run (as far as interpreted languages go). I guess there is a reason [fewer than 200 people](https://github.com/github/linguist/pull/5104#issuecomment-739561686) are using it on GitHub. Regardless, I am committed to finishing the challenge I set forward for my self (barring Day 7 \*shakes fist\*). See y'all for day 10!