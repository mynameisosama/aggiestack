# AggieStack
AggieStack CLI - A command line interface to manage virtual servers

- Module uses persistent storage 'shelves' to keep configuration information.
- Supports information loaded from multiple files.
- If data is repeated, it will be overwritten. Same server name in two config files will use data from latest file.
- Config files need to follow format of sample files provided in config folder.
- Log file is generated in root directory.

Time Taken:
   - Project was completed in 12 hrs
   - Part A (5 hours)
        - Adding rack and virtual machine data members
        - Created pre-processing for reading new hardware file
        - Adding server functions
        - Improving argparse for new instructions
   - Part B (2 hours)
        - Adding rack functions
        - Adding provisions for Part C
        - Improving argparse for new instructions
   - Part C (1 hour)
        - Completed provisions for managing image cache
        - Updated rack functions with image cache
        - Improving argparse for new instructions
   - 1 hr was spent improving logging and adding functionality of reading commands from file
   - 3 hrs were spent on testing and bug fixing

Setup requirements:
   - Python 3.7.0

Usage:
   - Run module from project directory.
   - Run help
       `python -m aggiestack --help`
   - Load physical server information
       `python -m aggiestack config --hardware config\hdwr-config.txt`
   - Load images information
       `python -m aggiestack config --images config\image-config.txt`
   - Load flavor information
       `python -m aggiestack config --flavors config\flavor-config.txt`
   - Display physical server information
       `python -m aggiestack show hardware`
   - Display images information
       `python -m aggiestack show images`
   - Display flavor information
       `python -m aggiestack show flavor`
   - Display all (racks, machines, images, flavors) information
       `python -m aggiestack show all`
   - Display current physical server information
       `python -m aggiestack admin show hardware`
   - Display current virtual server information
       `python -m aggiestack admin show instances`
   - Display current rack information (available storage and any images in storage server)
       `python -m aggiestack admin show imagecaches`
   - Add `<machine_name>` physical server to `<machine_rack>`
       `python -m aggiestack admin add --mem <memory> --disk <storage> --vcpus <cpus> -ip <machine_ip> -rack <machine_rack> <machine_name>`
   - Remove all physical and virtual servers from `<rack>`
       `python -m aggiestack admin evacuate <rack>`
   - Remove physical server `<machine>` from datacenter
       `python -m aggiestack admin remove <machine>`
   - Check whether a physical server can spawn a particular flavored VM
       `python -m aggiestack admin can_host <machine> <flavor>`
   - Create virtual server `<name>` with `<image>` and `<flavor>`
       `python -m aggiestack server create --image <image> --flavor <flavor> <name>`
   - Delete virtual server `<name>`
       `python -m aggiestack server delete <name>`
   - Display all virtual servers
       `python -m aggiestack server list`
