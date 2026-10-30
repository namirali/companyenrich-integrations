import { afterEach, describe, expect, it, vi } from 'vitest';
import { createCorsair } from 'corsair/core';
import { companyenrich } from './index';

const company = { id: '550e8400-e29b-41d4-a716-446655440000', name: 'Example', domain: 'example.com', technologies: ['PostgreSQL'] };
function reply(body: object, status = 200, headers: Record<string, string> = {}) {
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', ...headers } });
}
const client = () => createCorsair({ plugins: [companyenrich({ key: 'test-key' })] });
afterEach(() => vi.unstubAllGlobals());

describe('CompanyEnrich through the Corsair client', () => {
  it('enriches a domain through the bound plugin and returns validated company fields', async () => {
    const fetch = vi.fn().mockResolvedValue(reply(company));
    vi.stubGlobal('fetch', fetch);
    const result = await client().companyenrich.api.companies.enrich({ domain: 'example.com' });
    expect(result.id).toBe(company.id);
    expect(result.technologies).toEqual(['PostgreSQL']);
    const [url, init] = fetch.mock.calls[0];
    expect(new URL(url).searchParams.get('domain')).toBe('example.com');
    expect(new Headers(init.headers).get('authorization')).toBe('Bearer test-key');
  });
  it('searches the requested page and preserves total counts', async () => {
    const fetch = vi.fn().mockResolvedValue(reply({ items: [company], page: 2, totalPages: 3, totalItems: 21 }));
    vi.stubGlobal('fetch', fetch);
    const result = await client().companyenrich.api.companies.search({ query: 'Example', page: 2, pageSize: 10 });
    expect(result.totalItems).toBe(21);
    expect(JSON.parse(fetch.mock.calls[0][1].body)).toMatchObject({ page: 2, pageSize: 10, query: 'Example' });
    expect(fetch).toHaveBeenCalledTimes(1);
  });
  it('preserves lookalike score metadata', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(reply({ items: [company], page: 1, totalPages: 1, totalItems: 1, metadata: { scores: { [company.id]: 0.9 } } })));
    const result = await client().companyenrich.api.companies.similar({ domains: ['example.com'] });
    expect(result.metadata?.scores[company.id]).toBe(0.9);
  });
  it('does not return API keys from account validation', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(reply({ apiKey: 'never-export-this', credits: 10 })));
    expect(await client().companyenrich.api.account.validate({})).toEqual({ valid: true });
  });
  it('rejects over-limit pagination before sending a request', async () => {
    const fetch = vi.fn();
    vi.stubGlobal('fetch', fetch);
    await expect(client().companyenrich.api.companies.search({ query: 'Example', page: 101, pageSize: 100 })).rejects.toThrow();
    expect(fetch).not.toHaveBeenCalled();
  });
  it('does not retry paid requests after rate-limit or server errors', async () => {
    for (const status of [402, 429, 500]) {
      const fetch = vi.fn().mockResolvedValue(reply({ detail: 'provider error' }, status, { 'Retry-After': '1' }));
      vi.stubGlobal('fetch', fetch);
      await expect(client().companyenrich.api.companies.enrich({ domain: 'example.com' })).rejects.toThrow();
      expect(fetch).toHaveBeenCalledTimes(1);
    }
  });
});

describe('CompanyEnrich invalid credentials and responses', () => {
  it('does not send a request without a configured key', async () => {
    const fetch = vi.fn();
    vi.stubGlobal('fetch', fetch);
    const unauthenticated = createCorsair({ plugins: [companyenrich()] });
    await expect(unauthenticated.companyenrich.api.account.validate({})).rejects.toThrow();
    expect(fetch).not.toHaveBeenCalled();
  });
  it('rejects a successful response that lacks a company identifier', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(reply({ name: 'Incomplete record' })));
    await expect(client().companyenrich.api.companies.enrich({ domain: 'example.com' })).rejects.toThrow();
  });
});
