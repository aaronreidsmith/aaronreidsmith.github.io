---
title: "Perl Weekly Challenge 100"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

This week was a lot of fun! Challenge 1 threw an additional curve ball at us -- the solution should be a "one-liner." I did my best to fit my solution on one line; the solution itself is 163 characters long.

## Task 1: Fun Time

You are given a time (12 hour / 24 hour).

Write a script to convert the given time from a 12-hour format to 24-hour format and vice versa.

**Ideally we expect a one-liner.**

### Example 1
```
Input: 05:15 pm or 05:15pm
Output: 17:15
```

### Example 2

```
Input: 19:15
Output: 07:15 pm or 07:15pm
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-100/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Str \t) returns Str {
    t~~/(\d+)\:(\d+)\s?([a|p]m)?/;my (\h,\m,\q)=$/[*];sprintf('%02d:%02d%s',q??h==12??q eq'am'??0!!h!!h+(12*(q eq'pm'))!!h==0|12??12!!h%12,m,q??''!!h>=12??'pm'!!'am');
}

# Implementation comments will go in this version of the above solution
sub challenge-expanded(Str \t) returns Str {
    t ~~ /
      (\d+)     # One or more digits (should technically use \d ** {2}, but this is shorter
      \:        # A literal colon character
      (\d+)     # One or more digits (again, should use \d ** {2})
      \s?       # An optional space (to support HH:MMam or HH:MM am)
      ([a|p]m)? # An optional 'am' or 'pm' (to support both 12- and 24-hour time)
    /;

    my (\h, \m, \q) = $/[*]; # [1][2][3]

	 # The logic in here is the same as above, with added parentheses for clarity
    sprintf(
      '%02d:%02d%s', # [4]
      q ??
        (h == 12 ??
          (q  eq 'am' ?? 0 !! h) !!
          h + (12 * ( q eq 'pm'))) !!
        h == 0|12 ?? 12 !! h%12,
      m,
      q ?? '' !! (h >= 12 ?? 'pm' !! 'am')
    );
}

sub MAIN(Str $time) {
    say challenge($time);
}
```

This program runs as such:

```
$ raku ch-1.raku 05:15 pm
17:15

$ raku ch-1.raku 19:15
7:15pm
```

### Explanation

This one is ugly, so I apologize in advance! When I hear "one-liner" I immediately think ["code golf"](https://en.wikipedia.org/wiki/Code_golf). I used every trick I know to make my solution as short as possible while handling all the edge cases (it's pretty easy to handle the given test cases, but the boundaries make things tricky. I tested every possible time in my full solution on GitHub). You'll notice I _heavily_ lean on the ternary operator for all my branching logic.

For what it's worth, this still has some flaws (for example, it will accept the time `99:99am`), but it accepts **all** valid input, so that is good enough for me.

First, we look for a string matching the regex provided (see embedded comment on what we are looking for). From this regex, we extract 3 elements: the hour, the minute, and the qualifier (am/pm) if it exists. Once we have those 3 elements, we pass them to the `sprintf` function for all the logic.

For the hour, we follow the following logic:

- Is there a qualifier?
  - If yes:
    - Is the hour equal to 12?
      - If yes:
        - Is the qualifier equal to `am`?
          - If yes: `hour = 12`
          - If no: `hour` is left alone
      - If no:
        - Is the qualifier equal to `pm`?
          - If yes: `hour = 12 + hour`
          - If no: `hour` is left alone
  - If no:
    - Is the hour equal to 0 or 12?
      - If yes: `hour = 12`
      - If no: `hour = hour % 12`

Minute will always be `0-59`, so we leave it alone.

For the qualifier, we follow the following logic:

- Is there a qualifier?
  - If yes, we are converting to a 24-hour format, so the new qualifier is empty
  - If no:
    - Is the hour greater than or equal to 12?
      - If yes: `qualifier = 'pm'`
      - If no: `qualifier = 'am'`

Finally, `sprintf` handles all the formatting (discussed below).  

#### Specific comments

1. Everywhere where I used a variable, you'll notice I use `\variable-name`. In Raku, there are several [sigils](https://docs.raku.org/language/variables#Sigils): `$` for scalars, `@` for positionals, `%` for associatives, and `&` for functions. There is also the special `\` sigil for [sigilless scalars](https://docs.raku.org/type/Scalar#index-entry-%5c_(sigilless_scalar)). Basically, if a variable is defined as `\variable-name`, we are able to reference it as `variable-name`. This saved me 11 characters, by my count.
2. A match object (returned by the smartmatch operator [`~~`]) creates a variable names `$/`, so that is where that came from. I could just have easily said `my $match = t ~~ <the rest>`, but that would cost my characters.
3. We used [regex capturing](https://docs.raku.org/language/regexes#Capturing) to pull out the hour, minute, and qualifier. Those end up in the match object (`$/`) as `hour = $/[0]`, `minute = $/[1]`, and `qualifier = $/[2]`. We are able to extract _all 3_ elements by using the special `*` index to reference _all_ elements in the array.
4. Raku's [`sprintf` function](https://docs.raku.org/routine/sprintf) is similar to Unix's. It takes a formatting string (`'%02d:%02d%s'`) that describes the output. In this case, we say we want a 2-digit number, then a colon, then another 2-digit number, then a string. Those three elements are filled in with arguments 2-4 (hour, minute, qualifier).
  
## Task 2: Triangle Sum

You are given triangle array.

Write a script to find the minimum path sum from top to bottom.

When you are on index `i` on the current row then you may move to either index `i` or index `i + 1` on the next row.

### Example 1

```
Input: Triangle = [ [1], [2,4], [6,4,9], [5,1,7,2] ]
Output: 8

Explanation: The given triangle

            1
           2 4
          6 4 9
         5 1 7 2

The minimum path sum from top to bottom:  1 + 2 + 4 + 1 = 8

             [1]
           [2]  4
           6 [4] 9
          5 [1] 7 2
```

### Example 2

```
Input: Triangle = [ [3], [3,1], [5,2,3], [4,3,1,3] ]
Output: 7

Explanation: The given triangle

            3
           3 1
          5 2 3
         4 3 1 3

The minimum path sum from top to bottom: 3 + 1 + 2 + 1 = 7

             [3]
            3  [1]
           5 [2] 3
          4 3 [1] 3
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-100/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(@triangle) {
    my @layers = (0..@triangle.end); # [1]
    my @indices = gather {           # [2]
        for @triangle -> @layer {
            take (0..@layer.end).List;
        }
    }
    my @paths = gather {
        for ([X] @indices) -> @path {         # [3]
            my @zipped = @path Z @path[1..*]; # [4]
            my $valid = True;
            for @zipped -> ($a, $b) {
                if $b < $a || $b > $a + 1 {
                    $valid = False;
                    last;
                }
            }
            take @path if $valid;             # [5]
        }
    }
    my @sums = gather {
        my $sum = 0;
        for @paths -> @path {
            for @layers Z @path -> ($layer, $index) {
                $sum += @triangle[$layer][$index];
            }
            take $sum;
            $sum = 0;
        }
    }
    @sums.min;
}

sub MAIN(*@N where all(@N) ~~ Int) {
	 # Some extra logic to turn a list into a triangle
    my ($index, $size) = (0, 1);
    my @triangle;
    while $index <= @N.end {
        my $end-index = $index + $size;

        my @layer = @N[$index..^$end-index];
        @triangle.push(@layer);

        $index = $end-index;
        $size++;
    }
    say challenge(@triangle);
}
```

This program runs as such:

```
$ raku ch-2.raku 1 2 4 6 4 9 5 1 7 2
8
```

### Explanation

The logic here is pretty straightforward:

1. Find how many layers to the triangle there are
2. Find the valid indices of each layer. So, for example 1, this would be something like `((0), (0, 1), (0, 1, 2), (0, 1, 2, 3))`
3. Find all valid paths. "Valid" in this case means that we always move from position `i` to position `i` or `i+1` on the next layer.
4. Find the sum of each valid path.
5. Return the minimum sum out of the valid paths.

#### Specific Comments

1. Raku has a great method for positionals called [`end`](https://docs.raku.org/routine/end). It returns the last index in a list and saves us from confusion (similar to something like `len(list) - 1`).
2. [`gather`](https://docs.raku.org/syntax/gather%20take) is a way to build up a list based on some logic. It can be thought of as a more powerful list comprehension (from Python).
3. [`X`](https://docs.raku.org/routine/X) is the cross product operator. When used like `[X] @list`, it works like this: `[X] ((1, 2, 3), (4, 5, 6), (7, 8, 9)) == (1, 2, 3) X (4, 5, 6) X (7, 8, 9)`. In this case, it creates all possible paths through the triangle (which we filter down to valid paths).
4. To make sure we only move from position `i` to position `i+1` from layer to layer, we "zip" against our path from position `i+1` to the end.
5. `if` can be used in a postfix form to save space. In this case, we only want to take a path if it is valid (as defined above).

## Final Thoughts

I had a lot of fun with this week's challenges, especially challenge 1! Let me know if you think of a shorter solution. Otherwise, see y'all next week!