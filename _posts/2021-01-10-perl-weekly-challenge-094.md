---
title: "Perl Weekly Challenge 94"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

The second challenge was a lot like last weeks second challenge, so I went a step further and implemented multiple tree traversals. I won't include the tests this week, but feel free to click the GitHub links to see the test cases.

## Task 1: Group Anagrams

You are given an array of strings `@S`.

Write a script to group `Anagrams` together in any random order.

> An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

### Example 1

```
 Input: ("opt", "bat", "saw", "tab", "pot", "top", "was")
Output: [ ("bat", "tab"),
          ("saw", "was"),
          ("top", "pot", "opt") ]
```

### Example 2

```
 Input: ("x")
Output: [ ("x") ]
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-094/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(@S) {
    my $output = Set.new;
    for @S -> $word {
        my @permutations = $word.comb.permutations.map(*.join); # [1]
        $output ∪= (@S ∩ @permutations).keys.sort.join(',');    # [2]
    }
    $output.keys.map(*.split(',')).sort
}
sub MAIN(*@S where all(@S) ~~ /^<alpha>+$/) { # [3]
    say challenge(@S);
}
```

This program runs as such:

```
$ raku ch-1.raku opt bat saw tab pot top was
((bat tab) (opt pot top) (saw was))
```

### Explanation

This solution utilizes a cool Raku subroutine called `permutations`, which finds all the permutations of a given list. It only works for list smaller than 20 elements, so that is a caveat here. The logic is as follows:

1. For each inout word, find all the permutations.
2. Find the _union_ of the input words with the permutations of our current word to find permutations in the input list.
3. Add the above union to a set, so we don't store duplicates.
4. Return the set as a list of lists in alphabetical order (the problem says random order, but I alphabetized for determinism in my tests).

#### Specific Comments
 
1. `permutations` only works on a list, so we have to cast our word to a list via `comb`, then back to a string via `join`.
2. Sets only work on scalars, so since we have a _list_ of words, we have to join it into a string separated by a comma.
3. The challenge doesn't say to only accept letters, but I felt it was implied.
  
## Task 2: Binary Tree to Linked List

You are given a binary tree.

Write a script to represent the given binary tree as an object and flatten it to a linked list object. Finally, print the linked list object.

### Example

```
Input:

    1
   / \
  2   3
 / \
4   5
   / \
  6   7

Output:

1 -> 2 -> 4 -> 5 -> 6 -> 7 -> 3
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-094/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
subset NodeValue of Str where { $_ ~~ /^<digit>$/ || $_ eq 'Nil' }

class Node {
    has Node $.left  is rw = Nil;
    has Node $.right is rw = Nil;
    has Int $.value        = 0;
}

enum Traversal <Preorder Inorder Postorder>;

sub build-tree(@array, $root is copy = Nil, Int $i = 0) {
    if $i < @array.elems && @array[$i] ne 'Nil' {
        $root       = Node.new(value => @array[$i].Int);
        $root.left  = build-tree(@array, $root.left, 2 * $i + 1);
        $root.right = build-tree(@array, $root.right, 2 * $i + 2);
    }
    $root;
}

sub challenge(Node $root, Traversal $traversal) {
    with $root {
        given $traversal {
            when Preorder  { ($root.value, |challenge($root.left, $traversal), |challenge($root.right, $traversal)) }
            when Inorder   { (|challenge($root.left, $traversal), $root.value, |challenge($root.right, $traversal)) }
            when Postorder { (|challenge($root.left, $traversal), |challenge($root.right, $traversal), $root.value) }
        }
    }
}

sub challenge-wrapper(Node $root, Traversal $traversal = Preorder) {
    challenge($root, $traversal).join(' -> ');
}

sub MAIN(Str :$traversal = 'preorder', *@N where all(@N) ~~ NodeValue) {
    my $root = build-tree(@N);
    given $traversal.lc {
        when 'preorder'  { say challenge-wrapper($root, Preorder) }
        when 'inorder'   { say challenge-wrapper($root, Inorder) }
        when 'postorder' { say challenge-wrapper($root, Postorder) }
        default          { die "Traversal must be one of: (preorder, inorder, postorder), not $traversal" }
    }
}
```

This program runs as such:

```
$ raku ch-2.raku 1 2 3 4 5 Nil Nil Nil Nil 6 7
1 -> 2 -> 4 -> 5 -> 6 -> 7 -> 3

# Same as above with traversal explicitly stated
$ raku ch-2.raku --traversal=preorder 1 2 3 4 5 Nil Nil Nil Nil 6 7
1 -> 2 -> 4 -> 5 -> 6 -> 7 -> 3

$ raku ch-2.raku --traversal=inorder 1 2 3 4 5 Nil Nil Nil Nil 6 7
4 -> 2 -> 6 -> 5 -> 7 -> 1 -> 3

$ raku ch-2.raku --traversal=postorder 1 2 3 4 5 Nil Nil Nil Nil 6 7
4 -> 6 -> 7 -> 5 -> 2 -> 3 -> 1
```

### Explanation

The bulk of this code is the same as [last week's](https://aaronreidsmith.github.io/blog/perl-weekly-challenge-093/#solution-1), with the overlapping code being used to build a tree from command line arguments. Since the challenge code itself is only a line or two, I added the ability to pick which type of [tree traversal](https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/) you want (with the default being `preorder`, as shown in the example).

Basically, we just have a subroutine that takes a `Node`, and depending on what traversal type is chosen, will build up an array like one of the following (where `Left` and `Right` can themselves be a tree and will be expanded recursively):

```
Preorder  -> (Root, Left, Right)
Inorder   -> (Left, Root, Right)
Postorder -> (Left, Right, Root)
```

We then have a simple wrapper to "stringify" the list with arrows between the elements.

## Final Thoughts

Hoping for something a little less copy/paste next week, but regardless, this was a fun start to the new year!