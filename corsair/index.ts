import { AuthMissingError } from 'corsair/core';
import type { BindEndpoints, CorsairEndpoint, CorsairErrorHandler, CorsairPlugin, CorsairPluginContext, KeyBuilderContext, PickAuth, PluginPermissionsConfig, RequiredPluginEndpointMeta, RequiredPluginEndpointSchemas } from 'corsair/core';
import { enrich, search, similar, validate } from './endpoints';
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
const endpoints = { companies: { enrich, search, similar }, account: { validate } } as const;
export type CompanyEnrichBoundEndpoints = BindEndpoints<typeof endpoints>;
const endpointSchemas = {
  'companies.enrich': { input: inputs.enrich, output: outputs.enrich },
  'companies.search': { input: inputs.search, output: outputs.search },
  'companies.similar': { input: inputs.similar, output: outputs.similar },
  'account.validate': { input: inputs.validate, output: outputs.validate },
} as const satisfies RequiredPluginEndpointSchemas<typeof endpoints>;
const endpointMeta = {
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
