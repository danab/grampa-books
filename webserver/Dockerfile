FROM nginx:1.17.9-alpine

# COPY ./ssl /etc/ssl
COPY ./conf.d /etc/nginx/conf.d

EXPOSE 80 8080
CMD ["nginx", "-g", "daemon off;"]
