import { Metadata } from "next";
import { notFound } from "next/navigation";
import { Card, CardTitle } from "@/components/ui/Card";
import { AppShell } from "@/components/layout/AppShell";
import { PriceChart } from "@/components/charts/PriceChart";
import { api, OHLCV } from "@/lib/api";
import { generateMockOHLCV } from "@/lib/mock-data";
import { formatNumber } from "@/lib/format";

interface StockPageProps {
  params: Promise<{ ticker: string }>;
}

async function getPrices(ticker: string): Promise<OHLCV[]> {
  const data = await api.prices(ticker);
  if (!data || data.length === 0) {
    return generateMockOHLCV(ticker);
  }
  return data;
}

export async function generateMetadata({ params }: StockPageProps): Promise<Metadata> {
  const { ticker } = await params;
  return {
    title: `${ticker.toUpperCase()} — IDX Witcher`,
  };
}

export default async function StockPage({ params }: StockPageProps) {
  const { ticker } = await params;
  const code = ticker.toUpperCase();
  const data = await getPrices(code);

  if (!data || data.length === 0) {
    notFound();
  }

  const latest = data[data.length - 1];
  const previous = data[data.length - 2] ?? latest;
  const change = latest.close_price && previous.close_price
    ? latest.close_price - previous.close_price
    : 0;
  const changePercent = previous.close_price
    ? (change / previous.close_price) * 100
    : 0;

  const chartData = data.map((d) => ({
    date: d.date,
    open: d.open_price ?? 0,
    high: d.high_price ?? 0,
    low: d.low_price ?? 0,
    close: d.close_price ?? 0,
    volume: d.volume ?? 0,
  }));

  return (
    <AppShell>
      <div className="mx-auto max-w-7xl space-y-6">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-[var(--text-primary)]">
              {code}
            </h1>
            <p className="text-sm text-[var(--text-secondary)]">Stock detail & price chart</p>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold tabular-nums text-[var(--text-primary)]">
              {formatNumber(latest.close_price, 0)}
            </p>
            <p
              className={`text-sm font-medium tabular-nums ${
                change >= 0 ? "text-[var(--positive)]" : "text-[var(--negative)]"
              }`}
            >
              {change >= 0 ? "+" : ""}
              {formatNumber(change, 0)} ({change >= 0 ? "+" : ""}
              {changePercent.toFixed(2)}%)
            </p>
          </div>
        </div>

        <Card>
          <CardTitle>Price Chart</CardTitle>
          <div className="mt-4 min-h-[400px]">
            <PriceChart data={chartData} height={400} />
          </div>
        </Card>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardTitle>Open</CardTitle>
            <p className="mt-2 text-xl font-bold tabular-nums text-[var(--text-primary)]">
              {formatNumber(latest.open_price, 0)}
            </p>
          </Card>
          <Card>
            <CardTitle>High</CardTitle>
            <p className="mt-2 text-xl font-bold tabular-nums text-[var(--text-primary)]">
              {formatNumber(latest.high_price, 0)}
            </p>
          </Card>
          <Card>
            <CardTitle>Low</CardTitle>
            <p className="mt-2 text-xl font-bold tabular-nums text-[var(--text-primary)]">
              {formatNumber(latest.low_price, 0)}
            </p>
          </Card>
          <Card>
            <CardTitle>Volume</CardTitle>
            <p className="mt-2 text-xl font-bold tabular-nums text-[var(--text-primary)]">
              {formatNumber(latest.volume, 0)}
            </p>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
