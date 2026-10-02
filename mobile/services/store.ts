export type ScanResult = Record<string, any>;

export const store: {
  result: ScanResult | null;
  incident: ScanResult | null;
  report: string | null;
} = {
  result: null,
  incident: null,
  report: null,
};