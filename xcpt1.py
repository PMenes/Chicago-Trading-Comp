import src.utils as u
from market_maker import MarketMaker

if __name__ == "__main__":
    u.launch_server_async(MarketMaker, __file__)
