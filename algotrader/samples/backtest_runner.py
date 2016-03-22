from algotrader.chart.plotter import StrategyPlotter
from algotrader.provider.broker.simulator import Simulator
from algotrader.provider.feed.csv import PandasCSVDataFeed
from algotrader.strategy.down_2pct_strategy import Down2PctStrategy
from algotrader.trading.instrument_data import inst_data_mgr
from algotrader.trading.order_mgr import order_mgr
from algotrader.trading.portfolio import Portfolio
from algotrader.utils import clock


class BacktestRunner:
    def __init__(self, stg):
        self.__stg = stg

    def start(self):
        clock.default_clock = clock.simluation_clock
        clock.simluation_clock.start()
        inst_data_mgr.start()
        order_mgr.start()

        self.__stg.start()


def main():
    feed = PandasCSVDataFeed(names=['spy'])
    portfolio = Portfolio(cash=100000)
    strategy = Down2PctStrategy("down2%", Simulator.ID, feed, portfolio, 1000)

    runner = BacktestRunner(strategy)
    runner.start()
    print portfolio.cash


    equity = strategy.get_portfolio().total_equity.get_series()
    equity.name = 'equity'
    rets =  equity.pct_change().dropna()
    rets.index = rets.index.tz_localize("UTC")

    print rets
    print type(rets)

    import pyfolio as pf
    #pf.create_returns_tear_sheet(rets)
    pf.create_full_tear_sheet(rets)

    import matplotlib.pyplot as plt
    plt.show()

    #plotter = StrategyPlotter(strategy)
    #plotter.plot()


if __name__ == "__main__":
    main()
