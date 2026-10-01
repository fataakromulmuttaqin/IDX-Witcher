"use client";

import { cn } from "@/lib/format";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "default" | "positive" | "negative" | "warning" | "info";
  className?: string;
}

export function Badge({ children, variant = "default", className }: BadgeProps) {
  const variants = {
    default: "bg-[var(--bg-surface-highlight)] text-[var(--text-secondary)] border-[var(--border-default)]",
    positive: "bg-[var(--positive-dim)] text-[var(--positive)] border-[var(--positive)]/20",
    negative: "bg-[var(--negative-dim)] text-[var(--negative)] border-[var(--negative)]/20",
    warning: "bg-[var(--warning-dim)] text-[var(--warning)] border-[var(--warning)]/20",
    info: "bg-[var(--info-dim)] text-[var(--info)] border-[var(--info)]/20",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium",
        variants[variant],
        className
      )}
    >
      {children}
    </span>
  );
}
