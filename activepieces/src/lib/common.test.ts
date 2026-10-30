import { afterEach, describe, expect, it, vi } from 'vitest';
import { companyenrichAuth, companyenrichClient } from './common';

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe('CompanyEnrich request boundary', () => {
  it('checks credentials without reading or returning account secrets', async () => {
    const response = new Response(JSON.stringify({ api_key: 'must-stay-private', credits: 10 }));
    const read = vi.spyOn(response, 'json');
    const send = vi.fn().mockResolvedValue(response);
    vi.stubGlobal('fetch', send);
    expect(await companyenrichAuth.validate?.({ auth: 'test-key' })).toEqual({ valid: true });
    expect(String(send.mock.calls[0][0])).toBe('https://api.companyenrich.com/me');
    expect(read).not.toHaveBeenCalled();
  });
  it('encodes domains, authenticates, bounds time, and rejects redirects', async () => {
    const send = vi.fn().mockResolvedValue(new Response('{"id":"company-1"}'));
    vi.stubGlobal('fetch', send);
    const timeout = vi.spyOn(AbortSignal, 'timeout');
    await expect(companyenrichClient.request({ apiKey: 'test-key', path: '/companies/enrich', queryParams: { domain: 'example.com&x=secret' } })).resolves.toEqual({ id: 'company-1' });
    const [url, options] = send.mock.calls[0];
    expect(url.searchParams.get('domain')).toBe('example.com&x=secret');
    expect(url.searchParams.has('x')).toBe(false);
    expect(options.headers.Authorization).toBe('Bearer test-key');
    expect(options.redirect).toBe('error');
    expect(options.signal).toBeInstanceOf(AbortSignal);
    expect(timeout).toHaveBeenCalledWith(30_000);
  });
  it.each([401, 402, 429, 500])('sanitizes HTTP %i without retrying paid requests', async (status) => {
    const send = vi.fn().mockResolvedValue(new Response('api_key=private-secret', { status }));
    vi.stubGlobal('fetch', send);
    await expect(companyenrichClient.request({ apiKey: 'test-key', path: '/companies/search', method: 'POST', body: { query: 'Acme', page: 1, pageSize: 10 } })).rejects.toThrow(`HTTP ${status}`);
    expect(send).toHaveBeenCalledTimes(1);
  });
  it('sanitizes transport errors and rejects malformed JSON without retries', async () => {
    const send = vi.fn().mockRejectedValueOnce(new Error('Authorization: Bearer leaked-key')).mockResolvedValueOnce(new Response('private-invalid-body'));
    vi.stubGlobal('fetch', send);
    await expect(companyenrichClient.request({ apiKey: 'test-key', path: '/companies/enrich' })).rejects.toThrow('CompanyEnrich request failed or timed out. No retry was attempted.');
    await expect(companyenrichClient.request({ apiKey: 'test-key', path: '/companies/enrich' })).rejects.toThrow('CompanyEnrich returned an invalid JSON response. No retry was attempted.');
    expect(send).toHaveBeenCalledTimes(2);
  });
  it('rejects over-cap pagination and oversized literal searches before a paid call', () => {
    for (const value of [{ page: 0 }, { page: 1.5 }, { pageSize: 101 }, { pageSize: 0 }, { page: 101, pageSize: 100 }]) {
      expect(() => companyenrichClient.pageInput(value)).toThrow();
    }
    expect(() => companyenrichClient.queryInput('a'.repeat(251))).toThrow();
    expect(() => companyenrichClient.queryInput('  ')).toThrow();
    expect(companyenrichClient.queryInput('a'.repeat(250))).toHaveLength(250);
    expect(companyenrichClient.pageInput({})).toEqual({ page: 1, pageSize: 10 });
    expect(companyenrichClient.pageInput({ page: 100, pageSize: 100 })).toEqual({ page: 100, pageSize: 100 });
  });
});
