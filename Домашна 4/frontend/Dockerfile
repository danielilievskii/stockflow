#FROM node:20-alpine as build
#WORKDIR /app
#ENV PATH /app/node_modules/.bin:$PATH
#COPY package.json ./
#COPY package-lock.json ./
#RUN npm ci --silent
#COPY . ./
#
#EXPOSE 3000
#CMD ["npm", "start"]

FROM node:20-alpine as build
WORKDIR /app
COPY package.json package-lock.json ./
ARG REACT_APP_BACKEND_HOST
ENV REACT_APP_BACKEND_HOST=$REACT_APP_BACKEND_HOST
RUN npm ci --silent
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]