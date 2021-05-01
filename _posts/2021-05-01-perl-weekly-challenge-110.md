---
title: "Perl Weekly Challenge 110"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

A couple IO-related challenges this week with nice functional solutions. 🙂

## Task 1: Valid Phone Numbers

You are given a text file.

Write a script to display all valid phone numbers in the given text file.

### Acceptable Phone Number Formats

```
+nn  nnnnnnnnnn
(nn) nnnnnnnnnn
nnnn nnnnnnnnnn
```

### Input File

```
0044 1148820341
 +44 1148820341
  44-11-4882-0341
(44) 1148820341
  00 1148820341
```

### Output

```
0044 1148820341
 +44 1148820341
(44) 1148820341
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-110/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Str $file-path) returns Str {
  $file-path
    .IO
    .lines
    .grep(* ~~ /                                         # [1]
      ^                                                  # [2]
      <space>*                                           # [3]
      [\+<digit> ** 2 | \(<digit> ** 2\) | <digit> ** 4] # [4]
      <space>                                            # [5]
      <digit> ** 10                                      # [6]
      $                                                  # [7]
    /)
    .join("\n");
}

sub MAIN(Str $file-path) {
  say challenge($file-path);
}
```

This program runs as such:

```
$ raku ch-1.raku test.txt
0044 1148820341
 +44 1148820341
(44) 1148820341
```

### Explanation

The basics here are pretty simple -- for each line in the file, check if it matches our regex. If so, keep it, otherwise, drop it. Finally, join all matching lines together using the newline character. See below for comments on the regex itself.

#### Specific comments

1. Spaces in regexes in Raku are insignificant unless we put the [`:s` modifier](https://docs.raku.org/language/regexes#Sigspace) (or "ratchet") in front of the opening forward slash. This allows us to break the logic up over multiple lines and even add comments.
2. Match the beginning of the line; this is a universal regex metacharacter.
3. Match zero or more spaces. The example file had different levels of space at the beginning of each line, but all of it was insignificant.
4. This line matches what I will call our "prefix." It will match exactly one of the following:
  - A literal `+` character follow by two digits.
  - A literal `(` character followed by two digits followed by a literal `)` character.
  - Four digits in a row.
5. Each valid phone number had a space between the prefix and the last 10 digits, so this matches a literal space.
6. All valid phone numbers end in exactly 10 numbers
7. Match the end of the line to verify there is nothing else in the matching line.
  
## Task 2: Transpose File

You are given a text file.

Write a script to transpose the contents of the given file.

### Input File

```
name,age,sex
Mohammad,45,m
Joe,20,m
Julie,35,f
Cristina,10,f
```

### Output

```
name,Mohammad,Joe,Julie,Cristina
age,45,20,35,10
sex,m,m,f,f
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-110/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
use Text::CSV; # Imports `csv` function

sub challenge(Str $file-path) returns Str {
  my @lines = csv(in => $file-path, headers => "auto"); # [1] 
  my $names = ('name', |@lines.map(*<name>)).join(','); # [2]
  my $ages  = ('age', |@lines.map(*<age>)).join(',');
  my $sexes = ('sex', |@lines.map(*<sex>)).join(',');
  ($names, $ages, $sexes).join("\n");                   # [3]
}

sub MAIN(Str $file-path) {
  say challenge($file-path);
}
```

This program runs as such:

```
$ raku ch-2.raku test.csv
name,Mohammad,Joe,Julie,Cristina
age,45,20,35,10
sex,m,m,f,f
```

### Explanation

The bulk of the hard work is done for us by using the `Text::CSV` module. It allows us to pull the file into a list of hashes, and then do the logical work on that list. See below for how we apply the logic.

#### Specific Comments

1. `csv` with the `headers` option allows us to pull the CSV file into a list of hashes that looks like this:

    ```
    [
      {age => 45, name => Mohammad, sex => m}
      {age => 20, name => Joe, sex => m}
      {age => 35, name => Julie, sex => f}
      {age => 10, name => Cristina, sex => f}
    ]
    ```
2. Once we have the list of hashes above, we need three individual strings (one for `name`, `age`, and `sex` respectively). To do this, we just need to extract the respective key for each item in the list; we can do this via a [`map`](https://docs.raku.org/routine/map) function. Additionally, we prepend the respective key using the `("key", |@list)` syntax. For `name`, this is what the output list looks like: `(name Mohammad Joe Julie Cristina)`. Finally, we join the output list using commas.
3. Once we have the 3 key lists, we simply have to join them using the newline character as shown in the example output.

## Final Thoughts

I am going through an exercise at my day job where I refactor code from a more imperative approach to a more functional approach. Functional programming should not be used for everything, but when we can use it, it often allows for much more readable and predictable code.
