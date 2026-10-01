"use client";

import { Card } from "./Card";
import { formatNumber, formatPercent } from "@/lib/format";

interface StatCardProps {
  label: string;
  value: number | string | null;
  change?: number | null;
  prefix?: string;
  suffix?: string;
  isPercent?: boolean;
  className?: string;
}

export function StatCard({
  label,
  value,
  change,
  prefix = "",
  suffix = "",
  isPercent = false,
  className,
}: StatCardProps) {
  const formatted =
    typeof value === "number"
      ? isPercent
        ? formatPercent(value)
        : `${prefix}${formatNumber(value)}${suffix}`
      : value ?? "—";

  return (
    <Card className={className}>
      <p className="text-xs font-medium uppercase tracking-wide text-[var(--text-muted)]">
        {label}
      </p>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="text-2xl font-bold tabular-nums text-[var(--text-primary)]">
          {formatted}
        </span>
        {change != null && (
          <span
            className={`text-xs font-medium tabular-nums ${
              change >= 0 ? "text-[var(--positive)]" : "text-[var(--negative)]"
            }`}
          >
            {change >= 0 ? "+" : ""}
            {change.toFixed(2)}%
          </span>
        )}
      </div>
    </Card>
  );
}
