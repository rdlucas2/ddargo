# Setup ArgoCD with docker desktop

## nginx ingress setup

### 1. add the ingress
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.2/deploy/static/provider/cloud/deploy.yaml
```

### 2. test a simple example:
```bash
kubectl create deployment demo --image=httpd --port=80

kubectl expose deployment demo

kubectl create ingress demo-localhost --class=nginx \
  --rule="demo.localdev.me/*=demo:80"
```

### 3. remove the demo application by running delete commands

## Install argocd cli

### 1. You can download the latest stable release by executing below steps:
```bash
VERSION=$(curl -L -s https://raw.githubusercontent.com/argoproj/argo-cd/stable/VERSION)
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/download/v$VERSION/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64
```

## ArgoCD setup

### 1. Enable kubernetes in Docker Desktop

### 2. Create namespace 
```bash
kubectl create namespace argocd
```

### 3. Install ArgoCD Resources: 
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`
```

### 4. allow insecure (not for production usage):
```bash
 kubectl patch deployment argocd-server -n argocd   --type='json' -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--insecure"}]'
 ```

### 5. Add to ingress:
```bash
kubectl create ingress argocd-localhost --class=nginx --rule="argo.localdev.me/*=argocd-server:80" -n argocd
```

### 6. Get the password to login with admin user
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

### 7. Login at argo.localdev.me

### 8. Login with argocd cli
```bash
argocd login argo.localdev.me
```

### 9. register docker-desktop cluster
```bash
argocd cluster add docker-desktop
```

## Adding Repositories and Apps

### 1. make a github app: 
- make a new app here: `https://github.com/settings/apps/new`
- create a private key to be used in next step (and add *.pem to your .gitignore)

### 2. add the repo:
- replace app id, installation id, and the pem with your own values
```
argocd repo add https://git.example.com/repos/repo --github-app-id 1 --github-app-installation-id 2 --github-app-private-key-path test.private-key.pem
```

### 3. adding the app of apps:
argocd app create bootstrap-example --dest-namespace argocd --dest-server https://kubernetes.default.svc --repo https://github.com/rdlucas2/ddargo.git --path argo/bootstrap-example

## TODO:
- create an argo app, k8s manifests or helm chart, create a simple app and host on dockerhub
- write a script for complete setup

### References:
- https://kubernetes.github.io/ingress-nginx/deploy/#quick-start
- https://argo-cd.readthedocs.io/en/stable/cli_installation/
- https://collabnix.com/getting-started-with-argocd-on-docker-desktop/
- https://argo-cd.readthedocs.io/en/release-2.10/user-guide/commands/argocd_repo_add/
- https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/
