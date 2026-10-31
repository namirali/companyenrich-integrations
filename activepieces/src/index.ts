import { createPiece } from '@activepieces/pieces-framework';
import { companyenrichAuth } from './lib/common';
import { coreActions, advancedOperation } from './lib/actions/catalog';

export const companyenrich = createPiece({
  displayName: 'CompanyEnrich',
  description: 'Enrich and discover companies and people, inspect workforce, and run explicit advanced API operations.',
  auth: companyenrichAuth,
  minimumSupportedRelease: '0.36.1',
  logoUrl: 'https://companyenrich.com/companyenrich-solo-logo.svg',
  authors: ['namirali'],
  actions: [...coreActions, advancedOperation],
  triggers: [],
});
