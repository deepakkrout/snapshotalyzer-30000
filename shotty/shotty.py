import boto3
import click


@click.command()
def list_instances() :
    """List the EC2 instances"""

    for instance in ec2.instances.all():
        print(f"""{instance.id},{instance.instance_type},{instance.placement['AvailabilityZone']},{instance.state['Name']},{instance.public_dns_name or 'NO VALUE'}""")

session = boto3.Session(profile_name ='boto3practice')
ec2 = session.resource('ec2')


if __name__ == '__main__' :
    list_instances()
