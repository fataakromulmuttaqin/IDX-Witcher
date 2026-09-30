"use client";

import { useState } from "react";
import { cn } from "@/lib/format";

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
}

const navItems: NavItem[] = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: (
      <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25c0 1.242 1.007 2.25 2.25 2.25h6.75M3.75 3h16.5M3.75 3l7.013 7.013M20.25 3v11.25c0 1.242-1.007 2.25-2.25 2.25h-6.75M20.25 3l-7.013 7.013M3.75 21h16.5" />
      </svg>
    ),
  },
  {
    label: "Screener",
    href: "/screener",
    icon: (
      <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.139 5.139a2.25 2.25 0 00-.659 1.591v8.538a2.25 2.25 0 01-3.375 1.968l-3.026-1.757a2.25 2.25 0 01-1.125-1.952v-6.75a2.25 2.25 0 00-.659-1.591L2.659 7.409A2.25 2.25 0 012 5.818V4.774c0-.54.384-1.006.917-1.096A49.738 49.738 0 0112 3z" />
      </svg>
    ),
  },
  {
    label: "Signals",
    href: "/signals",
    icon: (
      <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L18.75 21H3.75l2.25-7.5z" />
      </svg>
    ),
  },
  {
    label: "Portfolio",
    href: "/portfolio",
    icon: (
      <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.91 11.91 0 005.596-3.042l.963-.963a.75.75 0 011.073 0l.963.963a11.91 11.91 0 005.596 3.042l.327.327" />
      </svg>
    ),
  },
];

export function Sidebar() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setMobileOpen(!mobileOpen)}
        className="fixed left-4 top-4 z-50 rounded-md border border-[var(--border-default)] bg-[var(--bg-surface)] p-2 text-[var(--text-secondary)] lg:hidden"
      >
        <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
        </svg>
      </button>

      <aside
        className={cn(
          "fixed left-0 top-0 z-40 h-screen w-64 border-r border-[var(--border-default)] bg-[var(--bg-surface)] transition-transform duration-300",
          mobileOpen ? "translate-x-0" : "-translate-x-full",
          "lg:translate-x-0"
        )}
      >
        <div className="flex h-full flex-col">
          <div className="flex items-center gap-3 border-b border-[var(--border-default)] px-6 py-5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-[var(--accent-cyan)] to-[var(--accent-violet)] text-[var(--bg-base)] font-bold">
              N
            </div>
            <div>
              <span className="text-lg font-bold tracking-tight text-[var(--text-primary)]">IDX Witcher</span>
            </div>
          </div>

          <nav className="flex-1 space-y-1 p-4">
            {navItems.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-[var(--text-secondary)] transition-colors hover:bg-[var(--bg-surface-highlight)] hover:text-[var(--text-primary)]"
              >
                <span className="text-[var(--text-muted)] group-hover:text-[var(--accent-cyan)] transition-colors">
                  {item.icon}
                </span>
                {item.label}
              </a>
            ))}
          </nav>

          <div className="border-t border-[var(--border-default)] p-4">
            <div className="rounded-lg border border-[var(--border-default)] bg-[var(--bg-surface-highlight)] p-3">
              <p className="text-xs text-[var(--text-muted)]">Data source</p>
              <div className="mt-1 flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-[var(--accent-cyan)] animate-pulse" />
                <span className="text-xs font-medium text-[var(--text-primary)]">Yahoo Finance + IDX</span>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {mobileOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}
    </>
  );
}
