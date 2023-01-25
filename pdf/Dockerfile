FROM centos:7

EXPOSE 8080

RUN yum install -y epel-release && \
    yum install -y npm nodejs && \
    yum clean all
    
COPY wkhtmltox-0.12.5-1.centos7.x86_64.rpm wkhtmltox-0.12.5-1.centos7.x86_64.rpm

RUN yum localinstall wkhtmltox-0.12.5-1.centos7.x86_64.rpm -y

COPY src /src

WORKDIR /src

RUN npm install --production

CMD [ "node","app.js" ]
