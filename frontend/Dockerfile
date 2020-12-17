FROM node:12.16.1-buster-slim AS build-stage

WORKDIR /tmp/gramps
COPY package.json yarn.lock /tmp/gramps/
RUN yarn

COPY . /tmp/gramps
RUN yarn build

FROM alpine:3.11.5 AS app

COPY --from=build-stage /tmp/gramps/dist/spa /opt/app/gramps
COPY --from=build-stage /tmp/gramps/src/assets /opt/app/gramps/assets
