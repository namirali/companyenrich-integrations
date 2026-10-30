import { ApiError, request } from 'corsair/http';
import type { ApiRequestOptions, OpenAPIConfig } from 'corsair/http';

export class CompanyEnrichAPIError extends Error {
  readonly status: number;
  readonly retryAfter?: number;
  constructor(error: ApiError) {
    super(`CompanyEnrich request failed (HTTP ${error.status})`);
    this.name = 'CompanyEnrichAPIError';
    this.status = error.status;
    this.retryAfter = error.retryAfter;
  }
}

export async function makeRequest(apiKey: string, options: ApiRequestOptions): Promise<unknown> {
  const config: OpenAPIConfig = {
    BASE: 'https://api.companyenrich.com', VERSION: '1', WITH_CREDENTIALS: false, CREDENTIALS: 'omit',
    HEADERS: { Authorization: `Bearer ${apiKey}`, Accept: 'application/json' },
  };
  try {
    return await request<unknown>(config, options, {
      rateLimitConfig: { enabled: true, maxRetries: 0, initialRetryDelay: 1000, backoffMultiplier: 2, headerNames: { retryAfter: 'retry-after' } },
    });
  } catch (error) {
    if (error instanceof ApiError) throw new CompanyEnrichAPIError(error);
    throw error;
  }
}
