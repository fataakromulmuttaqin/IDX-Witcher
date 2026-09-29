import { Metadata } from "next";
import { Card, CardTitle } from "@/components/ui/Card";
import { StatCard } from "@/components/ui/StatCard";
import { Badge } from "@/components/ui/Badge";
import { AppShell } from "@/components/layout/AppShell";
import { api, MarketSummary, TopMover } from "@/lib/api";
import { formatCompact, formatNumber, formatPercent } from "@/lib/format";
import { mockMarketSummary, mockTopMovers } from "@/lib/mock-data";

export const metadata: Metadata = {
  title: "Dashboard — Alpha Cygni",
  description: "Ringkasan pasar saham Indonesia",
};

async function getMarketSummary(): Promise<MarketSummary | null> {
  return (await api.marketSummary()) ?? mockMarketSummary;
}

async function getTopMovers(): Promise<TopMover[]> {
  return (await api.topMovers()) ?? mockTopMovers;
}

export default async function DashboardPage() {
  const summary = await getMarketSummary();
  const topMovers = await getTopMovers();

  return (
    <AppShell>
      <div className="mx-auto max-w-7xl space-y-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-[var(--text-primary)]">
              Dashboard
            </h1>
            <p className="mt-1 text-sm text-[var(--text-secondary)]">
              Ringkasan pasar dan sinyal utama hari ini.
            </p>
          </div>
          <Badge variant="info">Live</Badge>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            label="IHSG"
            value={summary?.close ?? null}
            change={summary?.change_percent ?? null}
          />
          <StatCard
            label="High"
            value={summary?.high ?? null}
          />
          <StatCard
            label="Low"
            value={summary?.low ?? null}
          />
          <StatCard
            label="Volume"
            value={summary?.volume ?? null}
            change={undefined}
          />
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          <Card className="lg:col-span-2">
            <CardTitle>Market Overview</CardTitle>
            <div className="mt-4">
              {summary?.close ? (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-[var(--text-muted)]">Index</span>
                    <span className="font-medium text-[var(--text-primary)]">
                      {summary.index_name ?? "IHSG"}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-[var(--text-muted)]">Change</span>
                    <span
                      className={`font-medium tabular-nums ${
                        (summary.change ?? 0) >= 0 ? "text-[var(--positive)]" : "text-[var(--negative)]"
                      }`}
                    >
                      {formatPercent(summary.change_percent)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-[var(--text-muted)]">Value</span>
                    <span className="font-medium tabular-nums text-[var(--text-primary)]">
                      {formatCompact(summary.value)}
                    </span>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-[var(--text-muted)]">No market data.</p>
              )}
            </div>
          </Card>

          <Card>
            <CardTitle>Top Movers by Volume</CardTitle>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-[var(--border-default)] text-xs text-[var(--text-muted)]">
                    <th className="pb-2 font-medium">Ticker</th>
                    <th className="pb-2 font-medium text-right">Close</th>
                    <th className="pb-2 font-medium text-right">Volume</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border-subtle)]">
                  {topMovers.map((m) => (
                    <tr key={m.code} className="group">
                      <td className="py-3">
                        <a
                          href={`/stocks/${m.code}`}
                          className="font-medium text-[var(--text-primary)] group-hover:text-[var(--accent-cyan)] transition-colors"
                        >
                          {m.code}
                        </a>
                      </td>
                      <td className="py-3 text-right tabular-nums text-[var(--text-secondary)]">
                        {formatNumber(m.close, 0)}
                      </td>
                      <td className="py-3 text-right tabular-nums text-[var(--text-secondary)]">
                        {formatCompact(m.volume)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
