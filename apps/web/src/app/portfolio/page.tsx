"use client";

import { useState } from "react";
import { Card, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { AppShell } from "@/components/layout/AppShell";
import { api } from "@/lib/api";

interface PortfolioItem {
  code: string;
  weight: number;
  expected_return_5d: number;
  confidence: number;
}

interface PortfolioResult {
  ok: boolean;
  risk_profile: string;
  portfolio: PortfolioItem[];
  cash_weight: number;
  expected_return_annual: number;
  volatility_annual: number;
  sharpe: number;
}

const profiles = [
  { id: "conservative", label: "Konservatif", desc: "Target return stabil, toleransi risiko rendah." },
  { id: "moderate", label: "Moderat", desc: "Keseimbangan return dan risiko." },
  { id: "aggressive", label: "Agresif", desc: "Target return tinggi, toleransi risiko tinggi." },
];

export default function PortfolioPage() {
  const [step, setStep] = useState<"select" | "result">("select");
  const [profile, setProfile] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PortfolioResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSelect = async (id: string) => {
    setLoading(true);
    setProfile(id);
    setError(null);
    try {
      const data = await api.buildPortfolio(id);
      if (!data) {
        throw new Error("Tidak bisa terhubung ke backend");
      }
      setResult(data);
      setStep("result");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Gagal membangun portofolio");
      setProfile(null);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setProfile(null);
    setResult(null);
    setError(null);
    setStep("select");
  };

  return (
    <AppShell>
      <div className="mx-auto max-w-7xl space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--text-primary)]">
            AI Portfolio Builder
          </h1>
          <p className="mt-1 text-sm text-[var(--text-secondary)]">
            Pilih profil risiko, lalu lihat rekomendasi alokasi portofolio berbasis AI.
          </p>
        </div>

        {error && (
          <div className="rounded-lg border border-[var(--negative)]/30 bg-[var(--negative-dim)] p-4 text-sm text-[var(--negative)]">
            {error}
          </div>
        )}

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

        {step === "result" && result && (
          <>
            <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h2 className="text-lg font-semibold text-[var(--text-primary)]">
                  Profil: {profiles.find((p) => p.id === result.risk_profile)?.label}
                </h2>
                <p className="text-sm text-[var(--text-secondary)]">
                  Expected return tahunan: <strong>{(result.expected_return_annual * 100).toFixed(2)}%</strong> ·
                  Volatilitas: <strong>{(result.volatility_annual * 100).toFixed(2)}%</strong> ·
                  Sharpe: <strong>{result.sharpe.toFixed(2)}</strong>
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
                      <th className="pb-3 font-medium text-right">Weight</th>
                      <th className="pb-3 font-medium text-right">Expected Return (5D)</th>
                      <th className="pb-3 font-medium">Confidence</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--border-subtle)]">
                    {result.portfolio.map((s) => (
                      <tr key={s.code} className="hover:bg-[var(--bg-surface-highlight)]/50">
                        <td className="py-4 pl-2 font-bold tabular-nums text-[var(--text-primary)]">
                          {s.code}
                        </td>
                        <td className="py-4 text-right tabular-nums text-[var(--text-primary)]">
                          {(s.weight * 100).toFixed(2)}%
                        </td>
                        <td className="py-4 text-right tabular-nums text-[var(--positive)]">
                          {(s.expected_return_5d * 100).toFixed(2)}%
                        </td>
                        <td className="py-4">
                          <Badge variant={s.confidence > 0.7 ? "positive" : "info"}>
                            {(s.confidence * 100).toFixed(0)}%
                          </Badge>
                        </td>
                      </tr>
                    ))}
                    {result.cash_weight > 0 && (
                      <tr className="hover:bg-[var(--bg-surface-highlight)]/50">
                        <td className="py-4 pl-2 font-bold tabular-nums text-[var(--text-primary)]">
                          CASH
                        </td>
                        <td className="py-4 text-right tabular-nums text-[var(--text-primary)]">
                          {(result.cash_weight * 100).toFixed(2)}%
                        </td>
                        <td className="py-4 text-right tabular-nums text-[var(--text-muted)]">-</td>
                        <td className="py-4">
                          <Badge variant="default">reservasi</Badge>
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </Card>

            <Card className="bg-gradient-to-r from-[var(--accent-cyan)]/10 to-[var(--accent-violet)]/10">
              <p className="text-sm text-[var(--text-secondary)]">
                <strong>Disclaimer:</strong> Hasil di atas adalah simulasi berbasis data historis
                dan model AI sederhana. Bukan rekomendasi investasi. Keputusan investasi sepenuhnya
                menjadi tanggung jawab pengguna.
              </p>
            </Card>
          </>
        )}
      </div>
    </AppShell>
  );
}
