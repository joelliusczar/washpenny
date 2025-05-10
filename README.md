Interfaces to queue song paths for Moonbase59's implementation of ices0

# First time setup

cd into `dev_ops` and run script `ruby_dependency_install.sh.sh`

Next run,

`bundle update`

`bundle exec ruby './binstall.rb'`


# Set up API for testing


Need to run this so that https will work
```
wspn_dev setup_debug
```




# Ways to run api

After having installed the wspn procs file, you can run the server through
nginx
```
wspn_dev startup_api

wspn_dev setup_client

#or from inside dev_ops
# ./wspn_dev_dev startup_api
```



## VSCode debug
Use debug launch profile "Python: API"

### For client code

#### First time
`npm i`

#### Starting front end

`npm start`

# Deploying to server

## Fresh Server
```
wspn_dev deploy_install

./deploy.sh deploy_install

wspn_dev startup_api
```

## Testing new changes
If need to test a new feature, we just run`wspn_dev startup_api` while that branch
is checked out in git.
Run `wspn_dev deploy_client` to setup the client.