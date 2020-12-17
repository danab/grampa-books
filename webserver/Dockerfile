FROM nginx:1.17.9-alpine

# COPY ./ssl /etc/ssl
COPY ./conf.d /etc/nginx/conf.d

EXPOSE 80 80
CMD ["nginx", "-g", "daemon off;"]
