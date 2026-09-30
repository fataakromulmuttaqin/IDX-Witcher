import { Metadata } from "next";
import { api } from "@/lib/api";

export const metadata: Metadata = {
  title: "IDX Witcher — AI Portfolio & IDX Analytics",
  description: "Platform riset dan optimasi portofolio saham Indonesia berbasis AI.",
};

interface HealthData {
  status: string;
  service: string;
  version: string;
  timestamp: string;
}

async function getHealth(): Promise<HealthData | null> {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    const res = await fetch(`${apiUrl}/health`, { cache: "no-store" });
    if (!res.ok) return null;
    return (await res.json()) as HealthData;
  } catch {
    return null;
  }
}

export default async function Home() {
  const health = await getHealth();

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-[var(--bg-base)] px-6">
      <div className="mx-auto max-w-3xl text-center">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-[var(--border-default)] bg-[var(--bg-surface)] px-3 py-1 text-xs font-medium text-[var(--text-secondary)]">
          <span className="h-2 w-2 rounded-full bg-[var(--accent-cyan)] animate-pulse" />
          Fase 2 — Dashboard & Screener Live
        </div>

        <h1 className="text-5xl font-extrabold tracking-tight text-[var(--text-primary)] sm:text-6xl">
          IDX <span className="text-gradient">Witcher</span>
        </h1>
        <p className="mt-6 text-lg leading-8 text-[var(--text-secondary)]">
          Platform riset & optimasi portofolio saham Indonesia berbasis AI.
          Data pasar, analitik kuantitatif, dan rekomendasi portofolio dalam
          satu dashboard.
        </p>

        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a
            href="/dashboard"
            className="rounded-full bg-gradient-to-r from-[var(--accent-cyan)] to-[var(--accent-violet)] px-8 py-3 text-sm font-semibold text-[var(--bg-base)] shadow-[0_0_24px_var(--accent-cyan-glow)] transition hover:opacity-90"
          >
            Buka Dashboard
          </a>
          <a
            href="/screener"
            className="rounded-full border border-[var(--border-default)] bg-[var(--bg-surface-elevated)] px-8 py-3 text-sm font-semibold text-[var(--text-primary)] transition hover:border-[var(--border-hover)] hover:bg-[var(--bg-surface-highlight)]"
          >
            Screener Saham
          </a>
        </div>

        <div className="mt-12 rounded-2xl border border-[var(--border-default)] bg-[var(--bg-surface)] p-6 text-left shadow-lg">
          <h2 className="text-sm font-medium uppercase tracking-wide text-[var(--text-muted)]">
            Status Backend
          </h2>
          {health ? (
            <div className="mt-3 grid gap-2 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-[var(--text-secondary)]">Service</span>
                <span className="font-medium text-[var(--text-primary)]">{health.service}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[var(--text-secondary)]">Status</span>
                <span className="inline-flex items-center gap-1.5 font-medium text-[var(--positive)]">
                  <span className="h-1.5 w-1.5 rounded-full bg-[var(--positive)]" />
                  {health.status}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[var(--text-secondary)]">Version</span>
                <span className="font-mono text-[var(--text-primary)]">{health.version}</span>
              </div>
            </div>
          ) : (
            <p className="mt-3 text-sm text-[var(--text-muted)]">
              Backend sedang offline. Pastikan FastAPI berjalan di
              http://localhost:8000
            </p>
          )}
        </div>
      </div>
    </main>
  );
}
