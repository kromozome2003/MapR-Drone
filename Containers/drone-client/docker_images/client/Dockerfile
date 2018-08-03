FROM ubuntu:16.04

ENV container docker

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update -qq && apt-get install --no-install-recommends -q -y curl sudo tzdata wget apt-utils dnsutils file iputils-ping net-tools nfs-common openssl syslinux sysv-rc-conf libssl1.0.0 openjdk-8-jdk && apt-get autoremove --purge -q -y && rm -rf /var/lib/apt/lists/* && apt-get clean -q

LABEL mapr.os=ubuntu16 mapr.version=6.0.1 mapr.mep_version=5.0.0

COPY mapr-setup.sh /opt/mapr/installer/docker/

RUN /opt/mapr/installer/docker/mapr-setup.sh -r http://package.mapr.com/releases container client 6.0.1 5.0.0 mapr-client mapr-posix-client-container mapr-kafka mapr-librdkafka

ENTRYPOINT ["/opt/mapr/installer/docker/mapr-setup.sh", "container"]
