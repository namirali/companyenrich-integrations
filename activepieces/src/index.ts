import { createPiece } from '@activepieces/pieces-framework';
import { companyenrichAuth } from './lib/common';
import { enrichCompany } from './lib/actions/enrich-company';
import { searchCompanies, findSimilarCompanies } from './lib/actions/discover-companies';

export const companyenrich = createPiece({
  displayName: 'CompanyEnrich',
  description: 'Enrich companies by domain, search company profiles, and find similar companies.',
  auth: companyenrichAuth,
  minimumSupportedRelease: '0.36.1',
  logoUrl: 'https://companyenrich.com/companyenrich-solo-logo.svg',
  authors: ['namirali'],
  actions: [enrichCompany, searchCompanies, findSimilarCompanies],
  triggers: [],
});
