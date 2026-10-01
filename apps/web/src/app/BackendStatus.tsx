"use client";

import { useEffect, useState } from "react";

interface HealthData {
  status: string;
  service: string;
  version: string;
  timestamp: string;
}

export function BackendStatus() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    fetch(`${apiUrl}/health`, { cache: "no-store" })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => setHealth(data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="mt-3 text-sm text-[var(--text-muted)]">Memeriksa status backend...</p>;
  }

  if (!health) {
    return (
      <p className="mt-3 text-sm text-[var(--text-muted)]">
        Backend sedang offline. Pastikan FastAPI berjalan di {process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}
      </p>
    );
  }

  return (
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
  );
}
