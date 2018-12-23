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

@click.group('cli')
def cli():
    """Shotty mangement CLI script"""

@cli.group('volumes')
def volumes():
    """Command for Volumes"""

@volumes.command('list')
@click.option('--project',default=None,help="Only volumes for Projects will be listed <tag Project : <Name>")
def list_volumes(project):
    instances = filter_instances(project)
    for instance in instances :
        for volume in instance.volumes.all():
            print(f"""{volume.id} , {instance.id} , {volume.state}, {volume.size}GiB, {volume.encrypted and "Encrypted" or "Not Encrypted"} """)

@cli.group('snapshots')
def snapshots():
    """Command for Snapshots"""

@snapshots.command('list')
@click.option('--project',default=None,help="Only snapshots for Projects will be listed <tag Project : <Name>")
def list_snapshots(project):
    instances = filter_instances(project)
    for instance in instances :
        for volume in instance.volumes.all():
            for snapshot in volume.snapshots.all():
                print(f"""{snapshot.id},{volume.id},{instance.id},{snapshot.state},{snapshot.progress},{snapshot.start_time.strftime("%c")}""")
    return





@cli.group('instances')
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
    for instance in instances:
        print(f"Stopping {instance.id}")
        instance.stop()
    return



@instances.command('start')
@click.option('--project',default=None,help="Only instances for Projects will be started <tag Project : <Name>")
def start_instances(project) :
    """Starting EC2 instances"""

    instances = filter_instances(project)

    instances = filter_instances(project)
    for instance in instances :
        print(f"Starting {instance.id}")
        instance.start()
    return



@instances.command('snapshot')
@click.option('--project',default=None,help="Creates snapshots of all the volumes attached to instances for Projects  <tag Project : <Name>")

def create_snapshots(project):
    """Create Snapshot of Instances"""
    instances = filter_instances(project)
    for instance in instances:
        print(f"Stopping {instance.id} ...")
        instance.stop()
        instance.wait_until_stopped()
        for volume in instance.volumes.all():
            print(f"""Creating snapshot for {volume.id}...""")
            volume.create_snapshot(Description="Created by SnapshotAlyzer 30000")
        print(f"Starting {instance.id} ...")
        instance.start()
        instance.wait_until_running()
    print("Job done")
    return




session = boto3.Session(profile_name ='boto3practice')
ec2 = session.resource('ec2')






if __name__ == '__main__' :
    cli()
