---
title: "Advent of Code: Year 2020, Day 25"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Merry Christmas! Part two was probably my favorite part of all of Advent of Code; check it out!

## The Problem

### Part 1

We finally get to the front desk of the resort, and they tell us that the system is down, and we will be unable to check in. Luckily, they created all the room keys this morning, so we _will_ be able to go to our room, and just formally check in later. We are on the 25th floor, and the elevator is broken. 🙃

We make it to our room and scan the key and get the disheartening red light from the door. Luckily, there is a number to call IT on the card, and we give them a ring. They say we can either go down to the front desk to get it reset or reverse engineer the cryptographic handshake between the card and the door. Obviously we will take the latter choice.

We're able to obtain the _public keys_ of both the door and the card (our input). To find the cryptographic handshake we must take the subject number (a constant; `7`) and transform it according to the following rules:

1. Start with a value of `1`
2. Set the value equal to itself times the subject number (`7`)
3. Set the value equal to the remainder after dividing by `20201227`
4. Continue until the value equals the device's public key
5. For the above steps, count how many loops it took; this is the secret **loop size**

Once we have found the secret loop size for one of the devices, we can take the loop size and apply the same transformation as above using the public key from _the other device_ as our subject number, which yields the handshake key. Let's look at an example:

```
Card Public Key: 5764801
Door Public Key: 17807724

--- Finding the loop size for the card ---
# Loop 1
value = 1 * 7        = 7
value = 7 % 20201227 = 7

# Loop 2
value = 7 * 7         = 49
value = 49 % 20201227 = 49

# Loop 3
value = 49 * 7         = 343
value = 343 % 20201227 = 343

# Loop 4
value = 343 * 7         = 2401
value = 2401 % 20201227 = 2401

# Loop 5
value = 2401 * 7         = 16807
value = 16807 % 20201227 = 16807

# Loop 6
value = 16807 * 7         = 117649
value = 117649 % 20201227 = 117649

# Loop 7
value = 117649 * 7        = 823543
value = 823543 % 20201227 = 823543

# Loop 8
value = 823543 * 7         = 5764801
value = 5764801 % 20201227 = 5764801 <-- The card's public key

--- Applying the loop size to the door ---
# Loop 1
value = 1 * 17807724        = 17807724
value = 17807724 % 20201227 = 17807724

# Loop 2
value = 17807724 * 17807724        = 317115034060176
value = 317115034060176 % 20201227 = 10847306

# Loop 3
value = 10847306 * 17807724        = 193165831391544
value = 193165831391544 % 20201227 = 1914476

# Loop 4
value = 1914476 * 17807724        = 34092460212624
value = 34092460212624 % 20201227 = 874663

# Loop 5
value = 874663 * 17807724         = 15575757297012
value = 15575757297012 % 20201227 = 5243202

# Loop 6
value = 5243202 * 17807724        = 93369494092248
value = 93369494092248 % 20201227 = 8733831

# Loop 7
value = 8733831 * 17807724         = 155529651910644
value = 155529651910644 % 20201227 = 1213104

# Loop 8
value = 1213104 * 17807724        = 21602621215296
value = 21602621215296 % 20201227 = 14897079       <-- Cryptographic Handshake
```

I will not display it, but if we had found the door's loop size and then used the card's public key as the subject number, we would have come to the same cryptographic handshake; this is how the door, and the card know they are a match.

With our _real_ card and door public keys, what is the cryptographic handshake between them?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/25/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub MAIN($file) {
    my ($card-key, $door-key) = $file.IO.lines.map(*.Int);
    my $handshake = 1;
    my $target = 1;
    while $target != $door-key {
        $target = ($target * 7) % 20201227;
        $handshake = ($handshake * $card-key) % 20201227;
    }
    say $handshake;
}
```

This runs as such:

```
$ raku main.raku input.txt
18293391
```

#### Explanation

Rather than keep track of the loop size, we just do the above 2 loops in parallel until `$target` matches `$door-key`. Rather than do the two steps outline above, we are able to do the multiplication and remainder division ([modulo](https://en.wikipedia.org/wiki/Modulo_operation)) in one step. Finally, all we have to do is say the handshake!

### Part 2

2020 has been a tough year and everyone needs a break. Day 25 part 2 is a freebie. 🙂

## Final Thoughts

I had my ups and downs with this challenge. Obviously I did not fulfill my goal of solving everything in functional Raku; in fact, I wasn't even able to solve everything in Raku. However, I learned a lot about the language, I learned a few new algorithms, and I had fun! This whole thing was a lot of fun, and I want to thank [Eric](https://github.com/topaz) for doing it for the past 6 years (even though this was my first time participating).

Next year I will have a one-and-a-half-year-old, so no promises I will be able to blog every day (it was hard enough this year), but I will do my best to participate, and I may blog for problems I find particularly clever.

With that, I would like to wish everyone a very merry Christmas and a happy New Year!
