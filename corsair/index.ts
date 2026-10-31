import { AuthMissingError } from 'corsair/core';
import type { BindEndpoints, CorsairEndpoint, CorsairErrorHandler, CorsairPlugin, CorsairPluginContext, KeyBuilderContext, PickAuth, PluginPermissionsConfig, RequiredPluginEndpointMeta, RequiredPluginEndpointSchemas } from 'corsair/core';
import { enrich, search, similar, validate, searchPeople, lookupPerson, workforce, enrichByProperties, enrichBatch, getCompany, getPerson, count, similarCount, advanced } from './endpoints';
import { CompanyEnrichEndpointInputSchemas as inputs, CompanyEnrichEndpointOutputSchemas as outputs } from './endpoints/types';
import type { CompanyEnrichEndpointInputs, CompanyEnrichEndpointOutputs } from './endpoints/types';
import { CompanyEnrichSchema } from './schema';
import { errorHandlers } from './error-handlers';

export type CompanyEnrichPluginOptions = {
  authType?: PickAuth<'api_key'>; key?: string; persistCompanies?: boolean; hooks?: InternalCompanyEnrichPlugin['hooks'];
  errorHandlers?: CorsairErrorHandler; permissions?: PluginPermissionsConfig<typeof endpoints>;
};
export type CompanyEnrichContext = CorsairPluginContext<typeof CompanyEnrichSchema, CompanyEnrichPluginOptions>;
export type CompanyEnrichEndpoints = { [K in keyof CompanyEnrichEndpointOutputs]: CorsairEndpoint<CompanyEnrichContext, CompanyEnrichEndpointInputs[K], CompanyEnrichEndpointOutputs[K]> };
const endpoints = { companies: { enrich, search, similar, workforce, enrichByProperties, enrichBatch, get: getCompany, count, similarCount }, people: { search: searchPeople, lookup: lookupPerson, get: getPerson }, api: { advanced }, account: { validate } } as const;
export type CompanyEnrichBoundEndpoints = BindEndpoints<typeof endpoints>;
const endpointSchemas = {
  'companies.workforce': { input: inputs.workforce, output: outputs.workforce },
  'companies.enrichByProperties': { input: inputs.enrichByProperties, output: outputs.enrichByProperties },
  'companies.enrichBatch': { input: inputs.enrichBatch, output: outputs.enrichBatch },
  'companies.get': { input: inputs.getCompany, output: outputs.getCompany },
  'companies.count': { input: inputs.count, output: outputs.count },
  'companies.similarCount': { input: inputs.similarCount, output: outputs.similarCount },
  'people.search': { input: inputs.searchPeople, output: outputs.searchPeople },
  'people.lookup': { input: inputs.lookupPerson, output: outputs.lookupPerson },
  'people.get': { input: inputs.getPerson, output: outputs.getPerson },
  'api.advanced': { input: inputs.advanced, output: outputs.advanced },

  'companies.enrich': { input: inputs.enrich, output: outputs.enrich },
  'companies.search': { input: inputs.search, output: outputs.search },
  'companies.similar': { input: inputs.similar, output: outputs.similar },
  'account.validate': { input: inputs.validate, output: outputs.validate },
} as const satisfies RequiredPluginEndpointSchemas<typeof endpoints>;
const endpointMeta = {
  'companies.workforce': { riskLevel: 'read', description: 'One CompanyEnrich API operation; may consume credits. No retries or automatic pagination.' },
  'companies.enrichByProperties': { riskLevel: 'read', description: 'One CompanyEnrich API operation; may consume credits. No retries or automatic pagination.' },
  'companies.enrichBatch': { riskLevel: 'read', description: 'One CompanyEnrich API operation; may consume credits. No retries or automatic pagination.' },
  'companies.get': { riskLevel: 'read', description: 'One CompanyEnrich API operation; may consume credits. No retries or automatic pagination.' },
  'companies.count': { riskLevel: 'read', description: 'One CompanyEnrich API operation; may consume credits. No retries or automatic pagination.' },
  'companies.similarCount': { riskLevel: 'read', description: 'One CompanyEnrich API operation; may consume credits. No retries or automatic pagination.' },
  'people.search': { riskLevel: 'read', description: 'One CompanyEnrich API operation; may consume credits. No retries or automatic pagination.' },
  'people.lookup': { riskLevel: 'read', description: 'One CompanyEnrich API operation; may consume credits. No retries or automatic pagination.' },
  'people.get': { riskLevel: 'read', description: 'One CompanyEnrich API operation; may consume credits. No retries or automatic pagination.' },
  'api.advanced': { riskLevel: 'write', description: 'One CompanyEnrich API operation; may consume credits. No retries or automatic pagination.' },

  'companies.enrich': { riskLevel: 'read', description: 'Enrich a company by domain; costs 1 credit' },
  'companies.search': { riskLevel: 'read', description: 'Search one page of companies; costs 1 credit per result, 1 minimum per request' },
  'companies.similar': { riskLevel: 'read', description: 'Find one page of lookalike companies; costs 5 credits per result, 5 minimum per request' },
  'account.validate': { riskLevel: 'read', description: 'Validate the API key without consuming credits; account secrets are not returned' },
} as const satisfies RequiredPluginEndpointMeta<typeof endpoints>;
export type InternalCompanyEnrichPlugin = CorsairPlugin<'companyenrich', typeof CompanyEnrichSchema, typeof endpoints, {}, CompanyEnrichPluginOptions, 'api_key'>;

export function companyenrich(options: CompanyEnrichPluginOptions = {}): InternalCompanyEnrichPlugin {
  return {
    id: 'companyenrich', schema: CompanyEnrichSchema, options: { ...options, authType: 'api_key' },
    hooks: options.hooks, endpoints, webhooks: {}, endpointMeta, endpointSchemas,
    pluginWebhookMatcher: () => false,
    errorHandlers: { ...errorHandlers, ...options.errorHandlers },
    keyBuilder: async (ctx: KeyBuilderContext<CompanyEnrichPluginOptions>, source) => {
      if (source === 'endpoint' && options.key) return options.key;
      if (source === 'endpoint' && ctx.authType === 'api_key') {
        const key = await ctx.keys.get_api_key();
        if (key) return key;
      }
      throw new AuthMissingError('companyenrich', 'api_key');
    },
  };
}
export type { CompanyRecord, CompanyEnrichEndpointInputs, CompanyEnrichEndpointOutputs } from './endpoints/types';
