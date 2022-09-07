FROM node:18-alpine AS build

WORKDIR /code
COPY . .
ENV VITE_MAIL_CONTACT_ERROR='fehler@beispiel.de'
ENV VITE_API_DOCS_URL='http://localhost:8000/docs'
ENV VITE_API_BASE_URL='http://localhost:8000'
ENV VITE_API_UPDATE_INTERVAL=12000
RUN npm i
RUN npm run build

FROM nginx:stable-alpine AS deploy-static

WORKDIR /usr/share/nginx/html
COPY --from=build /code/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]
