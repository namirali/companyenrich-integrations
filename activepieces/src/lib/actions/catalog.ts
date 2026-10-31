import { createAction, Property } from '@activepieces/pieces-framework';
import { companyenrichAuth, companyenrichClient } from '../common';
import { mergeDefined, OPERATIONS, prepareOperation } from '../dispatcher';

const text = (displayName: string, required = false, description?: string) => Property.ShortText({ displayName, required, description });
const json = (displayName: string, required = false) => Property.Json({ displayName, required, description: 'A JSON object using the documented CompanyEnrich fields. Dedicated fields take precedence.' });
const pagination = {
  page: Property.Number({ displayName: 'Page', required: false, defaultValue: 1 }),
  pageSize: Property.Number({ displayName: 'Page size (1–100)', required: false, defaultValue: 10 }),
};
const expand = text('Expand', false, 'Comma-separated expansions: workforce for companies, education for people.');
const waitForEnrichment = Property.Checkbox({ displayName: 'Wait for enrichment', required: false });
function csv(value: unknown, label: string) {
  if (typeof value !== 'string') throw new Error(`${label} must be comma-separated text`);
  return value.split(',').map((v) => v.trim());
}
const specs = [
  ['enrich_company', 'Enrich Company', 'get_companies_enrich', { domain: text('Domain', true), expand, waitForEnrichment }],
  ['search_companies', 'Search Companies', 'post_companies_search', { query: text('Name/domain query (up to 250 characters)'), semanticQuery: text('Semantic query (up to 500 characters)'), filters: json('Filters'), ...pagination, expand }],
  ['find_similar_companies', 'Find Similar Companies', 'post_companies_similar', { domain: text('Seed domain (legacy)'), domains: text('Seed domains (1–10)', false, 'Comma-separated; takes precedence over the single domain.'), filters: json('Filters'), ...pagination, expand, waitForEnrichment }],
  ['search_people', 'Search People', 'post_people_search', { query: text('Name query'), filters: json('Filters'), ...pagination, expand }],
  ['lookup_person', 'Lookup Person by Email', 'post_people_lookup', { email: text('Email', true), expand }],
  ['get_workforce', 'Get Company Workforce', 'get_companies_workforce', { id: text('Company UUID'), domain: text('Domain (exactly one of ID/domain)') }],
  ['enrich_company_by_properties', 'Enrich Company by Properties', 'post_companies_enrich', { properties: json('Matching properties', true), expand }],
  ['enrich_companies_batch', 'Enrich Companies Batch', 'post_companies_enrich_batch', { domains: text('Domains (1–50)', true), expand }],
  ['get_company', 'Get Company by ID', 'get_companies', { id: text('Company UUID', true), expand }],
  ['get_person', 'Get Person by ID', 'get_people', { id: text('Person ID (decimal string)', true), expand }],
  ['count_companies', 'Count Companies', 'post_companies_search_count', { query: text('Name/domain query'), semanticQuery: text('Semantic query'), filters: json('Filters') }],
  ['count_similar_companies', 'Count Similar Companies', 'post_companies_similar_count', { domains: text('Seed domains (1–10)', true), filters: json('Filters') }],
] as const;

export const coreActions = specs.map(([name, displayName, operation, props]) => createAction({
  name, displayName, auth: companyenrichAuth,
  description: 'One CompanyEnrich API request. May consume credits. Returns the full response, including metadata. No automatic retries or pagination.',
  props,
  async run(context) {
    const p = context.propsValue as Record<string, unknown>;
    const query: Record<string, unknown> = {};
    if (p.expand) query.expand = csv(p.expand, 'expand');
    if (p.waitForEnrichment !== undefined) query.waitForEnrichment = p.waitForEnrichment;
    let body: Record<string, unknown> | undefined;
    if (OPERATIONS[operation].method === 'GET') {
      for (const key of ['id', 'domain']) if (p[key] !== undefined && p[key] !== '') query[key] = p[key];
    } else if (name === 'enrich_company_by_properties') {
      body = mergeDefined(p.properties, {});
    } else if (name === 'enrich_companies_batch') {
      body = { domains: csv(p.domains, 'domains') };
    } else if (name === 'lookup_person') {
      body = { email: p.email };
    } else {
      const dedicated: Record<string, unknown> = {};
      for (const key of ['query', 'semanticQuery']) if (p[key] !== undefined && p[key] !== '') dedicated[key] = p[key];
      if ('page' in props) Object.assign(dedicated, companyenrichClient.pageInput(p));
      if (name === 'find_similar_companies' || name === 'count_similar_companies') dedicated.domains = csv(p.domains || p.domain, 'domains');
      body = mergeDefined(p.filters, dedicated);
    }
    return companyenrichClient.send(context.auth.secret_text, prepareOperation({ operation, body, query }));
  },
}));

export const advancedOperation = createAction({
  name: 'advanced_operation', displayName: 'Advanced API Operation', auth: companyenrichAuth,
  description: 'One fixed API operation, including bulk jobs, scroll, taxonomies and explicit beta email calls. Export count is limited to 50,000. Returns job/status URLs without polling or downloading.',
  props: {
    operation: Property.StaticDropdown({ displayName: 'Operation', required: true, options: { options: Object.entries(OPERATIONS).map(([value, op]) => ({ value, label: `${op.title}${op.beta ? ' (Beta)' : ''}` })) } }),
    body: json('Body'), query: json('Query parameters'), path_parameters: json('Path parameters'),
    allow_beta: Property.Checkbox({ displayName: 'Enable beta email operations', required: false, defaultValue: false }),
  },
  async run(context) {
    return companyenrichClient.send(context.auth.secret_text, prepareOperation(context.propsValue));
  },
});
