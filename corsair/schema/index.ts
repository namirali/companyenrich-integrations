import { z } from 'zod';
import { Company } from '../endpoints/types';

export const CompanyEnrichSchema = {
  version: '1.0.0',
  entities: { companies: Company.extend({ refreshedAt: z.date() }) },
} as const;
