"use client";

import { useEffect, useState } from "react";
import { Card, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { AppShell } from "@/components/layout/AppShell";
import { api, MarketSummary } from "@/lib/api";
import { formatCompact, formatNumber, formatPercent } from "@/lib/format";

interface Signal {
  id: number;
  title: string;
  status: string;
  desc: string;
  variant: "positive" | "warning" | "info" | "negative";
}

const staticSignals: Signal[] = [
  {
    id: 1,
    title: "IHSG Momentum",
    status: "Bullish",
    desc: "Indeks menembus resistance 7.350 dengan volume di atas rata-rata.",
    variant: "positive",
  },
  {
    id: 2,
    title: "Foreign Flow",
    status: "Net Buy",
    desc: "Asing masuk net buy Rp 1.2T pada sektor perbankan.",
    variant: "positive",
  },
  {
    id: 3,
    title: "Sector Rotation",
    status: "Energy",
    desc: "Rotasi ke sektor energi dan bahan baku terlihat minggu ini.",
    variant: "warning",
  },
  {
    id: 4,
    title: "Dividend Radar",
    status: "Watch",
    desc: "Beberapa emiten blue-chip mendekati cum date.",
    variant: "info",
  },
];

export default function SignalsPage() {
  const [summary, setSummary] = useState<MarketSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.marketSummary()
      .then((data) => {
        if (data) setSummary(data);
      })
      .finally(() => setLoading(false));
  }, []);

  const isBullish = (summary?.change_percent ?? 0) >= 0;

  return (
    <AppShell>
      <div className="mx-auto max-w-7xl space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--text-primary)]">
            Signals
          </h1>
          <p className="mt-1 text-sm text-[var(--text-secondary)]">
            Sinyal dan briefing harian untuk pasar saham Indonesia.
          </p>
        </div>

        <Card className="bg-gradient-to-r from-[var(--accent-cyan)]/10 to-[var(--accent-violet)]/10">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <CardTitle>IHSG Snapshot</CardTitle>
              {loading ? (
                <p className="mt-2 text-sm text-[var(--text-muted)]">Loading...</p>
              ) : summary?.close ? (
                <div className="mt-2 flex items-baseline gap-3">
                  <span className="text-3xl font-bold tabular-nums text-[var(--text-primary)]">
                    {formatNumber(summary.close, 0)}
                  </span>
                  <span
                    className={`text-sm font-medium tabular-nums ${
                      isBullish ? "text-[var(--positive)]" : "text-[var(--negative)]"
                    }`}
                  >
                    {isBullish ? "+" : ""}
                    {formatNumber(summary.change, 0)} ({formatPercent(summary.change_percent)})
                  </span>
                </div>
              ) : (
                <p className="mt-2 text-sm text-[var(--text-muted)]">Data IHSG belum tersedia.</p>
              )}
            </div>
            <div className="text-sm text-[var(--text-secondary)]">
              <p>High: {summary?.high ? formatNumber(summary.high, 0) : "-"}</p>
              <p>Low: {summary?.low ? formatNumber(summary.low, 0) : "-"}</p>
              <p>Value: {summary?.value ? formatCompact(summary.value) : "-"}</p>
            </div>
          </div>
        </Card>

        <div className="grid gap-4 md:grid-cols-2">
          {staticSignals.map((s) => (
            <Card key={s.id} hover>
              <div className="flex items-start justify-between gap-4">
                <div>
                  <CardTitle>{s.title}</CardTitle>
                  <p className="mt-2 text-sm text-[var(--text-secondary)]">{s.desc}</p>
                </div>
                <Badge variant={s.variant}>{s.status}</Badge>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
