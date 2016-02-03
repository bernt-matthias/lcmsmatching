FROM ubuntu:14.04

MAINTAINER Pierrick Roger (pierrick.roger@gmail.com)

# Update package database
RUN apt-get update

# Install Ansible
RUN apt-get install -y git
WORKDIR /files
RUN git clone --recursive git://github.com/ansible/ansible.git ansible-src
WORKDIR /files/ansible-src
RUN apt-get install -y python python-setuptools
RUN apt-get install -y gcc
RUN apt-get install -y python-dev
RUN apt-get install -y libgmp-dev
RUN easy_install pip
RUN pip install paramiko PyYAML Jinja2 httplib2 six
RUN apt-get install -y libffi-dev
RUN apt-get install -y libssl-dev
RUN pip install 'requests[security]'
RUN apt-get install -y make
RUN make
RUN python setup.py install --record installed_files.txt
RUN ansible --version
RUN mkdir /etc/ansible
RUN echo '[local]\nlocalhost\n' > /etc/ansible/hosts

# Run ansible role
ADD ansible /files/ansible
WORKDIR /files/ansible
RUN ansible-playbook lcmsmatching.yml -c local

# Clean up
WORKDIR /files/ansible-src
RUN cat installed_files.txt | xargs rm -rf
RUN pip uninstall requests[security] paramiko PyYAML Jinja2 httplib2 six
RUN apt-get remove make libssl-dev libffi-dev libgmp-dev python-dev gcc python python-setuptools git
RUN apt-get clean && apt-get autoremove -y && rm -rf /var/lib/{apt,dpkg,cache,log}/ /tmp/* /var/tmp/*
WORKDIR /files
RUN rm -r /files/ansible-src

# Define Entry point script
ENTRYPOINT ["/files/lcmsmatching/r-msdb/search-mz"]
