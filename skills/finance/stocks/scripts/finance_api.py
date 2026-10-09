import sys
import json
import urllib.request
import urllib.parse
import argparse
from datetime import datetime

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

def make_request(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(json.dumps({"error": f"HTTP query failed: {str(e)}"}))
        sys.exit(1)

def resolve_ticker(company_name):
    encoded = urllib.parse.quote(company_name.strip())
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={encoded}&quotesCount=1"
    res = make_request(url)
    quotes = res.get("quotes", [])
    if quotes:
        first = quotes[0]
        symbol = first.get("symbol")
        longname = first.get("longname") or first.get("shortname") or symbol
        return {"symbol": symbol, "company": longname}
    return {"error": f"No ticker symbol found for: {company_name}"}

def fetch_latest(symbol):
    encoded = urllib.parse.quote(symbol.strip().upper())
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded}?range=1d"
    res = make_request(url)
    chart = res.get("chart", {})
    result_list = chart.get("result", [])
    
    if not result_list:
        error = chart.get("error", {})
        error_msg = error.get("description") if isinstance(error, dict) else "Unknown symbol or error"
        return {"error": f"Failed to retrieve latest data for '{symbol}': {error_msg}"}
        
    result = result_list[0]
    meta = result.get("meta", {})
    
    price = meta.get("regularMarketPrice")
    prev_close = meta.get("chartPreviousClose")
    
    change = None
    change_pct = None
    if price is not None and prev_close is not None:
        change = round(price - prev_close, 4)
        if prev_close != 0:
            change_pct = round((change / prev_close) * 100, 4)
            
    market_time_epoch = meta.get("regularMarketTime")
    time_str = None
    if market_time_epoch:
        time_str = datetime.fromtimestamp(market_time_epoch).isoformat()
        
    return {
        "symbol": meta.get("symbol"),
        "company": meta.get("longName") or meta.get("shortName") or symbol,
        "currency": meta.get("currency"),
        "price": price,
        "previous_close": prev_close,
        "change": change,
        "change_percent": change_pct,
        "high": meta.get("regularMarketDayHigh"),
        "low": meta.get("regularMarketDayLow"),
        "volume": meta.get("regularMarketVolume"),
        "market_time": time_str,
        "timezone": meta.get("exchangeTimezoneName"),
        "api_url": url
    }

def fetch_historical(symbol, start_date, end_date):
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        period1 = int(start_dt.timestamp())
        # To include the entire end_date, set timestamp to end of day
        period2 = int(end_dt.replace(hour=23, minute=59, second=59).timestamp())
    except Exception as e:
        return {"error": f"Invalid date format: {str(e)}. Use YYYY-MM-DD."}
        
    encoded = urllib.parse.quote(symbol.strip().upper())
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded}?period1={period1}&period2={period2}&interval=1d"
    res = make_request(url)
    chart = res.get("chart", {})
    result_list = chart.get("result", [])
    
    if not result_list:
        error = chart.get("error", {})
        error_msg = error.get("description") if isinstance(error, dict) else "Unknown symbol or error"
        return {"error": f"Failed to retrieve historical data for '{symbol}': {error_msg}"}
        
    result = result_list[0]
    meta = result.get("meta", {})
    timestamps = result.get("timestamp", [])
    indicators = result.get("indicators", {})
    quote_list = indicators.get("quote", [{}])
    quote = quote_list[0] if quote_list else {}
    
    opens = quote.get("open", [])
    highs = quote.get("high", [])
    lows = quote.get("low", [])
    closes = quote.get("close", [])
    volumes = quote.get("volume", [])
    
    adjclose_list = indicators.get("adjclose", [{}])
    adjcloses = adjclose_list[0].get("adjclose", []) if adjclose_list else []
    
    quotes_formatted = []
    for i in range(len(timestamps)):
        ts = timestamps[i]
        date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        
        # Round values for cleaner presentation
        o = round(opens[i], 4) if i < len(opens) and opens[i] is not None else None
        h = round(highs[i], 4) if i < len(highs) and highs[i] is not None else None
        l = round(lows[i], 4) if i < len(lows) and lows[i] is not None else None
        c = round(closes[i], 4) if i < len(closes) and closes[i] is not None else None
        ac = round(adjcloses[i], 4) if i < len(adjcloses) and adjcloses[i] is not None else None
        vol = volumes[i] if i < len(volumes) else None
        
        if o is None and c is None:
            continue # Skip non-trading dummy/holiday entries
            
        quotes_formatted.append({
            "date": date_str,
            "open": o,
            "high": h,
            "low": l,
            "close": c,
            "adj_close": ac,
            "volume": vol
        })
        
    return {
        "symbol": meta.get("symbol"),
        "company": meta.get("longName") or meta.get("shortName") or symbol,
        "currency": meta.get("currency"),
        "timezone": meta.get("exchangeTimezoneName"),
        "quotes": quotes_formatted,
        "api_url": url
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Yahoo Finance details.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommand to execute")
    
    # Resolve subparser
    resolve_parser = subparsers.add_parser("resolve", help="Resolve company name to ticker symbol")
    resolve_parser.add_argument("--company", required=True, help="Company name to search")
    
    # Latest subparser
    latest_parser = subparsers.add_parser("latest", help="Fetch latest stock quote")
    latest_parser.add_argument("--symbol", required=True, help="Ticker symbol")
    
    # Historical subparser
    historical_parser = subparsers.add_parser("historical", help="Fetch historical daily quotes")
    historical_parser.add_argument("--symbol", required=True, help="Ticker symbol")
    historical_parser.add_argument("--start", required=True, help="Start date (YYYY-MM-DD)")
    historical_parser.add_argument("--end", required=True, help="End date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    if args.command == "resolve":
        print(json.dumps(resolve_ticker(args.company), indent=2))
    elif args.command == "latest":
        print(json.dumps(fetch_latest(args.symbol), indent=2))
    elif args.command == "historical":
        print(json.dumps(fetch_historical(args.symbol, args.start, args.end), indent=2))
