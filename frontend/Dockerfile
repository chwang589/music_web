FROM node:18-alpine as build-stage

WORKDIR /app

RUN npm config set registry https://registry.npmmirror.com/

COPY package*.json ./
RUN npm install

COPY . .
# 将1.png复制到public目录以便访问
RUN cp 1.png public/
RUN npm run build-only

FROM nginx:alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]