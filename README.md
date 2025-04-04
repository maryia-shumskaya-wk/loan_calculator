# Loan Payment Calculator

## Requirements
* Docker
* make [optional]

## How to 

### start

```shell
make up
make up-build # if you need to rebuild app
docker-compose up # if you have no make
```

### test
```shell
make test
docker-compose exec backend pytest . # if you have no make
```

### lint
```shell
make lint
# if you have no make:
docker-compose exec backend black .
docker-compose exec backend flake8 .
docker-compose exec backend isort .
```

## Project Structure
```
root
  ├ front
  | ├ src
  | | ├ assets
  | | ├ components
  | | ├ pages
  | | ├ plugins
  | | ├ services
  | | └ utils
  | └ App.vue
  ├ back
  | ├ api
  | ├ build
  | ├ common
  | ├ config
  | ├ mortgage
  | ├ tests
  | └ manage.py
  ├ Makefile
  └ docker-compose.yml
```
### Front folder
As usual contains all default files as file structure for Vue project as package.json, lock file (yarn.lock) and so on. I decided to go on with Component Driven Design to create generic components to reach reusability.
`src` folder contains:
* `assets` - with public assets such as css and so on
* `components` - with generic components to be used in future
* `pages` - page representation of views, assembled from `components`
* `plugins` - for vue plugins
* `utils` - for utilities such as validations or transformers used across code


### Back folder
A common Django structure with some adjustments:
* `api` - a package used to collect all api accoring to routing, it makes easier to maintain API (for example `/api/v1/mortgage/` route similar with import api.v1.mortgage )
* `build` - any files related with building projects, some entrypoints, Dockerfiles, configs
* `common` - package with some utilities could be used across all application (it feature could be separeted into custom library)
* `config` - default django main package
* `mortgage` - django app with model 
* `tests` - unit tests for application

## Some possible future adjustments
1. For now as on designes were no pagination. It means all data will be loaded at the moment. So sorting is provided on frontend side as default functionality of the component. But in future it should be done on API level.
2. Adjusted validation on fronted. For now frontend just ignores errors from API. Displaying errors on frontend will improve UI UX.