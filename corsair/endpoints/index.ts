import type { CompanyEnrichContext, CompanyEnrichEndpoints } from '../index';
import { makeRequest } from '../client';
import { CompanyEnrichEndpointInputSchemas as inputs, CompanyEnrichEndpointOutputSchemas as outputs } from './types';
import type { CompanyRecord } from './types';

async function save(ctx: CompanyEnrichContext, companies: CompanyRecord[]) {
  if (!ctx.options.persistCompanies) return;
  for (const company of companies) {
    await ctx.db.companies.upsertByEntityId(company.id, { ...company, refreshedAt: new Date() });
  }
}

export const enrich: CompanyEnrichEndpoints['enrich'] = async (ctx, input) => {
  const query = inputs.enrich.parse(input);
  const result = outputs.enrich.parse(await makeRequest(ctx.key, { method: 'GET', url: '/companies/enrich', query }));
  await save(ctx, [result]);
  return result;
};
export const search: CompanyEnrichEndpoints['search'] = async (ctx, input) => {
  const body = inputs.search.parse(input);
  const result = outputs.search.parse(await makeRequest(ctx.key, { method: 'POST', url: '/companies/search', body, mediaType: 'application/json' }));
  await save(ctx, result.items);
  return result;
};
export const similar: CompanyEnrichEndpoints['similar'] = async (ctx, input) => {
  const body = inputs.similar.parse(input);
  const result = outputs.similar.parse(await makeRequest(ctx.key, { method: 'POST', url: '/companies/similar', body, mediaType: 'application/json' }));
  await save(ctx, result.items);
  return result;
};
export const validate: CompanyEnrichEndpoints['validate'] = async (ctx, input) => {
  inputs.validate.parse(input);
  await makeRequest(ctx.key, { method: 'GET', url: '/me' });
  return outputs.validate.parse({ valid: true });
};
