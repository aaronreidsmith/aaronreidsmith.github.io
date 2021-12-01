---
title: "Advent of Code: Year 2020, Day 18"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

I like to hate on Raku quite a bit, but it was literally the _perfect_ language for today's challenge. I guess the love-hate relationship continues!

## The Problem

### Part 1

While we're sitting on our flight, the kid next to us asks if we can help with his math homework. Unfortunately, the rules of this math are different from what we are familiar with -- parentheses have the same precedence, but everything else is evaluated from left to right (_suck it_, PEMDAS). Here is an example:

```
1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71
```

Luckily it seems like all of his math problems are only addition and multiplication. After evaluating all the expressions, what is the sum of their outputs?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-18.raku)

See below for explanation and any implementation-specific comments.

```
use MONKEY-SEE-NO-EVAL; # [1]

sub infix:<plus>(Int:D $a, Int:D $b) returns Int:D is equiv(&infix:<*>) { $a + $b } # [2][3]

sub MAIN($file, Bool :$p2 = False) {
   my @expressions = $file.IO.lines.map(*.trans(['+'] => ['plus'])); # [4]
   say @expressions.map(-> $expr { EVAL $expr }).sum;                # [5]
}   
```

This runs as such:

```
$ raku day-18.raku input.txt
45840336521334
```

#### Explanation

Basically what do here is define a new [_infix operator_](https://docs.raku.org/language/operators#index-entry-infix_operator), `plus`. Infix means it goes between arguments, so it takes 2 integers and is written like this: `$a plus $b`. We also define it with equivalent precedence to the existing multiplication operator, so the expressions will be evaluated left-to-right.

After we have done that, we read all the lines in and translate `+` to `plus` for each one. Finally, we evaluate each expression using `EVAL` and sum the results!

##### Specific Comments

1. `EVAL` is a _very_ unsafe function and should only be used with caution. What it does is takes any valid string and attempts to evaluate it as Raku code. As you can imagine, this can be dangerous, so we have to manually allow the function using the [`MONKEY-SEE-NO-EVAL` pragma](https://docs.raku.org/language/pragmas#index-entry-MONKEY-SEE-NO-EVAL__pragma).
2. When defining this function, we don't explicitly have to say what types it takes, but it does speed up calculating quite a bit. In this case we say it takes two `Int:D` variables, meaning each one is a _specific_ integer and not an uninitialized `Int` object. Likewise, it returns an `Int:D` object.
3. We are able to set the function's [precedence](https://docs.raku.org/language/functions#Precedence) in regard to other functions. The options are `is looser`, `is equiv`, and `is tighter`. In this case, we set the new `plus` operator to have the same precedence as multiplication.
4. `trans` translates substrings from `a` to `b`. By default, the input length has to match the output length. This means substituting `+` with `plus` would only replace the `+` with `p`. To get around that we are able to use the brackets to say "substitute the _entire_ string."
5. After the substitution, we will end up with a string that looks like this (using the example from above): `1 plus 2 * 3 plus 4 * 5 plus 6`. Since we have defined this as valid Raku code, we can safely call `EVAL` on it, which returns an integer for us to sum up later.

### Part 2

After finishing up part one, we reach the _advanced math_ section. In this section addition now has _greater_ precedence than multiplication. Using the same input, what is the sum of the output numbers using advanced math?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-18.raku)

See below for explanation and any implementation-specific comments.

```
use MONKEY-SEE-NO-EVAL;

sub infix:<plus>(Int:D $a, Int:D $b) returns Int:D is equiv(&infix:<*>)  { $a + $b }
sub infix:<mult>(Int:D $a, Int:D $b) returns Int:D is looser(&infix:<+>) { $a * $b }

sub MAIN($file, Bool :$p2 = False) {
   my @expressions = $file.IO.lines.map($p2 ?? *.trans(['*'] => ['mult']) !! *.trans(['+'] => ['plus'])); # [1]
   say @expressions.map(-> $expr { EVAL $expr }).sum
}
```

This runs as such:

```
$ raku day-18.raku input.txt
45840336521334

$ raku day-18.raku --p2 input.txt
328920644404583
```

#### Explanation

Again, all we have to do is define a new infix operator with precedence _looser_ than regular addition. If the user sends the `$p2` flag, we substitute `*` with `mult`, otherwise we substitute `+` with `*`. Regardless, we still `EVAL` all expressions and sum the output.

##### Specific Comments

1. This is where the `Whatever` star gets ugly. On this line we use `*` to mean both `Whatever` _and_ a literal `*` character to translate in our string.

## Final Thoughts

You can define infix operators in other languages (for example, operators in Scala are just functions, so you would just write `def plus`), however Scala does not let you [define the precedence](https://docs.scala-lang.org/tour/operators.html). That is what is so special about Raku and what makes this solution so sleek for what could be a very tough problem.
