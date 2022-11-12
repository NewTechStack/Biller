FROM node:14-buster as build-deps
WORKDIR /usr/src/app
COPY ./src/package.json ./
RUN yarn
COPY ./src/ ./
RUN yarn build

FROM nginx:1.12-alpine
COPY --from=build-deps /usr/src/app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
