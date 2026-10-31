import { z } from 'zod';
import { OPERATIONS } from '../dispatcher';

// Known fields retain their existing types; passthrough preserves all additional data.
export const Company = z.object({
  id: z.string(), name: z.string().nullish(), domain: z.string().nullish(),
  website: z.string().nullish(), description: z.string().nullish(), industry: z.string().nullish(),
  employees: z.string().nullish(), revenue: z.string().nullish(),
  founded_year: z.number().int().nullish(), technologies: z.array(z.string()).nullish(),
}).passthrough();
const Page = z.object({ items: z.array(Company), page: z.number().int(), totalPages: z.number().int(), totalItems: z.number().int() }).passthrough();
const object = z.record(z.string(), z.unknown());
const expand = z.array(z.string()).optional();
const filters = object.optional();
const pagination = { page: z.number().int().min(1).default(1), pageSize: z.number().int().min(1).max(100).default(10) };
export const CompanyEnrichEndpointInputSchemas = {
  enrich: z.object({ domain: z.string().trim().min(1).max(1024), expand, waitForEnrichment: z.boolean().optional() }),
  search: z.object({ query: z.string().max(250).optional(), semanticQuery: z.string().max(500).optional(), filters, expand, ...pagination }).passthrough(),
  similar: z.object({ domains: z.array(z.string().trim().min(1)).min(1).max(10), filters, expand, waitForEnrichment: z.boolean().optional(), ...pagination }).passthrough(),
  searchPeople: z.object({ query: z.string().optional(), filters, expand, ...pagination }).passthrough(),
  lookupPerson: z.object({ email: z.string().trim().min(1), expand }),
  workforce: z.object({ id: z.string().optional(), domain: z.string().optional() }),
  enrichByProperties: z.object({ properties: object, expand }),
  enrichBatch: z.object({ domains: z.array(z.string()).min(1).max(50), expand }),
  getCompany: z.object({ id: z.string(), expand }),
  getPerson: z.object({ id: z.union([z.string(), z.number()]), expand }),
  count: z.object({ query: z.string().max(250).optional(), semanticQuery: z.string().max(500).optional(), filters }).passthrough(),
  similarCount: z.object({ domains: z.array(z.string()).min(1).max(10), filters }).passthrough(),
  advanced: z.object({ operation: z.enum(Object.keys(OPERATIONS) as [string, ...string[]]), body: object.optional(), query: object.optional(), path_parameters: object.optional(), allow_beta: z.boolean().default(false) }),
  validate: z.object({}),
};
export const CompanyEnrichEndpointOutputSchemas = {
  enrich: Company, search: Page,
  similar: Page.extend({ metadata: z.object({ scores: z.record(z.string(), z.number()) }).passthrough().nullish() }),
  searchPeople: object, lookupPerson: z.unknown(), workforce: z.unknown(),
  enrichByProperties: Company, enrichBatch: z.array(z.unknown()),
  getCompany: Company, getPerson: object, count: z.number(), similarCount: z.number(), advanced: z.unknown(),
  validate: z.object({ valid: z.boolean() }),
};
export type CompanyRecord = z.infer<typeof Company>;
export type CompanyEnrichEndpointInputs = { [K in keyof typeof CompanyEnrichEndpointInputSchemas]: z.input<(typeof CompanyEnrichEndpointInputSchemas)[K]> };
export type CompanyEnrichEndpointOutputs = { [K in keyof typeof CompanyEnrichEndpointOutputSchemas]: z.infer<(typeof CompanyEnrichEndpointOutputSchemas)[K]> };
