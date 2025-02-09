from django.shortcuts import get_object_or_404, redirect, render
from dal import autocomplete
from .models import Stock, StockData
from .forms import StockForm
from .utils import scrape_stock_data
from django.contrib import messages

def stocks(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock_id = request.POST.get('stock')   # primary key
            stock = Stock.objects.get(pk=stock_id)
            symbol = stock.symbol

            exchange = stock.exchange

            stock_response = scrape_stock_data(symbol, exchange)

            if stock_response:
                try:
                    stock_data = StockData.objects.get(stock=stock)
                except StockData.DoesNotExist:
                    stock_data = StockData(stock=stock)

                # update stock data instance with the response data
                stock_data.current_price = stock_response["current_price"]
                stock_data.price_changed = stock_response["price_changed"]
                stock_data.percentage_change = stock_response["percentage_change"]
                stock_data.previous_close = stock_response["previous_close"]
                stock_data.week_52_high = stock_response["week_52_high"]
                stock_data.week_52_low = stock_response["week_52_low"]
                stock_data.market_cap = stock_response["market_cap"]
                stock_data.pe_ratio = stock_response["pe_ratio"]
                stock_data.dividend_yield = stock_response["dividend_yield"]
                stock_data.save()
                return redirect('stock_detail', stock_data.id)
            else:
                messages.error(request, f'Could not fetch data for {symbol}')
                return redirect('stocks')

    else:
        form = StockForm()
        context = {
            'form': form,
        }
        return render(request, "stockannalysis/stocks.html", context)


def stock_detail(request, pk):
    stock_data = get_object_or_404(StockData, pk=pk)
    context = {
        'stock_data': stock_data,
    }
    return render(request, "stockannalysis/stock_detail.html", context)


class StockAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Stock.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
