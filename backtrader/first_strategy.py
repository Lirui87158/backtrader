import backtrader as bt
import pandas as pd

# 1. 定义一个简单的双均线策略
class DualMAStrategy(bt.Strategy):
    params = (
        ('fast_period', 10),
        ('slow_period', 30),
    )

    def __init__(self):
        self.fast_ma = bt.ind.SMA(period=self.params.fast_period)
        self.slow_ma = bt.ind.SMA(period=self.params.slow_period)
        self.crossover = bt.ind.CrossOver(self.fast_ma, self.slow_ma)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy(size=100)
        else:
            if self.crossover < 0:
                self.sell(size=100)

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(DualMAStrategy)

    # 加载 Backtrader 自带的示例数据
    data = bt.feeds.YahooFinanceCSVData(
        dataname='datas/orcl-1995-2014.txt',
        fromdate=pd.to_datetime('2000-01-01'),
        todate=pd.to_datetime('2010-01-01'),
        reverse=False)
    cerebro.adddata(data)

    # 设置资金和手续费
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    # 运行回测
    print(f'初始资金: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    print(f'最终资金: {cerebro.broker.getvalue():.2f}')

    # 画出回测图表
    cerebro.plot(style='candlestick')