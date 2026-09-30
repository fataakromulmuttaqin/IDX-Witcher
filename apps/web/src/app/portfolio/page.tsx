import { Metadata } from "next";
import { Card } from "@/components/ui/Card";
import { AppShell } from "@/components/layout/AppShell";

export const metadata: Metadata = {
  title: "Portfolio — IDX Witcher",
  description: "AI-optimized portfolio builder untuk saham LQ45.",
};

export default function PortfolioPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-7xl space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--text-primary)]">
            AI Portfolio Builder
          </h1>
          <p className="mt-1 text-sm text-[var(--text-secondary)]">
            Rekomendasi alokasi portofolio berdasarkan model NeuralAlpha.
          </p>
        </div>

        <Card className="flex h-96 flex-col items-center justify-center text-center">
          <div className="mb-4 h-16 w-16 rounded-full border border-[var(--border-default)] bg-[var(--bg-surface-highlight)]" />
          <h2 className="text-lg font-semibold text-[var(--text-primary)]">Coming Soon</h2>
          <p className="mt-2 max-w-md text-sm text-[var(--text-secondary)]">
            Fitur AI Portfolio Builder akan tersedia di Fase 3 setelah integrasi model NeuralAlpha selesai.
          </p>
        </Card>
      </div>
    </AppShell>
  );
}
