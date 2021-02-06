---
title: "Perl Weekly Challenge 98"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

This week's solutions explore some more obscure parts of the Raku ecosystem, namely [state variables](https://docs.raku.org/syntax/state) and [adverbs](https://docs.raku.org/language/glossary#index-entry-Adverb).

## Task 1: Read N-characters

You are given file `$FILE`.

Create subroutine `readN($FILE, $number)` that returns the first n-characters and moves the pointer to the `(n+1)th` character.

### Example

```
Input: Suppose the file (input.txt) contains "1234567890"
Output:
    print readN("input.txt", 4); # returns "1234"
    print readN("input.txt", 4); # returns "5678"
    print readN("input.txt", 4); # returns "90"
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-098/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub readN(Str $file-name, Int $chars-to-read where $chars-to-read > 0) returns Str {
    state %file-map;                                          # [1]

    if %file-map{$file-name}:!exists {                        # [2]
        %file-map{$file-name} = IO::CatHandle.new($file-name) # [3]
    }

    %file-map{$file-name}.readchars($chars-to-read);          # [4]
}

sub MAIN(Str $FILE, Int $N) {
    say readN($FILE, $N);
    say readN($FILE, $N);
    say readN($FILE, $N);
}
```

This program runs as such:

```
# Assuming input.txt contains '1234567890'
$ raku ch-1.raku input.txt 4
1234
5678
90
```

### Explanation

All of this relies on two very cool aspects of Raku: [state variables](https://docs.raku.org/syntax/state) and [`CatHandles`](https://docs.raku.org/type/IO::CatHandle), which I will detail below. Basically, we just create a new `CatHandle` and pass all the heavy lifting to it via `readchars`; it keeps track of where it is in the file and will not attempt to read past the end of the file. 

#### Specific comments

1. A state variable in Raku is similar to a static variable in other languages, with the additional caveat that it can be instantiated in subroutines in addition to classes. This variable will be instantiated once and shared across all invocations of the subroutine. So, if we wanted to, we could do the following:

```
# input1.txt
# maryalamb

# input2.txt
# hadlittle

sub MAIN {
  my $input1 = 'input1.txt';
  my $input2 = 'input2.txt';
  
  say readN($input1, 4);
  say readN($input2, 3);
  say readN($input1, 1);
  say readN($input2, 6);
  say readN($input1, 4);
}

# Output:
# mary
# had
# a
# little
# lamb
```

2. This is a special case of the [`exists`](https://docs.raku.org/type/Hash#:exists) adverb. Adverbs are just named arguments. In this case `:exists` is essentially the pair `exists => True`, so to negate it we use `!:exists`. I found this pretty interesting, because I thought it would have been `!%file-map{$file-name}:exists`, but Raku complains about that.
3. A [`CatHandle`](https://docs.raku.org/type/IO::CatHandle) is _normally_ used to `cat` together several file handles and read them all at once. In this case, we are using it to take advantage of its `readchars` function discussed below.
4. [`readchars`](https://docs.raku.org/type/IO::CatHandle#method_readchars) essentially just tracks our offset in the given handle and always outputs the next `n` characters that we request, and just returns an empty string if we are at the end of the file. Super convenient for this challenge!
  
## Task 2: Search Insert Position

You are given a sorted array of distinct integers `@N` and a target `$N`.

Write a script to return the index of the given target if found otherwise place the target in the sorted array and return the index.

### Example 1

```
Input: @N = (1, 2, 3, 4) and $N = 3
Output: 2 since the target 3 is in the array at the index 2.
```

### Example 2

```
Input: @N = (1, 3, 5, 7) and $N = 6
Output: 3 since the target 6 is missing and should be placed at the index 3.
```

### Example 3

```
Input: @N = (12, 14, 16, 18) and $N = 10
Output: 0 since the target 10 is missing and should be placed at the index 0.
```

### Example 4

```
Input: @N = (11, 13, 15, 17) and $N = 19
Output: 4 since the target 19 is missing and should be placed at the index 4.
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-098/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(@N is copy, Int $N) returns Int { # [1]
    my @new = $N ∉ @N ?? (|@N, $N).sort !! @N;  # [2]
    @new.first($N, :k);                         # [3]
}

sub MAIN(Int $N, *@N where all(@N) ~~ Int) {
    say challenge(@N, $N)
}
```

This program runs as such:

```
# $N followed by @N
$ raku ch-2.raku 3 1 2 3 4 
2
```

### Explanation

This is pretty straight forward; we check if `$N` is in `@N` (if not, we add it and re-sort), then return the index of `$N`. That's it!

#### Specific Comments

1. In Raku, the sigil (`$`, `@`, `%`, etc.) is _part of_ the variable declaration. Because of that, for better or for worse, it is not a problem (as far as the compiler is concerned) that we have to variables named `N`.
2. Rather than mark `@N` as `is copy` so we could use `@N.push($N).sort`, since we assign it to a new variable anyway (`@new`), we can use a [slip](https://docs.raku.org/type/Slip) to append `$N` to `@N`.
3. `first` returns the first instance of the argument in the list (in this case `$N`). We supply the [`:k` adverb](https://docs.raku.org/routine/first#class_List) to have it return the _index_ of `$N` rather than `$N` itself. 
 
## Final Thoughts

Raku has a lot of cool stuff built in to it. I find the hardest part of navigating this language is the documentation. Things are _mostly_ well documented, but things like Stack Overflow posts and how-tos can be few and far between. Hopefully this blog is helpful for anyone trying to learn the language!