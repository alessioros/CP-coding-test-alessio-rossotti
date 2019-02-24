FROM nginx:alpine

LABEL Author Alessio Rossotti "alessiorossotti@gmail.com"

COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /usr/share/nginx/html
COPY dist/ .

