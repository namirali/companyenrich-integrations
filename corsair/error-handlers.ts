import type { CorsairErrorHandler } from 'corsair/core';
import { CompanyEnrichAPIError } from './client';

export const errorHandlers = {
  RATE_LIMIT_ERROR: {
    match: (error: Error) => error instanceof CompanyEnrichAPIError && error.status === 429,
    handler: async (error: Error) => ({ maxRetries: 0, headersRetryAfterMs: error instanceof CompanyEnrichAPIError ? error.retryAfter : undefined }),
  },
  DEFAULT: { match: () => true, handler: async () => ({ maxRetries: 0 }) },
} satisfies CorsairErrorHandler;
