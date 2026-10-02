export const c = {
  bg: "#F7FAFC",
  card: "#FFFFFF",
  ink: "#17202A",
  muted: "#64748B",
  teal: "#0F766E",
  critical: "#DC2626",
  warning: "#D97706",
  low: "#16A34A",
  border: "#E2E8F0",
};

export const type = {
  h1: {
    fontSize: 32,
    fontWeight: "800" as const,
    color: c.ink,
  },
  h2: {
    fontSize: 20,
    fontWeight: "700" as const,
    color: c.ink,
  },
  body: {
    fontSize: 16,
    color: c.ink,
  },
  small: {
    fontSize: 14,
    color: c.muted,
  },
};
export function levelColor(level: string): string {
  switch (level?.toLowerCase()) {
    case "critical":
      return c.critical;
    case "high":
      return c.warning;
    case "medium":
      return c.warning;
    case "low":
      return c.low;
    default:
      return c.muted;
  }
}