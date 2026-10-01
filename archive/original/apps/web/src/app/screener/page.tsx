"use client";

import { useEffect, useState } from "react";
import { Card, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { AppShell } from "@/components/layout/AppShell";
import { api, Company } from "@/lib/api";
import { mockCompanies } from "@/lib/mock-data";

export default function ScreenerPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [sector, setSector] = useState<string>("");
  const [query, setQuery] = useState<string>("");

  useEffect(() => {
    setLoading(true);
    api
      .companies()
      .then((data) => {
        setCompanies(data ?? mockCompanies);
      })
      .finally(() => setLoading(false));
  }, []);

  const sectors = Array.from(new Set(companies.map((c) => c.sector).filter((s): s is string => Boolean(s))));

  const filtered = companies.filter((c) => {
    const matchSector = sector ? c.sector?.toLowerCase() === sector.toLowerCase() : true;
    const q = query.toLowerCase();
    const matchQuery =
      !q || c.code.toLowerCase().includes(q) || c.name.toLowerCase().includes(q);
    return matchSector && matchQuery;
  });

  return (
    <AppShell>
      <div className="mx-auto max-w-7xl space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--text-primary)]">
            Screener
          </h1>
          <p className="mt-1 text-sm text-[var(--text-secondary)]">
            Temukan saham berdasarkan sektor dan kriteria fundamental.
          </p>
        </div>

        <Card className="flex flex-col gap-4 p-4 sm:flex-row sm:items-end">
          <div className="flex-1">
            <label className="block text-xs font-medium text-[var(--text-muted)]">
              Cari saham
            </label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Kode atau nama saham"
              className="mt-1 w-full rounded-lg border border-[var(--border-default)] bg-[var(--bg-surface)] px-3 py-2 text-sm text-[var(--text-primary)] outline-none focus:border-[var(--accent-cyan)]"
            />
          </div>
          <div className="flex-1">
            <label className="block text-xs font-medium text-[var(--text-muted)]">Sektor</label>
            <select
              value={sector}
              onChange={(e) => setSector(e.target.value)}
              className="mt-1 w-full rounded-lg border border-[var(--border-default)] bg-[var(--bg-surface)] px-3 py-2 text-sm text-[var(--text-primary)] outline-none focus:border-[var(--accent-cyan)]"
            >
              <option value="">Semua sektor</option>
              {sectors.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
        </Card>

        <Card>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-[var(--border-default)] text-xs uppercase tracking-wider text-[var(--text-muted)]">
                  <th className="pb-3 pl-2 font-medium">Code</th>
                  <th className="pb-3 font-medium">Name</th>
                  <th className="pb-3 font-medium">Sector</th>
                  <th className="pb-3 font-medium">Status</th>
                  <th className="pb-3 font-medium">Source</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--border-subtle)]">
                {loading ? (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-[var(--text-muted)]">
                      Loading...
                    </td>
                  </tr>
                ) : filtered.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-[var(--text-muted)]">
                      Tidak ada saham yang cocok.
                    </td>
                  </tr>
                ) : (
                  filtered.map((c) => (
                    <tr
                      key={c.code}
                      className="group hover:bg-[var(--bg-surface-highlight)]/50 transition-colors"
                    >
                      <td className="py-4 pl-2">
                        <a
                          href={`/stocks/${c.code}`}
                          className="font-bold tabular-nums text-[var(--text-primary)] group-hover:text-[var(--accent-cyan)] transition-colors"
                        >
                          {c.code}
                        </a>
                      </td>
                      <td className="py-4 text-[var(--text-secondary)]">{c.name}</td>
                      <td className="py-4 text-[var(--text-secondary)]">{c.sector ?? "—"}</td>
                      <td className="py-4">
                        <Badge variant={c.is_active ? "positive" : "default"}>
                          {c.is_active ? "Active" : "Inactive"}
                        </Badge>
                      </td>
                      <td className="py-4 text-[var(--text-muted)]">{c.source}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </AppShell>
  );
}
