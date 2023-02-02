# polymath-host

## Setting up Firestore

Follow [Google Cloud instructions](https://cloud.google.com/firestore/docs/create-database-server-client-library) on how set up Firestore.

One non-obvious bit in the instructions above setting up the Service Account credentials. Service Account is the account that runs your project's instance of App Engine, and this step is necessary to reproduce the App Engine environment locally.

To get this moving, we'll need to create a Service Account key. Here's how:

1. Go to [Credentials](https://console.cloud.google.com/apis/credentials) page on Cloud console.

2. Click on the Service Account link (it will be of the form `{project-id}@appspot.gserviceaccount.com`.)

3. Select the `KEYS` tab and select `ADD KEY` -> `Create new key`. This will result in a download of a new key.

4. Move the key to someplace where you'll remember, like `./service-account-key.SECRET.json`. 

5. Run this in terminal anytime you want to run the server locally. Don't put this into `.bashrc` or `.zhrc`, since it is project-dependent. 
```shell
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key" 
```

Next, create configuration using [Firestore data editor](https://console.cloud.google.com/firestore/data/panel)

1. At root, create collection called `sites`.

2. For each site, create a document. The name of the document must be the first "slug" of the URL. For example, for `polymath.glazkov.com` it will be `polymath`. Don't forget to create one for local development. It will likely be called `127`.

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