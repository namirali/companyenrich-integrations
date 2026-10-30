import { z } from 'zod';

export const Company = z.object({
  id: z.string(), name: z.string().nullish(), domain: z.string().nullish(),
  website: z.string().nullish(), description: z.string().nullish(), industry: z.string().nullish(),
  employees: z.string().nullish(), revenue: z.string().nullish(),
  founded_year: z.number().int().nullish(), technologies: z.array(z.string()).nullish(),
});
const Page = z.object({ items: z.array(Company), page: z.number().int(), totalPages: z.number().int(), totalItems: z.number().int() });
const paginationFields = { page: z.number().int().min(1).default(1), pageSize: z.number().int().min(1).max(100).default(10) };
const inRange = (input: { page: number; pageSize: number }) => input.page * input.pageSize <= 10000;
export const CompanyEnrichEndpointInputSchemas = {
  enrich: z.object({ domain: z.string().trim().min(1).max(1024) }),
  search: z.object({ query: z.string().max(250), countries: z.array(z.string().length(2)).optional(), keywords: z.array(z.string()).optional(), ...paginationFields }).refine(inRange, 'page × pageSize must not exceed 10,000'),
  similar: z.object({ domains: z.array(z.string().trim().min(1)).min(1).max(10), ...paginationFields }).refine(inRange, 'page × pageSize must not exceed 10,000'),
  validate: z.object({}),
};
export const CompanyEnrichEndpointOutputSchemas = {
  enrich: Company,
  search: Page,
  similar: Page.extend({ metadata: z.object({ scores: z.record(z.string(), z.number()) }).nullish() }),
  validate: z.object({ valid: z.boolean() }),
};
export type CompanyRecord = z.infer<typeof Company>;
export type CompanyEnrichEndpointInputs = { [K in keyof typeof CompanyEnrichEndpointInputSchemas]: z.input<(typeof CompanyEnrichEndpointInputSchemas)[K]> };
export type CompanyEnrichEndpointOutputs = { [K in keyof typeof CompanyEnrichEndpointOutputSchemas]: z.infer<(typeof CompanyEnrichEndpointOutputSchemas)[K]> };
