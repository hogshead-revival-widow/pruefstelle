FROM node:18-alpine AS build

ADD .env .env
WORKDIR /code
COPY . .
RUN npm i
RUN npm run build

FROM nginx:stable-alpine AS deploy-static

WORKDIR /usr/share/nginx/html
COPY --from=build /code/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]
