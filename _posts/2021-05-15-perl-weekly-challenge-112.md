---
title: "Perl Weekly Challenge 112"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

A little string manipulation and recursion today. My solution to task 2 is _almost_ the same as my solution to [Advent of Code 2020: Day 10 (part 2)](https://aaronreidsmith.github.io/blog/advent-of-code-day-10/)!

## Task 1: Canonical Path

You are given a string path, starting with a slash ‘/'.

Write a script to convert the given absolute path to the simplified canonical path.

In a Unix-style file system:

```
- A period '.' refers to the current directory
- A double period '..' refers to the directory up a level
- Multiple consecutive slashes ('//') are treated as a single slash '/'
```

The canonical path format:

```
- The path starts with a single slash '/'.
- Any two directories are separated by a single slash '/'.
- The path does not end with a trailing '/'.
- The path only contains the directories on the path from the root directory to the target file or directory
```

### Example

```
Input: "/a/"
Output: "/a"

Input: "/a/b//c/"
Output: "/a/b/c"

Input: "/a/b/c/../.."
Output: "/a"
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-112/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Str $path is copy) returns Str {                  # [1]
  die "Must be an absolute path" unless $path.starts-with('/'); # [2]
  
  $path = $path.substr(1);                              # [3]
  $path = $path.subst(/\/ ** 2..*/, '/', :global);      # [4][5]
  $path = $path.substr(0, *-1) if $path.ends-with('/'); # [6]

  my @output;
  for $path.split('/') -> $dir {
    given $dir {
      when '.' { Nil }                            # [7]
      when '..' {
        die "Illegal path" if @output.elems == 0;
        @output.pop;
      }
      default { @output.push($dir) }
    }
  }
  '/' ~ @output.join('/')
}

sub MAIN(Str $path) {
  say challenge($path);
}
```

This program runs as such:

```
$ raku ch-1.raku /a/b//c
/a/b/c
```

### Explanation

We basically just follow the following steps:

1. Does the path start with a slash?
  - If yes, remove it and continue.
  - If not, `die`, since the problem indicates we are given a path starting with a slash.
2. Replace any duplicate slashes with a single slash.
3. Remove the trailing slash if it exists.
4. We should now have something that looks like `a/b/c` and we split it into a list that looks like `(a, b, c)`.
5. Iterate through the above list and take one of three actions depending on what item we encounter:
   - If we hit `.`, it is just redundant and we can continue.
   - If we hit `..`, we need to remove the most recent item from `@output`. As a caveat, if `@output` is empty and we encounter `..`, it will throw an error.
   - If we hit anything else (i.e., a normal directory), we can just add it to the end of `@output`.
6. Finally, we just join `@output` into a path using slashes, and prepend a slash onto it to make it an absolute path.

#### Specific comments

1. Since we are mutating `$path` within the subroutine, we need to declare it as `is copy`.
2. The question says our input must start with a slash. So we die `unless` it has the correct input.
3. If we reach this line, that means the `$path` _does_ start with a slash, and we need to remove it using `substr`.
4. We want to replace any instance where there are two or more slashes in a row. That is what this regex means `/\/ ** 2..*/`; `\/` means "literal slash" and `2..*` means "two or more times." We replace all of these instances with a single slash, and we want to do it for the whole string, hence `:global`.
5. As an aside, I hate that `substr` (substring) and `subst` (substitute) are so close in spelling. I feel the former should be named `slice` and the latter `replace`.
6. If our path ends with a slash, we want to remove it so that when we `split` we don't get an empty entry.
7. Don't really know if `Nil` is the right thing to do here. In Scala, it would just be `case "." =>` with nothing on the right-hand side of the arrow. I figured an empty block or `Nil` is safe since we don't want this case to fall into `default`.
  
## Task 2: Climb Stairs

You are given `$n` steps to climb

Write a script to find out the distinct ways to climb to the top. You are allowed to climb either 1 or 2 steps at a time.

### Example

```
Input: $n = 3
Output: 3

    Option 1: 1 step + 1 step + 1 step
    Option 2: 1 step + 2 steps
    Option 3: 2 steps + 1 step

Input: $n = 4
Output: 5

    Option 1: 1 step + 1 step + 1 step + 1 step
    Option 2: 1 step + 1 step + 2 steps
    Option 3: 2 steps + 1 step + 1 step
    Option 4: 1 step + 2 steps + 1 step
    Option 5: 2 steps + 2 steps
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-112/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
use experimental :cached; # [1]

sub challenge(
  $max where Int,
  @paths where Positional = (^$max), # [2][3]
  $current-step where Int = 0
) is cached {
  given $current-step {
    when * == $max { 1 }
    when * > $max  { 0 }
    default {
      challenge($max, @paths, $current-step + 1) +
      challenge($max, @paths, $current-step + 2)
    }
  }
}

sub MAIN(Int $n) {
  say challenge($n);
}
```

This program runs as such:

```
$ raku ch-2.raku 4
5
```

### Explanation

This one is actually pretty straight forward, even if it doesn't seem as such. Basically, `challenge` will construct a list from `0..^$n`; so for `$n = 3` we would get `(0, 1, 2)`. Starting at step `0` we check 2 conditions:

1. Are we at the top of the steps? If so, stop and mark this path as valid (`1`).
2. Are we _above_ the top of the steps? If so, stop and mark this path as _invalid_ (`0`).

If we don't match either of the above conditions, we try _both_ a step size of `1` and `2` recursively. So essentially this is a brute force approach, but it is efficient because we have memoized our subroutine using the `is cached` trait. This means that once it has done the computation for `challenge(3, (0, 1, 2), 2)`, the next time it sees that same input, it will always return the same result. Since a step size of `1` and `2` will have some overlap in individual steps, this makes this approach incredibly efficient.

Since the end conditions only return `0` or `1`, the `default` block actually handles summing the valid paths.

#### Specific Comments

1. `is cached` is an experimental feature and needs to be explicitly imported.
2. Normally you see me write `Int $foo` instead of `$foo where Int`. This fails for positionals and hashes; `Int @foo` indicates a _positional of ints_ (since the `@` sigil already indicates it is a positional). So why didn't I just do that? I tried. It fails with `expected Positional[Int] but got Range (^10)`, which I think is stupid. So this is a way to _kind of_ strongly-type it; better than nothing I guess.
3. I think it is cool that I can use `$max` in the default of `@paths` here!

## Final Thoughts

Pretty easy this week, but that is mostly because I was able to copy an older solution of mine for task two. Should I have done something new/different? Probably, but oh well. See y'all next week!
