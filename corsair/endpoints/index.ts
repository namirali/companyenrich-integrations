import type { CompanyEnrichContext, CompanyEnrichEndpoints } from '../index';
import { makeRequest, sendRequest } from '../client';
import { mergeDefined, OPERATIONS, prepareOperation } from '../dispatcher';
import { CompanyEnrichEndpointInputSchemas as inputs, CompanyEnrichEndpointOutputSchemas as outputs } from './types';
import type { CompanyRecord } from './types';

async function save(ctx: CompanyEnrichContext, companies: CompanyRecord[]) {
  if (!ctx.options.persistCompanies) return;
  for (const company of companies) await ctx.db.companies.upsertByEntityId(company.id, { ...company, refreshedAt: new Date() });
}
function endpoint<K extends Exclude<keyof CompanyEnrichEndpoints, 'advanced' | 'validate'>>(key: K, operation: string): CompanyEnrichEndpoints[K] {
  return (async (ctx: CompanyEnrichContext, input: unknown) => {
    const p = inputs[key].parse(input) as Record<string, unknown>;
    const { expand, waitForEnrichment, filters, properties, ...dedicated } = p;
    const query: Record<string, unknown> = {};
    if (expand !== undefined) query.expand = expand;
    if (waitForEnrichment !== undefined) query.waitForEnrichment = waitForEnrichment;
    let body: Record<string, unknown> | undefined;
    if (OPERATIONS[operation].method === 'GET') Object.assign(query, dedicated);
    else body = properties ? mergeDefined(properties, {}) : mergeDefined(filters, dedicated);
    const result = outputs[key].parse(await sendRequest(ctx.key, prepareOperation({ operation, body, query })));
    if (key === 'enrich' || key === 'enrichByProperties' || key === 'getCompany') await save(ctx, [result as CompanyRecord]);
    if (key === 'search' || key === 'similar') await save(ctx, (result as { items: CompanyRecord[] }).items);
    return result;
  }) as CompanyEnrichEndpoints[K];
}
export const enrich = endpoint('enrich', 'get_companies_enrich');
export const search = endpoint('search', 'post_companies_search');
export const similar = endpoint('similar', 'post_companies_similar');
export const searchPeople = endpoint('searchPeople', 'post_people_search');
export const lookupPerson = endpoint('lookupPerson', 'post_people_lookup');
export const workforce = endpoint('workforce', 'get_companies_workforce');
export const enrichByProperties = endpoint('enrichByProperties', 'post_companies_enrich');
export const enrichBatch = endpoint('enrichBatch', 'post_companies_enrich_batch');
export const getCompany = endpoint('getCompany', 'get_companies');
export const getPerson = endpoint('getPerson', 'get_people');
export const count = endpoint('count', 'post_companies_search_count');
export const similarCount = endpoint('similarCount', 'post_companies_similar_count');
export const advanced: CompanyEnrichEndpoints['advanced'] = async (ctx, input) => sendRequest(ctx.key, prepareOperation(inputs.advanced.parse(input)));
export const validate: CompanyEnrichEndpoints['validate'] = async (ctx, input) => {
  inputs.validate.parse(input);
  await makeRequest(ctx.key, { method: 'GET', url: '/me' });
  return { valid: true };
};
