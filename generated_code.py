 
from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB, Route53
from diagrams.aws.database import RDS, Elasticache
from diagrams.aws.storage import S3
from diagrams.aws.devtools import XRay
from diagrams.aws.integration import SQS
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import User

with Diagram("Complex Web Architecture", show=True, filename="complex_architecture_1"):

    # Internet-facing components
    dns = Route53("DNS")
    user = User("Client")
    
    # Load Balancer and Web Servers Cluster
    with Cluster("Load Balancer and Web Servers"):
        lb = ELB("Load Balancer")
        with Cluster("Web Server Auto-Scaling Group"):
            web_servers = [EC2("Web Server 1"),
                           EC2("Web Server 2"),
                           EC2("Web Server 3")]

    # Backend Services Cluster
    with Cluster("Backend Services"):
        # Database Cluster
        with Cluster("Database Layer"):
            master_db = RDS("Primary DB")
            replica_db = RDS("Replica DB")

        # Cache Cluster
        cache = Elasticache("Redis Cache")

        # Queue System
        queue = SQS("Message Queue")

    # Microservices Cluster
    with Cluster("Microservices"):
        microservices = [EC2("Service 1"),
                         EC2("Service 2"),
                         EC2("Service 3")]

    # Monitoring and Security
    monitoring = Cloudwatch("CloudWatch")
    tracing = XRay("Tracing")
    auth = IAM("Authentication")

    # Cloud Storage
    storage = S3("S3 Storage")

    # Diagram Connections
    user >> dns >> lb
    
    # Connect load balancer to each web server
    for web in web_servers:
        lb >> web

    # Web servers connecting to storage, DB, cache, queue, and microservices
    for web in web_servers:
        web >> storage
        web >> master_db
        web >> cache
        web >> queue
        for svc in microservices:
            web >> svc

    # Microservices connecting to DB, cache, and queue
    for svc in microservices:
        svc >> master_db
        svc >> cache
        svc >> queue

    # Monitoring and security connections for web servers and microservices
    for web in web_servers:
        web >> monitoring
        web >> tracing
        web >> auth

    for svc in microservices:
        svc >> monitoring
        svc >> tracing
