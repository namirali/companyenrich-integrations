import { createAction, Property } from '@activepieces/pieces-framework';
import { companyenrichAuth, companyenrichClient } from '../common';

export const enrichCompany = createAction({
  name: 'enrich_company',
  displayName: 'Enrich Company',
  description: 'Retrieve company details by domain. Costs 1 CompanyEnrich credit per call.',
  auth: companyenrichAuth,
  props: {
    domain: Property.ShortText({ displayName: 'Domain', description: 'Company domain, for example example.com.', required: true }),
  },
  run: async (context) => companyenrichClient.request({ apiKey: context.auth.secret_text, path: '/companies/enrich', queryParams: { domain: context.propsValue.domain } }),
});
