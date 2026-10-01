import { Metadata } from "next";
import { api } from "@/lib/api";

import { BackendStatus } from "./BackendStatus";

export const metadata: Metadata = {
  title: "IDX Witcher — AI Portfolio & IDX Analytics",
  description: "Platform riset dan optimasi portofolio saham Indonesia berbasis AI.",
};

export default async function Home() {

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
          <a
            href="/portfolio"
            className="rounded-full border border-[var(--border-default)] bg-[var(--bg-surface-elevated)] px-8 py-3 text-sm font-semibold text-[var(--text-primary)] transition hover:border-[var(--border-hover)] hover:bg-[var(--bg-surface-highlight)]"
          >
            Portfolio Builder
          </a>
        </div>

        <div className="mt-12 rounded-2xl border border-[var(--border-default)] bg-[var(--bg-surface)] p-6 text-left shadow-lg">
          <h2 className="text-sm font-medium uppercase tracking-wide text-[var(--text-muted)]">
            Status Backend
          </h2>
          <BackendStatus />
        </div>
      </div>
    </main>
  );
}
