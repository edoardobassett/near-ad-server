# NEAR AD SERVER 

## Installation

The project requires [Node.js](https://nodejs.org/) v10+ to run.
Install the dependencies and start the server.

```sh
git clone https://github.com/edoardobassett/near-ad-server.git
cd near-adserver/api
npm install
node index.js
```

In another terminal :

```sh
cd near-adserver/website
npm install
npm run dev
```
Then open `http://localhost:8080` in your browser. Make sure to have Ad blockers disabled.

## Notes
The  ```recommender-flask``` folder contains the code for the recommender system python Flask API. This will not need to be installed as it is already running on a hosted server.

