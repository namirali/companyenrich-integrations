import { PieceAuth } from '@activepieces/pieces-framework';

async function request({ apiKey, path, method = 'GET', body, queryParams }: RequestInput): Promise<unknown> {
  const url = new URL(path, 'https://api.companyenrich.com');
  for (const [key, value] of Object.entries(queryParams ?? {})) url.searchParams.set(key, value);
  return send(apiKey, {url: url.toString(), method, body: body === undefined ? undefined : JSON.stringify(body)});
}

async function send(apiKey: string, input: {url: string; method: string; body?: string}): Promise<unknown> {
  const url = new URL(input.url);
  if (url.origin !== "https://api.companyenrich.com") throw new Error("Invalid CompanyEnrich host");
  let response: Response;
  try {
    response = await fetch(url, {
      method: input.method,
      headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      body: input.body,
      signal: AbortSignal.timeout(30_000),
      redirect: 'error',
    });
  } catch {
    throw new Error('CompanyEnrich request failed or timed out. No retry was attempted.');
  }
  if (!response.ok) throw new Error(`CompanyEnrich request failed (HTTP ${response.status}).`);
  if (url.pathname === '/me') return undefined;
  try {
    return await response.json();
  } catch {
    throw new Error('CompanyEnrich returned an invalid JSON response. No retry was attempted.');
  }
}

function queryInput(query: string) {
  if (!query.trim() || query.length > 250) throw new Error('Query must contain 1 to 250 characters.');
  return query;
}

function pageInput({ page = 1, pageSize = 10 }: { page?: number; pageSize?: number }) {
  if (!Number.isInteger(page) || page < 1 || !Number.isInteger(pageSize) || pageSize < 1 || pageSize > 100 || page * pageSize > 10000) {
    throw new Error('Page must be a positive integer, page size must be 1–100, and page × page size must not exceed 10,000.');
  }
  return { page, pageSize };
}

export const companyenrichClient = { request, send, pageInput, queryInput };

export const companyenrichAuth = PieceAuth.SecretText({
  displayName: 'API Key',
  description: 'Get your API key from https://app.companyenrich.com/. Enter it without the Bearer prefix.',
  required: true,
  validate: async ({ auth }) => {
    try {
      await request({ apiKey: auth, path: '/me' });
      return { valid: true };
    } catch {
      return { valid: false, error: 'Could not validate the CompanyEnrich API key. Check the key and try again.' };
    }
  },
});

type RequestInput = {
  apiKey: string;
  path: '/me' | '/companies/enrich' | '/companies/search' | '/companies/similar';
  method?: 'GET' | 'POST';
  body?: Record<string, unknown>;
  queryParams?: Record<string, string>;
};
