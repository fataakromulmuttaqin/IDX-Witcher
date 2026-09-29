import { Metadata } from "next";
import { Card, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { AppShell } from "@/components/layout/AppShell";
import { api, Company } from "@/lib/api";
import { mockCompanies } from "@/lib/mock-data";

export const metadata: Metadata = {
  title: "Screener — Alpha Cygni",
  description: "Filter dan temukan saham berdasarkan sektor dan kriteria lainnya.",
};

async function getCompanies(): Promise<Company[]> {
  return (await api.companies()) ?? mockCompanies;
}

export default async function ScreenerPage() {
  const companies = await getCompanies();

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
                {companies.map((c) => (
                  <tr key={c.code} className="group hover:bg-[var(--bg-surface-highlight)]/50 transition-colors">
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
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </AppShell>
  );
}
