---
title: "Perl Weekly Challenge 107"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

I wrote this week's answers several days ago, but forgot to commit them. I ended up getting a new laptop and had to rewrite them. I think they ended up the same, but I guess no one knows for sure!

## Task 1: Self-descriptive Numbers

Write a script to display the first three self-descriptive numbers. As per [wikipedia](https://en.wikipedia.org/wiki/Self-descriptive_number), the definition of "self-descriptive number" is:

>In mathematics, a self-descriptive number is an integer m that in a given base b is b digits long in which each digit d at position n (the most significant digit being at position 0, and the least significant at position b−1) counts how many instances of digit n are in m.

For example:

```
 1210 is a four-digit self-descriptive number:

    Position 0 has value 1 i.e. there is only one 0 in the number
    Position 1 has value 2 i.e. there are two 1 in the number
    Position 2 has value 1 i.e. there is only one 2 in the number
    Position 3 has value 0 i.e. there is no 3 in the number
```

Expected output:

```
1210, 2020, 21200
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-107/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Int $n) returns Str { # [1]
    my @output;
    for (^∞) -> $i {                # [2][3]
        my @digits = $i.comb;
        my $valid = True;
        for @digits.kv -> $index, $value {
            $valid = @digits.grep($index).elems == $value;
            last unless $valid;     # [4]
        }
        @output.push($i) if $valid; # [5]
        last if @output.elems == $n;
    }
    @output.join(', ');
}

sub MAIN(Int $n = 3) {
    say challenge($n);
}
```

This program runs as such:

```
$ raku ch-1.raku
1210, 2020, 21200
```

### Explanation

We begin by defining a list to hold our output, then kick of an infinite loop starting at 0. For each number, we convert it to a list of digits (`.comb`). For each index, value pair, we check if the input number has `$value` number of `$index` digits. So for 1210 we would check if it had 1 zero, 2 ones, 1 two, and 0 threes. If it meets the conditions, we add it to `@output`. Finally, if we have found all 3 that we are looking for, we break out of the infinite loop and return.

#### Specific comments

1. We make this generic by accepting the argument `$n`, but the fourth self-describing number is `3,211,000`, and the fifth is `42,101,000`, so this method would get slow very quickly.
2. We _could_ have said `loop` to start an infinite loop, but then we wouldn't have access to `$i`.
3. When using this method, we always have to use the carrot (`^`) to say we are not including infinity. This is because it is impossible to be inclusive of infinity.
4. `unless` is just the opposite of `if`. I feel this reads better than `last if !$valid`.
5. I find the post-fix way of using conditionals to read better a lot of the time in Raku, as seen here.
  
## Task 2: List Methods

Write a script to list methods of a package/class.

### Example

Class definition:

```
package Calc;

use strict;
use warnings;

sub new { bless {}, shift; }
sub add { }
sub mul { }
sub div { }

1;
```

Expected output:

```
BEGIN
mul
div
new
add
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-107/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
# Used for testing
class Calc {      # [1]
    method add {}
    method mul {}
    method div {}
}

sub challenge(Any $class) returns Str {     # [2]
    $class.^methods.map(*.gist).join("\n"); # [3][4]
}

sub MAIN {
    say challenge(Calc.new);
}
```

This program runs as such:

```
$ raku ch-2.raku
add
mul
div
BUILDALL
```

### Explanation

The example shows a class definition in Perl, but we are using Raku, so we can just define our class using the `class` keyword as shown. Additionally, we have a `BUILDALL` method instead of `BEGIN`.

Raku gives us the [`^methods`](https://docs.raku.org/language/classtut#Introspection) meta method to introspect an object's methods, so we just have to utilize that on the input object!

#### Specific Comments

1. In Perl, we have to define classes in their own file, but in Raku we can just use the `class` keyword.
2. All objects inherit from [`Any`](https://docs.raku.org/type/Any), so we are just saying we accept any class here.
3. Raku provides us a nice introspection method, `^methods`, which returns a list of defined methods and `BUILDALL`. We can also pass in the flag `:local` meaning "only show us methods defined in `Calc` and not super classes," or we could pass in `:all` meaning "show us all methods that can act on this class."
4. The returned type is `List[Method]`, so to cast everything to a string, we need to call each method's [`gist`](https://docs.raku.org/routine/gist) method.

## Final Thoughts

Once again, Raku makes these challenges super easy. Looking forward to something tougher in the future!
