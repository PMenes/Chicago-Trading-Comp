## Instructions for working & testing the UChicago Trading contest


### installation

- create your working folder ex: myfolder
- get the boostrap.sh file somewhere... and copy it to myfolder
- cd to myfolder
- run `bash bootstrap.sh`

This should have installed the full progam on your computer (not really tested though..)


### quick start

- run `python run.py all`
- in your browser (firefox), open http://localhost:5046

If everything went well, you should see the random strategy running.

To stop, run `python run.py all -stop`

### changing strategies

market_maker.py includes 3 example strategies: "default", "paul" and "christian"

Example: to run the "paul" strategy:

- open config.json
- change "strategy": "default" with "strategy": "paul"

Test all strategies !

### changing "config.json"

That's the file storing all parameters. Some tips:

- exchange: change the IP and ports according to which exchange you want to connect to.

- processes: if you change them, make sure you keep the order: "case_two_bot.par" need "server.par" to have started first, and "market_maker.py" need "distributor.py" (unless you take it out in the "connect_to" parameter) for example.

- you can also change strategy parameters. Any change will overwrite "default"

- ...or change the limits

- env: change to "dev"

### developping

Obviously you want to develop your own strategy.

You can create your own "my_market_maker.py" file.
If you do, make sure to update the config file with your file name.


###### Tips
- You could change the "env" parameter "dev" instead of "prod" to throw on exceptions.

- when developping, run first

    `python run.py server.par case_two_bot.par distributor.py -start`

- ... then run your file `python myfile.py`


### structure of programs

*exchanges <---> market_maker.py ---> distributor.py ---> any and/or multiple clients*

Anybody can act as a client and connect to the distributor.

If you open a port on your router, they can do it from anywhere in the world. Be very careful though, there is absolutely *NO SECURITY* built in the programs, they are meant to be only local.

Note that we did not program any client input back to market_maker.py, but you could if you want to alter the automated trading from your browser.

You'll need to adapt distributor.py and market_maker.py to do that obviously, but that's not rocket science.


### for updates

In case of updates:

- go to your folder (ex: myfolder)
- get the update.sh file somewhere... and copy it to myfolder
- run `bash update.sh`
