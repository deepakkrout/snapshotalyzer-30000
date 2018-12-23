import boto3
import click



def filter_instances(project) :
        instances = []
        if project :
               filters = [{'Name':'tag:project', 'Values':[project]}]
               instances = list(ec2.instances.filter(Filters=filters))
        else :
                instances = list(ec2.instances.all())
        return instances



@click.group()
def instances ():
    """Command for instances"""
@instances.command('list')
@click.option('--project',default=None,help="Only instances for Projects will be listed <tag Project : <Name>")

def list_instances(project) :
    """List the EC2 instances"""

    instances = filter_instances(project)

    for instance in instances:
        tags = {t['Key'] : t['Value'] for t in instance.tags or [] }
        print(f"""{instance.id},{instance.instance_type},{instance.placement['AvailabilityZone']},{instance.state['Name']},{instance.public_dns_name or 'NO VALUE'},{tags.get("project","NO PROJECT TAG")}""")



@instances.command('stop')
@click.option('--project',default=None,help="Only instances for Projects will be stopped <tag Project : <Name>")
def stop_instances(project) :
    """Stopping EC2 instances"""

    instances = filter_instances(project)

    for i in instances :
        print(f"Stopping {i.id}")
        i.stop()



session = boto3.Session(profile_name ='boto3practice')
ec2 = session.resource('ec2')






if __name__ == '__main__' :
    instances()
