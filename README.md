# ruuvimec
ruuvi sensors for MEC


## howto stuff

### clone
```
git clone https://github.com/rulex/ruuvimec.git
```

### docker build & run
```
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes # if not on aarch64
docker build --tag ruleks/ruuvi:0.1.0-aarch64 -f Dockerfile.aarch64 .
docker run --privileged --rm --net=host -t ruleks/ruuvi:0.1.0-aarch64
```

### k3s
```
kubectl apply -f ruuvi_namespace.yml
kubectl apply -f ruuvi_service.yml
kubectl apply -f ruuvi_deployment-aarch64.yml

curl <k3sMasterIp>:31111/ # get sensor data
curl <k3sMasterIp>:31111/mac # sensor macs
curl <k3sMasterIp>:31111/mac/<RuuviMac> # get sensor data for specific mac
```

