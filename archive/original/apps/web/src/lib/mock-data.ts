import { Company, MarketSummary, OHLCV, TopMover } from "./api";

export const mockCompanies: Company[] = [
  { code: "BBCA", name: "Bank Central Asia", sector: "Financials", is_active: true, source: "seed" },
  { code: "BBRI", name: "Bank Rakyat Indonesia", sector: "Financials", is_active: true, source: "seed" },
  { code: "BMRI", name: "Bank Mandiri", sector: "Financials", is_active: true, source: "seed" },
  { code: "TLKM", name: "Telkom Indonesia", sector: "Technology", is_active: true, source: "seed" },
  { code: "ASII", name: "Astra International", sector: "Consumer", is_active: true, source: "seed" },
  { code: "INDF", name: "Indofood Sukses Makmur", sector: "Consumer", is_active: true, source: "seed" },
  { code: "UNVR", name: "Unilever Indonesia", sector: "Consumer", is_active: true, source: "seed" },
  { code: "PGAS", name: "Perusahaan Gas Negara", sector: "Energy", is_active: true, source: "seed" },
  { code: "ANTM", name: "Aneka Tambang", sector: "Materials", is_active: true, source: "seed" },
  { code: "PTBA", name: "Bukit Asam", sector: "Energy", is_active: true, source: "seed" },
];

export const mockMarketSummary: MarketSummary = {
  date: new Date().toISOString(),
  index_code: "^JKSE",
  index_name: "IHSG",
  open: 7250.25,
  high: 7390.5,
  low: 7210.15,
  close: 7365.4,
  change: 115.15,
  change_percent: 1.58,
  volume: 12500000000,
  value: 12500000000000,
};

export const mockTopMovers: TopMover[] = [
  { code: "BBCA", date: "2026-09-29", close: 9750, volume: 12500000 },
  { code: "BBRI", date: "2026-09-29", close: 4320, volume: 9800000 },
  { code: "TLKM", date: "2026-09-29", close: 3780, volume: 8200000 },
  { code: "ASII", date: "2026-09-29", close: 5600, volume: 6500000 },
  { code: "INDF", date: "2026-09-29", close: 7250, volume: 5100000 },
];

export function generateMockOHLCV(ticker: string): OHLCV[] {
  const data: OHLCV[] = [];
  let price = 5000;
  const now = new Date();
  for (let i = 90; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    const change = (Math.random() - 0.5) * 100;
    const open = price;
    price = Math.max(3000, price + change);
    const close = price;
    const high = Math.max(open, close) + Math.random() * 30;
    const low = Math.min(open, close) - Math.random() * 30;
    data.push({
      code: ticker,
      date: date.toISOString().split("T")[0],
      open_price: parseFloat(open.toFixed(2)),
      high_price: parseFloat(high.toFixed(2)),
      low_price: parseFloat(low.toFixed(2)),
      close_price: parseFloat(close.toFixed(2)),
      volume: Math.floor(Math.random() * 5000000) + 1000000,
      value: Math.floor(Math.random() * 50000000000),
      frequency: Math.floor(Math.random() * 10000),
      source: "mock",
    });
  }
  return data;
}
