# Remarks for Uchicago Trading Competition Exchange


I want to first thank the organizers to have conveyed such a gathering. It has certainly been fun trying to engineer some sort of program around the given "server.par" exchange engine.

Here I want to point to your attention some perceived bugs/problems in the "server.par" engine. I am confident they are not the result of bugs on our part, although by experience one can never be sure.

The statements given below can be checked by running our "market-marker.py" (everything is already installed). To do that, just:

`run case2 && sleep 5 && python market_maker.py`.

Now, may we have bugs, but we have noticed two major issues:

### No modified order ever gets filled.

  to check: `run case2 && sleep 5 && python market_maker.py configs/real_modify.py`

  - Let it run for 50 to 100 cycles, and stop it (Ctrl-C)
  - then open the log file in ".logs/market_maker.py.txt"
  - search for the word "modified", then the 6 "id" letters after "modified-"
  - then search for "filled-(id)": you should find none. Only other modifs that we keep doing with no result.

  You also see that we receive *a huge number of fills without order_id!* (search for "Could not find order (for fill_order): NONE")

  What are we doing wrong ?

  If nothing, then I suspect modified orders never get executed, as for us they seem to disappear in a black-hole.

### Execution queue is very slow

Now, we can mock modify_order by canceling and re-creating orders. Doing this, we get rid of the issue of non execution and fills without order_id.But even that creates its own sort of problems.

First it doubles the execution time (cancel+create instead of modify), which worrying especially for a market_maker.

But worse, it seems orders sometimes take 20 cycles to reach the execution engine.

To check: `run case2 && sleep 5 && python market_maker.py configs/mock_modify.py`

* in the log file (same as above), search for "CRITICAL", which usually indicates a filled order where we cannot find the original order in our own local orders inventory.
* if your search for the trade id, you will see that the trade has been canceled a long time ago (which is why it is no more in our own local orders inventory)
* so we get filled with sometimes a very old canceled trade.
We have noticed delays of more that 20 cycles.<br/><br/>

This may suggests (not sure) a sometimes very slow queue, which is worrying because locally we are only one. With 40 competitors the problem might be compounded and unmanageable.

We hope that at least the queue respects the order in which the orders were received, because we spent a lot of time trying to speed up the process on our end.


### Conclusion

We hope the issues outlined above are not due to our code. If they are, shame on us! (and please let us know...)

In any case, I heard that execution engines are notoriously hard to get right, especially when they need to cope with high bursts of volume.

In this case, I would have structured the exchange with one AWS lamba per competitor (which is cheap and would calculate competitor limits, pnl and fines) in order to keep the core matching engine "clean" and reasonably fast. It should be possible with 40 competitors, even using python.

Even if we would probably not invest real money with the exchange as it is now, we had fun trying to make something work. Thank you!
