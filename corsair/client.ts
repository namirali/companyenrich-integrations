import type { ApiRequestOptions } from 'corsair/http';

export class CompanyEnrichAPIError extends Error {
  readonly status: number;
  readonly retryAfter?: number;
  constructor(status: number) {
    super(`CompanyEnrich request failed (HTTP ${status})`);
    this.name = 'CompanyEnrichAPIError';
    this.status = status;
  }
}

export async function sendRequest(apiKey: string, options: { url: string; method: string; body?: string }): Promise<unknown> {
  const url = new URL(options.url);
  if (url.origin !== 'https://api.companyenrich.com') throw new Error('Invalid CompanyEnrich host');
  let response: Response;
  try {
    response = await fetch(url, {
      method: options.method, body: options.body,
      headers: { Authorization: `Bearer ${apiKey}`, Accept: 'application/json', 'Content-Type': 'application/json' },
      redirect: 'error', signal: AbortSignal.timeout(30_000),
    });
  } catch {
    throw new Error('CompanyEnrich request failed or timed out. No retry was attempted.');
  }
  if (!response.ok) throw new CompanyEnrichAPIError(response.status);
  if (url.pathname === '/me') return undefined;
  try { return await response.json(); }
  catch { throw new Error('CompanyEnrich returned invalid JSON. No retry was attempted.'); }
}

export async function makeRequest(apiKey: string, options: ApiRequestOptions): Promise<unknown> {
  const url = new URL(options.url, 'https://api.companyenrich.com');
  for (const [key, value] of Object.entries(options.query ?? {})) {
    for (const item of Array.isArray(value) ? value : [value]) if (item !== undefined) url.searchParams.append(key, String(item));
  }
  return sendRequest(apiKey, { url: url.toString(), method: options.method, body: options.body === undefined ? undefined : JSON.stringify(options.body) });
}
