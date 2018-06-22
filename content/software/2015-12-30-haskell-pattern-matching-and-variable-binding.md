---
layout: single
title:  "Haskell pattern matching and variable binding"
date:   2015-12-30 23:15:00 -0200
categories: programming
tags:   haskell
---
After a long time away from Haskell, I’ve just gotten back fiddling with it. I was trying to create a function that would filter objects based on their constructor parameters, so I’ve made for you an example with… right, *shoes*. I thought that it was so Haskell-y to write something like this, to create a filter based on the parameters I give to the `filterOnColorAndSize` function:

{% highlight haskell %}
data Color = Blue | Red | Green deriving (Eq, Show)
data Shoe = Shoe { color :: Color, size :: Int } deriving (Eq, Show)

-- this doesn’t work
filterOnColorAndSize c s = filter predicate where
    predicate (Shoe c s) = True
    predicate _          = False
{% endhighlight %}

But it doesn’t work. It does run, but the compiler warns that the patterns overlap, and indeed when I ran it I saw that it didn’t filter anything, it just passed everything through. The catch here is that *when you do pattern matching on a constructor, **a new variable is bound***. I did some research and, although I’m not positive that I’ve tracked down pretty much everything about it, it seems that there’s no way to circumvent that; you can’t pattern match on the value of a variable, and you can’t catch anything from the enclosing scope. So that leaves no alternative but to write an explicit comparison, like that:

{% highlight haskell %}
filterOnColorAndSize c s = filter predicate where
    predicate (Shoe c' s')
        | (c' == c && s' == s) = True
        | otherwise            = False

-- a sample dataset to save you some time
shoeList = [ Shoe c s | c <- [Blue, Red, Green], s <- [34 .. 42]]
{% endhighlight %}
