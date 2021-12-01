---
title: "Perl Weekly Challenge 112"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

Task 1 allowed for some functional programming using some cool built-ins in Raku. Task 2 built on some code I wrote for [Challenge 94](https://aaronreidsmith.github.io/blog/perl-weekly-challenge-094/#task-2-binary-tree-to-linked-list).

## Task 1: Represent Integer

You are given a positive integer `$N` and a digit `$D`.

Write a script to check if `$N` can be represented as a sum of positive integers having `$D` at least once. If check passes print 1 otherwise 0.

### Example

```
Input: $N = 25, $D = 7
Output: 0 as there are 2 numbers between 1 and 25 having the digit 7 i.e. 7 and 17. If we add up both we don't get 25.

Input: $N = 24, $D = 7
Output: 1
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-113/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
subset PositiveInt of Int where * > 0; # [1]

sub challenge(PositiveInt $N, PositiveInt $D) returns Int {
  my $output = (1..^$N)   # [2]
    .race                 # [3]
    .grep(*.contains($D)) # [4]
    .combinations(2..*)   # [5]
    .map(*.sum)           # [6]
    .any == $N;           # [7]
  $output.Bool.Int;       # [8]
}

sub MAIN(PositiveInt $N, PositiveInt $D) {
  say challenge($N, $D);
}
```

This program runs as such:

```
$ raku ch-1.raku 24 7
1
```

### Explanation

This function first generates a list of integers from 0 to `$N - 1` (no need to include 0 or `$N` itself, since 0 is not positive and. we want things that add up to `$N`). It then filters those down to only numbers that contain `$D`. It then finds all combinations of size 2 or larger to evaluate, and finds the sum of those combinations. Finally, it simply checks if any of the sums add up to `$N`. I like that we can easily just chain these methods together; makes it very easy to read.

#### Specific comments

1. The question says we should only allow positive integers. To do this, we can easily create a `subset` of `Int` and add a condition using `where` (in this case `where * > 0`).  
2. As mentioned above, no need to include `1` or `$N`, so we filter them using the `..^` range creator. It includes the bottom number and excludes the top number.
3. We don't need this list in any order, since we will end up with a boolean (and eventually integer) at the end. So we want to perform all of our actions as quickly as possible, and we don't care about order. [`race`](https://docs.raku.org/routine/race) creates a [RaceSeq](https://docs.raku.org/type/RaceSeq), which allows us to process a list in parallel without regards to order.
4. We filter (`grep`) down to numbers that contains `$D`. `contains` coerces the left-hand argument to a String, so this is the same as `*.Str.contains($d)`. This is actually a documented [trap](https://docs.raku.org/language/traps#Lists_become_strings,_so_beware_.contains()) that I [fell into](https://aaronreidsmith.github.io/blog/advent-of-code-year-2020-day-04/) during Advent of Code, but it works in my favor this time.
5. We want to examine all combinations of size 2 or larger, which can easily be created using the `2..*` syntax.
6. Once we have all the combinations, it is a simple matter to find their sums by mapping over each combination (and using the built-in `sum` method).
7. Once we have a list of sums, we want to see if _any_ equal `$N`. So we just call `.any` on the list and get our answer!
8. `any` returns a [Junction](https://docs.raku.org/routine/any), so we have to coerce it to a boolean, and then an integer to get the output that the challenge expects.
  
## Task 2: Recreate Binary Tree

You are given a Binary Tree.

Write a script to replace each node of the tree with the sum of all the remaining nodes.

### Example

#### Input Binary Tree

```
        1
       / \
      2   3
     /   / \
    4   5   6
     \
      7
```

#### Output Binary Tree

```
        27
       /  \
      26  25
     /   /  \
    24  23  22
     \
     21
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-113/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
subset NodeValue of Str where { $_ ~~ /^<digit>$/ || $_ eq 'Nil' }

class Node {
  has Node $.left  is rw = Nil;
  has Node $.right is rw = Nil;
  has Int  $.value is rw = 0;
}

# Adapted from https://rosettacode.org/wiki/Visualize_a_tree#Raku
sub format-tree(
  Node $root,
  Str :$indent = '',
  :@mid = ('├─', '│ '),
  :@end = ('└─', '  ')
) returns Str {
  sub visit(Node $node, *@pre) {
    with $node {
      |gather {
        take @pre[0] ~ $node.value;
        my @children = ($node.right, $node.left).grep(*.defined);
        my $end = @children.end;
        for @children.kv -> $_, $child {
          when $end { take visit($child, (@pre[1] X~ @end)) }
          default   { take visit($child, (@pre[1] X~ @mid)) }
        }
      }
    }
  }
  visit($root, $indent xx 2).join("\n");
}

sub build-tree(@array, $root is copy = Nil, Int $i = 0) returns Node {
  if $i < @array.elems && @array[$i] ne 'Nil' {
    $root       = Node.new(value => @array[$i].Int);
    $root.left  = build-tree(@array, $root.left, 2 * $i + 1);
    $root.right = build-tree(@array, $root.right, 2 * $i + 2);
  }
  $root;
}

sub challenge(Node $root is copy, @values = ()) returns Node {
  sub extract-values(Node $root) returns Positional {                           # [1]
    with $root {                                                                # [2]
      ($root.value, |extract-values($root.left), |extract-values($root.right)); # [3]
    }
  }

  with $root {
    my @node-values = @values.elems > 0 ?? @values !! extract-values($root); # [4]
    $root.value = @node-values.grep(* != $root.value).sum;                   # [5]
    challenge($root.left, @node-values);                                     # [6]
    challenge($root.right, @node-values);
  }
  $root;
}

sub MAIN(*@nodes where all(@nodes) ~~ NodeValue) {
  my $root = build-tree(@nodes);
  say format-tree(challenge($root));
}
```

This program runs as such:

```
$ raku ch-2.raku 1 2 3 4 Nil 5 6 Nil 7 Nil Nil
27
├─25
│ ├─22
│ └─23
└─26
  └─24
    └─21
```

### Explanation

I will only be discussing the `challenge` subroutine, as `build-tree` was written in my Challenge 94 blog, along with the `NodeValue` subset and the `Node` class. Additionally, I couldn't find a good way to actually print this tree out, so I copied `format-tree` from [Rosetta Code](https://rosettacode.org/wiki/Visualize_a_tree#Raku); it has some issues (the 24 is not obvious that it is the left branch), but it works overall.

As for the actual _new_ code that I wrote, given a tree, we simply need to traverse it once to find the values (storing it in `@node-values`). Then, traverse it a second time and changing the values at each node to the sum of `@node-values` excluding the current value. So for the root node, it would be `@node-values.grep(* != 1).sum`. Once we have done that, since we changed the tree in place, we can just return the root.

#### Specific Comments

1. This is defined within `challenge` because it is not really needed outside of it. Additionally, this logic can't be included as part of the main flow of `challenge` since we use a copy of `$root`. Since we traverse recursively, our list of values would be different on each recursive call.
2. This `with` guard prevents us from trying to run the logic/recurse even more if `$root` is `Nil`.
3. This is a simple prefix traversal (where we visit the current node, then left, then right). Since we have the `with` guard, this will prevent `Nil` values. So for the example input we would end up with this list: `(1, 2, 3, 4, 5, 6, 7)`.
4. We only want to call `extract-values` on the first call (since the tree is constantly changing), so we only run it if `@values` is empty (and then pass in `@node-values` on subsequent calls).
5. Like I showed above, we just need to sum all the values are not `$root.value`. Another way to do this would have been `@node-values.sum - $root.value`, which honestly might have been faster since it doesn't require traversing twice. Oh well!
6. These recursive calls will _technically_ return their `$root`, but since they aren't assigned to anything, they are just ignored.

## Final Thoughts

The hardest part of this week's challenge was honestly trying to find a way to print a binary tree! I tried translating some algorithms from other languages, and eventually settled on the one I used. Let me know if there are any good ones out there!
