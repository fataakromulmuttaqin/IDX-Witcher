"use client";

import { useEffect, useRef } from "react";
import {
  createChart,
  CandlestickSeries,
  ColorType,
  type IChartApi,
  type ISeriesApi,
  type CandlestickData,
  type Time,
} from "lightweight-charts";

interface PriceChartProps {
  data: { date: string; open: number; high: number; low: number; close: number; volume: number }[];
  height?: number;
}

export function PriceChart({ data, height = 400 }: PriceChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartApiRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    const chart = createChart(chartRef.current, {
      height,
      layout: {
        background: { type: ColorType.Solid, color: "transparent" },
        textColor: "var(--text-secondary)",
        fontFamily: "var(--font-geist-sans), sans-serif",
      },
      grid: {
        vertLines: { color: "rgba(30, 58, 95, 0.3)" },
        horzLines: { color: "rgba(30, 58, 95, 0.3)" },
      },
      crosshair: {
        mode: 1,
        vertLine: { color: "var(--accent-cyan)", labelBackgroundColor: "var(--accent-cyan)" },
        horzLine: { color: "var(--accent-cyan)", labelBackgroundColor: "var(--accent-cyan)" },
      },
      rightPriceScale: {
        borderColor: "var(--border-default)",
      },
      timeScale: {
        borderColor: "var(--border-default)",
        timeVisible: true,
      },
    });

    chartApiRef.current = chart;

    const series = chart.addSeries(CandlestickSeries, {
      upColor: "var(--positive)",
      downColor: "var(--negative)",
      borderUpColor: "var(--positive)",
      borderDownColor: "var(--negative)",
      wickUpColor: "var(--positive)",
      wickDownColor: "var(--negative)",
    });
    seriesRef.current = series;

    const handleResize = () => {
      if (chartRef.current) {
        chart.applyOptions({ width: chartRef.current.clientWidth, height });
      }
    };
    window.addEventListener("resize", handleResize);
    handleResize();

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
    };
  }, [height]);

  useEffect(() => {
    if (!seriesRef.current) return;
    const candleData: CandlestickData[] = data
      .slice()
      .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
      .map((d) => ({
        time: d.date as Time,
        open: d.open,
        high: d.high,
        low: d.low,
        close: d.close,
      }));
    seriesRef.current.setData(candleData);
    chartApiRef.current?.timeScale().fitContent();
  }, [data]);

  return <div ref={chartRef} className="w-full" />;
}
