import { createAction, Property } from '@activepieces/pieces-framework';
import { companyenrichAuth, companyenrichClient } from '../common';

const pagination = {
  page: Property.Number({ displayName: 'Page', description: 'One-based page number. Increment to retrieve the next page.', required: false, defaultValue: 1 }),
  pageSize: Property.Number({ displayName: 'Page Size', description: 'Companies per page (1–100). Data calls consume credits per returned company.', required: false, defaultValue: 10 }),
};

export const searchCompanies = createAction({
  name: 'search_companies',
  displayName: 'Search Companies',
  description: 'Search companies by name or domain. Costs 1 credit per result, with a 1-credit minimum per request.',
  auth: companyenrichAuth,
  props: {
    query: Property.ShortText({ displayName: 'Query', description: 'Search company names and domains (1–250 characters).', required: true }),
    ...pagination,
  },
  run: async (context) => companyenrichClient.request({
    apiKey: context.auth.secret_text,
    path: '/companies/search',
    method: 'POST',
    body: { query: companyenrichClient.queryInput(context.propsValue.query), ...companyenrichClient.pageInput(context.propsValue) },
  }),
});

export const findSimilarCompanies = createAction({
  name: 'find_similar_companies',
  displayName: 'Find Similar Companies',
  description: 'Find lookalike companies from one seed domain. Costs 5 credits per result, with a 5-credit minimum per request.',
  auth: companyenrichAuth,
  props: {
    domain: Property.ShortText({ displayName: 'Seed Domain', description: 'Company domain to find lookalikes for, for example example.com.', required: true }),
    ...pagination,
  },
  run: async (context) => companyenrichClient.request({
    apiKey: context.auth.secret_text,
    path: '/companies/similar',
    method: 'POST',
    body: { domains: [context.propsValue.domain], ...companyenrichClient.pageInput(context.propsValue) },
  }),
});
