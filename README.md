# polymath-host

## Setting up Firestore

Follow [Google Cloud instructions](https://cloud.google.com/firestore/docs/create-database-server-client-library) on how set up Firestore. Make sure to use `Native Mode` vs. `Datastore Mode` which is the default.

You'll need to make credentials available to local libraries. You can do this by running `gcloud auth application-default login`. This will open a browser to complete the flow, and you should only need to do it once.

Next, create configuration using [Firestore data editor](https://console.cloud.google.com/firestore/data/panel)

1. At root, create collection called `sites`.

2. For each site, create a document. The name of the document must be the first "slug" of the URL. For example, for `polymath.glazkov.com` it will be `polymath`. Don't forget to create one for local development. It will likely be called `127`, and once you setup your production version you can `Add similar document` to make it faster.

3. The document must have the following structure (name: type convention):

```
info: map
    fun_queries: array of strings
    headername: string
    placeholders: string
pinecone: map
    namespace: string
```

5. You should be ready to go.
