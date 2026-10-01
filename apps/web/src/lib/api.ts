const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function fetchJson<T>(path: string, fallback?: T): Promise<T | null> {
  try {
    const res = await fetch(`${API_BASE}${path}`, { cache: "no-store", mode: "cors" });
    if (!res.ok) return fallback ?? null;
    return (await res.json()) as T;
  } catch {
    return fallback ?? null;
  }
}

async function postJson<T>(path: string, body?: object): Promise<T | null> {
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined,
      cache: "no-store",
      mode: "cors",
    });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

export interface HealthData {
  status: string;
  service: string;
  version: string;
  timestamp: string;
}

export interface Company {
  code: string;
  name: string;
  sector?: string | null;
  sub_sector?: string | null;
  is_active: boolean;
  source: string;
}

export interface OHLCV {
  code: string;
  date: string;
  open_price: number | null;
  high_price: number | null;
  low_price: number | null;
  close_price: number | null;
  volume: number | null;
  value: number | null;
  frequency: number | null;
  source: string;
}

export interface MarketSummary {
  date?: string;
  index_code?: string;
  index_name?: string;
  open?: number;
  high?: number;
  low?: number;
  close?: number;
  change?: number;
  change_percent?: number;
  volume?: number;
  value?: number;
  message?: string;
}

export interface TopMover {
  code: string;
  date: string;
  close: number;
  volume: number;
}

export interface PortfolioResult {
  ok: boolean;
  risk_profile: string;
  portfolio: {
    code: string;
    weight: number;
    expected_return_5d: number;
    confidence: number;
  }[];
  cash_weight: number;
  expected_return_annual: number;
  volatility_annual: number;
  sharpe: number;
}

export const api = {
  health: () => fetchJson<HealthData>("/health"),
  companies: () => fetchJson<Company[]>("/companies"),
  marketSummary: () => fetchJson<MarketSummary>("/market/summary"),
  topMovers: () => fetchJson<TopMover[]>("/market/top-movers"),
  prices: (ticker: string) => fetchJson<OHLCV[]>(`/prices/${ticker}`),
  latestPrice: (ticker: string) => fetchJson<OHLCV>(`/prices/${ticker}/latest`),
  screen: (params?: Record<string, string>) => {
    const qs = params ? `?${new URLSearchParams(params).toString()}` : "";
    return fetchJson<Company[]>(`/screen${qs}`);
  },
  predict: (ticker: string) => fetchJson<Record<string, unknown>>(`/ai/predict/${ticker}`),
  buildPortfolio: (riskProfile: string) =>
    postJson<PortfolioResult>("/portfolio/build", { risk_profile: riskProfile }),
};
