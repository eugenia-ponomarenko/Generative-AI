# K8s
All manifest files are stored in:
- deployment.yml
- serviceAccount.yml
- lb-service.yml
- namespace.yml
- autoscaler.yml
- configMap.yml
- podDisruptionBudget.yml

# AWS
1. Created an IAM role for the EKS cluster with the following permissions:
   - AmazonEC2ContainerRegistryReadOnly
   - AmazonEKSClusterPolicy	
   - AmazonEKSWorkerNodePolicy
3. Created EKS cluster with default VPC and default subnets
4. Connected to the cluster from AWS Shell Console and apply all k8s manifests
5. Faced the issue that pods stay in Pending status and then observed nodes weren't created
6. Tried to create a Fargate Profile but couldn't create a private subnet (that's weird)
7. Then created Node Group:
   1. Created IAM Role with the permission as below:
      - AmazonEC2ContainerRegistryReadOnly
      - AmazonEKSClusterPolicy	
      - AmazonEKSWorkerNodePolicy
   2. Other configs were the default ones
   3. Desired capacity - 2
   4. Create two subnets in different AZs with enabled auto-assigning public IPv4 address
   5. Created Node Group and got the error that instances weren't able to join the cluster

EKS Managed Node Groups weren't created and worker nodes as well stopped the process of deployment. And it wasn't resolved so the task wasn't completed.
