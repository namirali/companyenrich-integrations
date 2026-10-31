# Privacy

The plugin sends the configured API key and the inputs required for the selected tool (company domains and matching properties, people search filters, email addresses or person IDs, pagination, and explicit bulk-job inputs) to `https://api.companyenrich.com`. It returns the API response to Dify. Credential validation sends the key to the same host's `/me` endpoint.

The plugin does not add persistent storage, analytics, logging, or third-party destinations. Dify manages the configured credential and may store workflow inputs and outputs according to the deployment's settings. CompanyEnrich processes API requests under its applicable terms and privacy policy: https://companyenrich.com/privacy-policy .

Only submit inputs you are permitted to send to CompanyEnrich. Support: https://github.com/namirali/companyenrich-integrations/issues .
