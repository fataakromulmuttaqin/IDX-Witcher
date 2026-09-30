"use client";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  children: React.ReactNode;
}

export function Button({
  variant = "primary",
  children,
  className = "",
  ...props
}: ButtonProps) {
  const base =
    "inline-flex items-center justify-center rounded-lg px-4 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--accent-cyan)] focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";
  const variants = {
    primary:
      "bg-gradient-to-r from-[var(--accent-cyan)] to-[var(--accent-violet)] text-[var(--bg-base)] hover:opacity-90",
    secondary:
      "border border-[var(--border-default)] bg-[var(--bg-surface-elevated)] text-[var(--text-primary)] hover:bg-[var(--bg-surface-highlight)]",
    ghost: "text-[var(--text-secondary)] hover:bg-[var(--bg-surface-highlight)]",
  };

  return (
    <button type="button" className={`${base} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}
