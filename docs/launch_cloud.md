# Launching cloud VMs

## Amazon Cloud (AWS)

### Instructions
 * Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/.
 * Click "Launch instance"
 * Select "Community AMIs"
 * Enter AMI ID in search bar (without `ami-` prefix, e.g.: `006638a0a99849fc3`)
 * Select Quantum Mobile AMI
 * Select instance type depending on your computational needs (e.g. `t2.medium`)
 * (optional) click through to storage section if you need to change the disk size from the default of 15GB
 * Click "Review and Launch" 
 * Click "Launch"
 * Create a new key pair
 * Launch the VM

### Note
Since Quantum Mobile is based on the Ubuntu image, the SSH public key will be added to the `ubuntu` user (hardcoded by AWS), while the simulation environment has been set up for the `max` user.  
In order to log in as the `max` user using your key, do the following:

```
ssh ubuntu@<IP> -i /path/to/key.pem
sudo cat ~ubuntu/.ssh/authorized_keys  >> ~max/.ssh/authorized_keys
exit
```
Now you can log in as the `max` user:
```
ssh max@<IP> -i /path/to/key.pem
```

## Google Cloud (GCP)

### Prerequisites

 * An account on [cloud.google.com](https://cloud.google.com/)
 * A project with Compute Engine API enabled (see their [quickstart docs](https://cloud.google.com/compute/docs/quickstart-linux) )


### Launching the VM

 * Go to [https://console.cloud.google.com/compute/imagesDetail/projects/marvel-nccr/global/images/quantum-mobile-20-05-0](https://console.cloud.google.com/compute/imagesDetail/projects/marvel-nccr/global/images/quantum-mobile-20-05-0)  
 * Click on "CREATE INSTANCE"
 * Adapt VM to your needs
 * Use `ssh-keygen` on your machine to create an SSH private-public key pair
 * Open the public key in a text editor & edit the `user@server` bit at the end, replacing `user` by `max` 
 * Under "Security", copy-paste the public SSH key  
   (GCP will add this key to the `max` user)
 * Click on "Create"
 * Copy IP address

After a few seconds, you should be able to log in to your new server via
```
ssh max@<IP> -i /path/to/private_key
```
