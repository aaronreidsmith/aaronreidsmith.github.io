---
title: "Perl Weekly Challenge 103"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

Challenge two this week was... interesting, to say the least. But, we are through it, and it's the weekend! 🍻

## Task 1: Chinese Zodiac

You are given a year `$year`.

Write a script to determine the Chinese Zodiac for the given year `$year`. Please check out [wikipage](https://en.wikipedia.org/wiki/Chinese_zodiac) for more information about it.

The animal cycle: Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, Pig.  
The element cycle: Wood, Fire, Earth, Metal, Water.

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-103/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Int $year) returns Str {
    constant $root-year = 1924; # From Wikipedia

    my $difference         = $year - $root-year;
    my $element-difference = $difference < 0 ?? $difference + 10 !! $difference; # [1]
    my $animal-difference  = $difference < 0 ?? $difference + 12 !! $difference;

    my $element = do given $element-difference % 10 { # [2][3]
        when 0|1 { 'Wood'  }
        when 2|3 { 'Fire'  }
        when 4|5 { 'Earth' }
        when 6|7 { 'Metal' }
        when 8|9 { 'Water' }
    }
    my $animal = do given $animal-difference % 12 {
        when 0  { 'Rat'     }
        when 1  { 'Ox'      }
        when 2  { 'Tiger'   }
        when 3  { 'Rabbit'  }
        when 4  { 'Dragon'  }
        when 5  { 'Snake'   }
        when 6  { 'Horse'   }
        when 7  { 'Goat'    }
        when 8  { 'Monkey'  }
        when 9  { 'Rooster' }
        when 10 { 'Dog'     }
        when 11 { 'Pig'     }
    }

    "$element $animal"; # [4]
}

sub MAIN(Int $year) {
    say challenge($year);
}
```

This program runs as such:

```
$ raku ch-1.raku 2017
Fire Rooster
```

### Explanation

I'm sure there is a better root than 1924, but that is the first year in the table on the [Wikipedia page](https://en.wikipedia.org/wiki/Chinese_zodiac). Reading through the Wikipedia page, we can see two things:

1. The element cycle has 5 rotations (Wood, Fire, Earth, Metal, and Water), and each one lasts for 2 years (a Yin year and a Yang year [which we don't care about]).
2. The animal cycle has 12 rotations (Rat, Ox,  Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, Pig), and each one lasts for 1 year.

This makes our logic pretty simple -- we just need to find our distance from the known year of 1924 and find which cycle that year falls in. For element, we find the difference and then find the remainder after dividing by 10 (5 cycles x 2 years each). If it is 0 or 1, it is Wood, if it is 2 or 3 it is Fire, etc. Similarly, we find the difference and find the remainder after dividing by 12 for the animals. If it is 0 it is Rat, if it is 1 it is Ox, etc. That's it!

#### Specific comments

1. We can't just do `abs($year - $root-year)` because for years before `$root-year`, it would yield the wrong cycle (for example, 1923 would have a remainder of 1 for `$element` instead of `9`). Because of this, if the difference is negative, we need to add the size of the cycle (10 and 12, respectively) to put it in its correct place.
2. `given` is a flow control keyword and doesn't actually return anything. To make the `given` block return its value, we need to add the `do` keyword before it.
3. You'll notice there is no `default` block for these `given`s. That is intentional, since we know all the possible outcomes. Best practice would probably be something like `default { die "Unexpected input: $_" }`. 
4. Double quotes tell the Raku compiler to interpolate this string, so we get `"Fire Rooster"` instead of the literal `'$element $animal'`.
  
## Task 2: What’s playing?

**Note: This was copied directly from [perlweeklychallenge.org](https://perlweeklychallenge.org/blog/perl-weekly-challenge-103/#TASK2)**

Working from home, you decided that on occasion you wanted some background noise while working. You threw together a network streamer to continuously loop through the files and launched it in a tmux (or screen) session, giving it a directory tree of files to play. During the day, you connected an audio player to the stream, listening through the workday, closing it when done.

For weeks you connect to the stream daily, slowly noticing a gradual drift of the media. After several weeks, you take vacation. When you return, you are pleasantly surprised to find the streamer still running. Before connecting, however, if you consider the puzzle of determining which track is playing.

After looking at a few modules to read info regarding the media, a quick bit of coding gave you a file list. The file list is in a simple CSV format, each line containing two fields: the first the number of milliseconds in length, the latter the media’s title (this example is of several episodes available from the MercuryTheatre.info):

```
1709363,"Les Miserables Episode 1: The Bishop (broadcast date: 1937-07-23)"
1723781,"Les Miserables Episode 2: Javert (broadcast date: 1937-07-30)"
1723781,"Les Miserables Episode 3: The Trial (broadcast date: 1937-08-06)"
1678356,"Les Miserables Episode 4: Cosette (broadcast date: 1937-08-13)"
1646043,"Les Miserables Episode 5: The Grave (broadcast date: 1937-08-20)"
1714640,"Les Miserables Episode 6: The Barricade (broadcast date: 1937-08-27)"
1714640,"Les Miserables Episode 7: Conclusion (broadcast date: 1937-09-03)"
```

For this script, you can assume to be provided the following information:

```
* the value of $^T ($BASETIME) of the streamer script,
* the value of time(), and
* a CSV file containing the media to play consisting of the length in milliseconds and an identifier for the media (title, filename, or other).
```

Write a program to output which file is currently playing. For purposes of this script, you may assume gapless playback, and format the output as you see fit.

Optional: Also display the current position in the media as a time-like value.

### Example

```
Input: 3 command line parameters: start time, current time, file name

    # starttime
    1606134123

    # currenttime
    1614591276

    # filelist.csv

Output:

    "Les Miserables Episode 1: The Bishop (broadcast date: 1937-07-23)"
    00:10:24
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-103/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
use Text::CSV; # imports `csv` function

sub challenge(Int $start-time, Int $current-time, Str $file-name) returns Str {
    my @playlist          = csv(in => $file-name);
    my $playlist-length   = @playlist[*;0].sum;                                      # [1]
    my $playlist-position = ($current-time - $start-time) * 1000 % $playlist-length;

    my ($track, $timestamp);
    for @playlist -> ($track-length, $track-name) {
        # If we are <= the playlist position, skip to the next track
        if $track-length <= $playlist-position {
            $playlist-position -= $track-length;
            next;                                                                    # [2]
        }

        # We know we are in the right track now, so find how far in we are
        $track            = $track-name;
        my $total-seconds = ($playlist-position / 1000).Int;
        my $hour          = ($total-seconds / 3600).Int;
        my $minutes       = ($total-seconds % 3600 / 60).Int;
        my $seconds       = $total-seconds % 60;
        $timestamp        = sprintf('%02d:%02d:%02d', $hour, $minutes, $seconds);
        last;                                                                        # [3]
    }

    "$track\n$timestamp";
}

sub MAIN(Int $start-time, Int $current-time, Str $file-name) {
    say challenge($start-time, $current-time, $file-name);
}
```

This program runs as such:

```
# Assumes `filelist.csv` contains the above input
$ raku ch-2.raku 1606134123 1614591276 filelist.csv
Les Miserables Episode 1: The Bishop (broadcast date: 1937-07-23)
00:10:24
```

### Explanation

I found this question to be _incredibly_ confusing. Maybe it is the wording, or the fact that it was written by a guest author, but it didn't make sense to me at first. Additionally, we are _explicitly_ told that one set of numbers (the ones in the CSV) are in milliseconds, and the others are not specified; I started programming this assuming they are _also_ in milliseconds only to have to figure out later on they are in seconds. With that out of the way, let's look at the actual logic:

1. Read the CSV into a list of lists.
2. Find the total length of the playlist.
3. Find the position that we are in the playlist (in milliseconds).
4. Iterate through each track in the playlist:
  - If the length of the track is less than the position in the playlist, decrement the position in the playlist by the length of the track and continue
  - Otherwise, we are _in_ the track we need to be in, and we need to find the position in the track. We do this by calculating the total seconds we are into the track, then formatting that using some simple division. It's also important we remember to break after we have found what track we are in. 

#### Specific Comments

1. This is an interesting way to find the sum of a particular index in the list. This says "give me position 0 for the whole list, then sum it."
2. `next` is the equivalent of something like `continue` in other languages.
3. `last` is the equivalent of something like `break` in other languages.

## Final Thoughts

Overall, not my favorite set of questions this week, but what can you do! Hope y'all enjoy the rest of the `Metal Ox` year!
