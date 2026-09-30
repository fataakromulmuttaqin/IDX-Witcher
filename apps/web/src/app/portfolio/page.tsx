"use client";

import { useState } from "react";
import { Card, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { AppShell } from "@/components/layout/AppShell";

interface MockStock {
  code: string;
  name: string;
  sector: string;
  weight: number;
  expectedReturn: number;
  risk: "low" | "medium" | "high";
}

const profiles = [
  {
    id: "conservative",
    label: "Konservatif",
    desc: "Target return stabil, toleransi risiko rendah.",
  },
  {
    id: "moderate",
    label: "Moderat",
    desc: "Keseimbangan return dan risiko.",
  },
  {
    id: "aggressive",
    label: "Agresif",
    desc: "Target return tinggi, toleransi risiko tinggi.",
  },
];

const mockPortfolio: Record<string, MockStock[]> = {
  conservative: [
    { code: "BBCA", name: "Bank Central Asia", sector: "Financials", weight: 25, expectedReturn: 8.5, risk: "low" },
    { code: "BBRI", name: "Bank Rakyat Indonesia", sector: "Financials", weight: 20, expectedReturn: 9.2, risk: "low" },
    { code: "TLKM", name: "Telkom Indonesia", sector: "Technology", weight: 18, expectedReturn: 7.8, risk: "low" },
    { code: "ASII", name: "Astra International", sector: "Consumer", weight: 15, expectedReturn: 8.1, risk: "medium" },
    { code: "INDF", name: "Indofood Sukses Makmur", sector: "Consumer", weight: 12, expectedReturn: 7.5, risk: "low" },
    { code: "CASH", name: "Kas", sector: "-", weight: 10, expectedReturn: 5.0, risk: "low" },
  ],
  moderate: [
    { code: "BBCA", name: "Bank Central Asia", sector: "Financials", weight: 18, expectedReturn: 10.2, risk: "medium" },
    { code: "BBRI", name: "Bank Rakyat Indonesia", sector: "Financials", weight: 15, expectedReturn: 11.5, risk: "medium" },
    { code: "TLKM", name: "Telkom Indonesia", sector: "Technology", weight: 14, expectedReturn: 9.8, risk: "medium" },
    { code: "ASII", name: "Astra International", sector: "Consumer", weight: 13, expectedReturn: 12.1, risk: "medium" },
    { code: "INDF", name: "Indofood Sukses Makmur", sector: "Consumer", weight: 12, expectedReturn: 10.5, risk: "medium" },
    { code: "ANTM", name: "Aneka Tambang", sector: "Materials", weight: 10, expectedReturn: 14.2, risk: "high" },
    { code: "CASH", name: "Kas", sector: "-", weight: 8, expectedReturn: 5.0, risk: "low" },
  ],
  aggressive: [
    { code: "ANTM", name: "Aneka Tambang", sector: "Materials", weight: 20, expectedReturn: 18.5, risk: "high" },
    { code: "BBCA", name: "Bank Central Asia", sector: "Financials", weight: 15, expectedReturn: 13.2, risk: "medium" },
    { code: "BBRI", name: "Bank Rakyat Indonesia", sector: "Financials", weight: 14, expectedReturn: 14.5, risk: "medium" },
    { code: "ASII", name: "Astra International", sector: "Consumer", weight: 12, expectedReturn: 15.1, risk: "high" },
    { code: "INDF", name: "Indofood Sukses Makmur", sector: "Consumer", weight: 10, expectedReturn: 13.5, risk: "high" },
    { code: "TLKM", name: "Telkom Indonesia", sector: "Technology", weight: 10, expectedReturn: 12.8, risk: "medium" },
    { code: "PTBA", name: "Bukit Asam", sector: "Energy", weight: 9, expectedReturn: 17.2, risk: "high" },
    { code: "CASH", name: "Kas", sector: "-", weight: 10, expectedReturn: 5.0, risk: "low" },
  ],
};

export default function PortfolioPage() {
  const [step, setStep] = useState<"select" | "result">("select");
  const [profile, setProfile] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSelect = (id: string) => {
    setLoading(true);
    setProfile(id);
    setTimeout(() => {
      setLoading(false);
      setStep("result");
    }, 1200);
  };

  const reset = () => {
    setProfile(null);
    setStep("select");
  };

  const currentPortfolio = profile ? mockPortfolio[profile] : [];
  const totalReturn =
    currentPortfolio.reduce((acc, s) => acc + (s.expectedReturn * s.weight) / 100, 0);

  return (
    <AppShell>
      <div className="mx-auto max-w-7xl space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--text-primary)]">
            AI Portfolio Builder
          </h1>
          <p className="mt-1 text-sm text-[var(--text-secondary)]">
            Pilih profil risiko, lalu lihat rekomendasi alokasi portofolio.
          </p>
        </div>

        {step === "select" && (
          <div className="grid gap-4 md:grid-cols-3">
            {profiles.map((p) => (
              <Card key={p.id} className="flex flex-col">
                <CardTitle>{p.label}</CardTitle>
                <p className="mt-2 flex-1 text-sm text-[var(--text-secondary)]">{p.desc}</p>
                <Button
                  className="mt-6 w-full"
                  onClick={() => handleSelect(p.id)}
                  disabled={loading}
                >
                  {loading && profile === p.id ? "Memproses..." : "Pilih"}
                </Button>
              </Card>
            ))}
          </div>
        )}

        {step === "result" && profile && (
          <>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-[var(--text-primary)]">
                  Profil: {profiles.find((p) => p.id === profile)?.label}
                </h2>
                <p className="text-sm text-[var(--text-secondary)]">
                  Estimasi return tahunan: <strong>{totalReturn.toFixed(2)}%</strong>
                </p>
              </div>
              <Button variant="secondary" onClick={reset}>
                Ulangi
              </Button>
            </div>

            <Card>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead>
                    <tr className="border-b border-[var(--border-default)] text-xs uppercase tracking-wider text-[var(--text-muted)]">
                      <th className="pb-3 pl-2 font-medium">Ticker</th>
                      <th className="pb-3 font-medium">Name</th>
                      <th className="pb-3 font-medium">Sector</th>
                      <th className="pb-3 font-medium text-right">Weight</th>
                      <th className="pb-3 font-medium text-right">Expected Return</th>
                      <th className="pb-3 font-medium">Risk</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--border-subtle)]">
                    {currentPortfolio.map((s) => (
                      <tr key={s.code} className="hover:bg-[var(--bg-surface-highlight)]/50">
                        <td className="py-4 pl-2 font-bold tabular-nums text-[var(--text-primary)]">
                          {s.code}
                        </td>
                        <td className="py-4 text-[var(--text-secondary)]">{s.name}</td>
                        <td className="py-4 text-[var(--text-secondary)]">{s.sector}</td>
                        <td className="py-4 text-right tabular-nums text-[var(--text-primary)]">
                          {s.weight}%
                        </td>
                        <td className="py-4 text-right tabular-nums text-[var(--positive)]">
                          {s.expectedReturn.toFixed(1)}%
                        </td>
                        <td className="py-4">
                          <Badge
                            variant={
                              s.risk === "high"
                                ? "negative"
                                : s.risk === "medium"
                                ? "warning"
                                : "positive"
                            }
                          >
                            {s.risk}
                          </Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>

            <Card className="bg-gradient-to-r from-[var(--accent-cyan)]/10 to-[var(--accent-violet)]/10">
              <p className="text-sm text-[var(--text-secondary)]">
                <strong>Disclaimer:</strong> Hasil di atas adalah simulasi berbasis data historis
                dan asumsi sederhana. Bukan rekomendasi investasi. Keputusan investasi sepenuhnya
                menjadi tanggung jawab pengguna.
              </p>
            </Card>
          </>
        )}
      </div>
    </AppShell>
  );
}
