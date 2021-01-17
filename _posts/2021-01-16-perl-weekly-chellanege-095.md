---
title: "Perl Weekly Challenge 95"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

Two pretty simple challenges this week! I tried ot focus on strongly typed subroutines and methods to shake things up.

## Task 1: Palindrome Number

You are given a number `$N`.

Write a script to figure out if the given number is a palindrome. Print `1` if true otherwise `0`.

### Example 1

```
Input: 1221
Output: 1
```

### Example 2

```
Input: -101
Output: 0 (since -101 and 101- are not the same)
```

### Example 3

```
Input: 90
Output: 0
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-095/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Int $N) {
    ($N.Str.flip eq $N.Str).Int; # [1]
}

sub MAIN(Int $N) {
    say challenge($N);
}
```

This program runs as such:

```
$ raku ch-1.raku 1221
1
```

### Explanation

Pretty simple solution here. THe `challenge` subroutine takes the input, casts it to a string, reverses it and compares it to the input argument (returning a boolean). Finally, it casts that boolean to a number to match the challenges output.

#### Specific Comments
 
1. Casting to a string allows us to account for any negative sign easily.
  
## Task 2: Demo Stack

Write a script to demonstrate stack operations like below:

- `push($n)` - add `$n` to the stack
- `pop()` - remove the top element
- `top()` - get the top element
- `min()` - return the minimum element

### Example

Note: This is shown with Perl 5 syntax.

```
my $stack = Stack->new;
$stack->push(2);
$stack->push(-1);
$stack->push(0);
$stack->pop;       # removes 0
print $stack->top; # prints -1
$stack->push(0);
print $stack->min; # prints -1
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-095/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
class Stack {
    has @!internal-state of Int;

    method push(Int $elem --> True) {
        @!internal-state.push($elem);
    }

    method pop() returns Int {
        if @!internal-state.elems == 0 {
            warn "Cannot pop an empty stack!";
        } else {
            @!internal-state.pop;
        }
    }

    method top returns Int {
        if @!internal-state.elems == 0 {
            warn "Cannot find top of empty stack!";
        } else {
            @!internal-state.tail;
        }
    }

    method min returns Int {
        if @!internal-state.elems == 0 {
            warn "Cannot find minimum of empty stack!";
        } else {
            @!internal-state.min;
        }
    }

    method Str returns Str {
        "({@!internal-state.join(', ')}) <-- Top";
    }
}

sub MAIN(*@push where all(@push) ~~ Int, Int :$pop = 2) {
     # Can't put a default on "slurpy" args, so this is our work around
    @push = @push.elems > 0 ?? @push !! (1, 2, 3, 4);

    my $stack = Stack.new;
    for @push -> $elem {
        $stack.push($elem);
    }
    say "     Stack after pushing: $stack";
    for ^$pop {
        $stack.pop();
    }
    say "     Stack after popping: $stack";
    say "    Top element of stack: {$stack.top}";
    say "Minimum element of stack: {$stack.min}";
}
```

This program runs as such:

```
# All default
$ raku ch-2.raku 
     Stack after pushing: (1, 2, 3, 4) <-- Top
     Stack after popping: (1, 2) <-- Top
    Top element of stack: 2
Minimum element of stack: 1

# Override pop default
$ raku ch-2.raku --pop=1
     Stack after pushing: (1, 2, 3, 4) <-- Top
     Stack after popping: (1, 2, 3) <-- Top
    Top element of stack: 3
Minimum element of stack: 1

# Override pop and push defaults
$ raku ch-2.raku --pop=1 1 2 3
     Stack after pushing: (1, 2, 3) <-- Top
     Stack after popping: (1, 2) <-- Top
    Top element of stack: 2
Minimum element of stack: 1
```

### Explanation

A stack is a last in, first out (LIFO) structure, where we can only interact with the top. You can think of it like a stack of plates; it's not easy to grab the middle plate from the stack!

In this case, we decided to make the stack homogenous (i.e., it can only hold integers). A Raku `List` already has a stack-like interface, so we basically just wrap that and add some warnings.

We simply define a class with a private `Array` of integers such that the user can only interact with it via the methods described in the challenge. Then, the `MAIN` subroutine simply demos those methods.

#### Specific Comments

1. Raku classes have something called [twigils](https://docs.raku.org/language/variables#Twigils). The `!` twigil here indicates that this variable is private to the class, and cannot be seen by any outside callers.
2. This could also be written as `has Int @!internal-state`, but I feel that doesn't read as well. It can be written like this since the `@` sigil already denotes it is a positional variable, so you only need to constrain the members.
3. This is a [common pattern](https://docs.raku.org/routine/say#(Independent_routines)_sub_say) for methods and subroutines that don't actually return anything. Similar to `Unit` in Scala, `void` in Java, or `None` in Python. And of course `-->` is the way we define the return type.
4. The returns type can _also_ be defined using `returns <type>` as shown here. The difference between `-->` and `returns` is that `returns` can only specify abstract types, whereas `-->` can specify both abstract type or specific values, which is why we needed to use `-->` to return the _specific value_ `True`.
5. You'll notice we don't add the empty parentheses here. They are optional if there are no arguments to the method. In this case, I am using the Scala convention of having parentheses if the method has [side effects](https://en.wikipedia.org/wiki/Side_effect_(computer_science)), and leaving them off otherwise.
6. `Str` is a magic method, similar to `__str__` in Python or `toString` in Java and Scala. It is called whenever this variable is coerced to a string. So we don't have to say `"Stack: {$stack.Str}"`, we can just say `"Stack: $stack"`.

## Final Thoughts

Strongly typed Raku is much faster than gradually typed Raku, but I find it to be more cumbersome. Scalars are fairly easy (which is the majority of what we dealt with here), but I find positional (`Lists`, `Arrays`, etc.) and associatives (`Hashes`, `Maps`, etc.) to be more challenging. For example, the way you constrain a `List` and an `Array` is _slightly_ different. And `Maps` _always_ have to have string keys, which makes things both cumbersome and slow. In fact, there was some interesting discussion around Raku's speed (or lack thereof) on the [Raku subreddit](https://www.reddit.com/r/rakulang/comments/kxjsca/raku_is_friggin_slow/), and I encourage anyone reading this to spend a little time over there. Anyway, that's enough rambling from me. Until next time!