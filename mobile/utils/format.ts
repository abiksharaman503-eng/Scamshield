export function timeAgo(value: string | number | Date): string {
  const date = new Date(value).getTime();
  if (Number.isNaN(date)) return "Unknown time";

  const seconds = Math.floor((Date.now() - date) / 1000);

  if (seconds < 60) return "Just now";

  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;

  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;

  const days = Math.floor(hours / 24);
  if (days < 30) return `${days}d ago`;

  const months = Math.floor(days / 30);
  return `${months}mo ago`;
}

export function kindLabel(kind: string): string {
  const labels: Record<string, string> = {
    url: "URL Check",
    message: "Message Check",
    screenshot: "Screenshot Check",
    account: "Account Check",
    incident: "Incident Check",
  };

  return labels[kind?.toLowerCase()] || "Security Check";
}