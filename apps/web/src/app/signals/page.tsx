import { Metadata } from "next";
import { Card, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { AppShell } from "@/components/layout/AppShell";

export const metadata: Metadata = {
  title: "Signals — IDX Witcher",
  description: "Sinyal dan briefing harian pasar saham Indonesia.",
};

const signals = [
  { id: 1, title: "IHSG Momentum", status: "Bullish", desc: "Indeks menembus resistance 7.350 dengan volume di atas rata-rata." },
  { id: 2, title: "Foreign Flow", status: "Net Buy", desc: "Asing masuk net buy Rp 1.2T pada sektor perbankan." },
  { id: 3, title: "Sector Rotation", status: "Energy", desc: "Rotasi ke sektor energi dan bahan baku terlihat minggu ini." },
  { id: 4, title: "Dividend Radar", status: "Watch", desc: "Beberapa emiten blue-chip mendekati cum date." },
];

export default function SignalsPage() {
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

        <div className="grid gap-4 md:grid-cols-2">
          {signals.map((s) => (
            <Card key={s.id} hover>
              <div className="flex items-start justify-between gap-4">
                <div>
                  <CardTitle>{s.title}</CardTitle>
                  <p className="mt-2 text-sm text-[var(--text-secondary)]">{s.desc}</p>
                </div>
                <Badge
                  variant={
                    s.status === "Bullish" || s.status === "Net Buy"
                      ? "positive"
                      : s.status === "Watch"
                      ? "warning"
                      : "info"
                  }
                >
                  {s.status}
                </Badge>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
