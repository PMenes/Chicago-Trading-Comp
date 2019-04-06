## Instructions for working & testing the UChicago Trading contest


### installation

- `git clone https://github.com/PMenes/ucess.git`
- make sure your virtual env is python > 3.6
- run `pip install -r src/scripts/requirements.txt`

###### for updates
- just `git pull`
- ... and maybe re-run `pip install -r src/scripts/requirements.txt`


### quick start

- first `export PATH="$PATH:./src/scripts"`

    so that you can use the shortcut 'run' (instead of 'python multi_starter.py')

- ..then, for case 2:
    - `run case2`
    - `python market_maker.py`
    - in your browser (firefox), open http://localhost:5046/#case2

    If everything went well, you should see the random strategy running.

- for case 1 (not optimized yet):
    - `run case1`
    - `python case1.py`
    - in your browser (firefox), open http://localhost:5046/#case1


- To stop: `run caseX -stop` (X being 1 or 2)

### changing strategies

market_maker.py includes 3 example strategies: "random", "paul" and "christian"

Example: to run the "paul" strategy:

- open config.json
- in the process key "market_maker.py", change "strategy": "random" with "strategy": "paul"

Test all strategies !

### changing "config.json"

That's the file storing all parameters. Some tips:

- exchange: change the IP and ports according to which exchange you want to connect to.
    It could be a remote exchange, doesn't have to be your local computer one.

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

- you can change the groups *case1* or *case2*, or create more groups. If you create a new group, just do `run mynewgroup`

- ... then run your file `python mytraderfile.py`


### structure of programs

*exchanges <---> market_maker.py ---> distributor.py ---> any and/or multiple clients*

Anybody can act as a client and connect to the distributor.

If you open a port on your router, they can do it from anywhere in the world. Be very careful though, there is absolutely *NO SECURITY* built in the programs, they are meant to be only local.

Note that we did not program any client input back to market_maker.py, but you could if you want to alter the automated trading from your browser.

You'll need to adapt distributor.py and market_maker.py to do that obviously, but that's not rocket science.
