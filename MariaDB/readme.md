kubectl apply -f pv.yaml
kubectl apply -f pvc.yaml
kubectl apply -f mariadb-statefulset.yaml

# Access the MariaDB pod
kubectl exec -it <pod_name> -- /bin/bash

# Connect to MariaDB using the MySQL client
mariadb -u root -p

password : root