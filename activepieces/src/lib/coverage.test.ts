import { afterEach, expect, it, vi } from 'vitest';
import { companyenrich } from '../index';
import fixtures from './route-fixtures.json';

const actions = companyenrich.actions();
const run = (name: string, propsValue: object) => actions[name].run({ auth: { secret_text: 'test-key' }, propsValue } as never);
afterEach(() => vi.unstubAllGlobals());
const cases = [
  ['enrich_company', { domain: 'example.com' }, '/companies/enrich', 'GET'],
  ['search_companies', { query: 'Example' }, '/companies/search', 'POST'],
  ['find_similar_companies', { domain: 'example.com' }, '/companies/similar', 'POST'],
  ['search_people', { query: 'Sam' }, '/people/search', 'POST'],
  ['lookup_person', { email: 'sam@example.com' }, '/people/lookup', 'POST'],
  ['get_workforce', { domain: 'example.com' }, '/companies/workforce', 'GET'],
  ['enrich_company_by_properties', { properties: { name: 'Example' } }, '/companies/enrich', 'POST'],
  ['enrich_companies_batch', { domains: 'example.com,example.org' }, '/companies/enrich/batch', 'POST'],
  ['get_company', { id: '550e8400-e29b-41d4-a716-446655440000' }, '/companies', 'GET'],
  ['get_person', { id: '9223372036854775807' }, '/people', 'GET'],
  ['count_companies', { query: 'Example' }, '/companies/search/count', 'POST'],
  ['count_similar_companies', { domains: 'example.com' }, '/companies/similar/count', 'POST'],
] as const;
it.each(cases)('registered action %s routes and preserves response', async (name, props, path, method) => {
  const data = name.startsWith('count') ? 0 : name === 'enrich_companies_batch' ? [{ future: { signals: [1] } }] : { future: { signals: [1] }, metadata: { scores: { id: 0.8 } } };
  const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify(data))); vi.stubGlobal('fetch', fetch);
  expect(await run(name, props)).toEqual(data);
  const [url, init] = fetch.mock.calls[0];
  expect(new URL(url).pathname).toBe(path); expect(init.method).toBe(method); expect(init.redirect).toBe('error');
  expect(fetch).toHaveBeenCalledTimes(1);
});
it.each(fixtures)('advanced dispatch $input.operation', async ({input, method, path}) => {
  const fetch = vi.fn().mockResolvedValue(new Response('0')); vi.stubGlobal('fetch', fetch);
  expect(await run('advanced_operation', input)).toBe(0);
  const [url, init] = fetch.mock.calls[0]; expect(new URL(url).pathname).toBe(path); expect(init.method).toBe(method); expect(fetch).toHaveBeenCalledTimes(1);
});
it('forwards filters, multi-seeds, expansions and metadata', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{}')); vi.stubGlobal('fetch', fetch);
  await run('find_similar_companies', { domains: 'example.com,example.org', filters: { countries: ['US'], futureFilter: { x: true } }, expand: 'workforce', waitForEnrichment: false });
  const [url, init] = fetch.mock.calls[0];
  expect(JSON.parse(init.body)).toMatchObject({ domains: ['example.com', 'example.org'], countries: ['US'], futureFilter: { x: true } });
  expect(new URL(url).searchParams.get('expand')).toBe('workforce'); expect(new URL(url).searchParams.get('waitForEnrichment')).toBe('false');
});
it.each([
  {operation:'get_people_email',query:{id:'42'}}, {operation:'get_me'}, {operation:'get_companies_workforce',query:{}},
  {operation:'post_companies_enrich_batch',body:{domains:[]}}, {operation:'post_people_search',body:{page:true}},
  {operation:'post_companies_search_async',body:{count:50001}}, {operation:'get_people',query:{id:9007199254740992}},
  {operation:'post_companies_search',body:{page:1001}}, {operation:'get_companies_enrich',query:{domain:'example.com',host:'elsewhere'}},
])('invalid advanced input makes no request', async (input) => {
  const fetch = vi.fn(); vi.stubGlobal('fetch', fetch); await expect(run('advanced_operation', input)).rejects.toThrow(); expect(fetch).not.toHaveBeenCalled();
});
it('registers all twelve core actions and the advanced selector', () => expect(Object.keys(actions)).toHaveLength(13));

it('preserves exact beta person IDs without changing unknown metadata strings', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{}')); vi.stubGlobal('fetch', fetch);
  await run('advanced_operation', {operation:'post_people_email_bulk', allow_beta:true, body:{items:[{person_id:'9223372036854775807'}], metadata:{person_id:'9223372036854775807'}}});
  const body = fetch.mock.calls[0][1].body;
  expect(body).toContain('"person_id":9223372036854775807');
  expect(JSON.parse(body).metadata.person_id).toBe('9223372036854775807');
});
it.each([
  {operation:'post_companies_search_async',body:{count:1,similar:{}}},
  {operation:'post_companies_search',body:{future:{bad:NaN}}},
])('rejects malformed nested inputs before HTTP', async (input) => {
  const fetch = vi.fn(); vi.stubGlobal('fetch', fetch); await expect(run('advanced_operation', input)).rejects.toThrow(); expect(fetch).not.toHaveBeenCalled();
});
it('sanitizes network errors on advanced calls', async () => {
  const fetch = vi.fn().mockRejectedValue(new Error('Bearer private-secret')); vi.stubGlobal('fetch', fetch);
  await expect(run('advanced_operation', {operation:'post_companies_search',body:{}})).rejects.toThrow('CompanyEnrich request failed or timed out. No retry was attempted.');
  expect(fetch).toHaveBeenCalledTimes(1);
});

it('bounds an omitted scroll page size without requesting another cursor', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{"nextCursor":"next"}')); vi.stubGlobal('fetch', fetch);
  expect(await run('advanced_operation', {operation:'post_people_search_scroll',body:{}})).toEqual({nextCursor:'next'});
  expect(JSON.parse(fetch.mock.calls[0][1].body).pageSize).toBe(10); expect(fetch).toHaveBeenCalledTimes(1);
});
